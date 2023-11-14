from minizinc import Instance, Model, Solver
from parser import *
import json

def get_categories(patients):
    ret = []

    for e in patients:
        ret += [e["category"]]

    for e in patients:
        ret += [e["category"]]    

    # print(ret)
    return ret

def load_instance_data(instance, instance_file):
    # Opening JSON file
    with open(instance_file) as f:
        data = json.load(f)

    # BASE 
    instance["sameVehicleBackward"] = data["sameVehicleBackward"]
    instance["maxWaitTime"] = hours_deformat(data["maxWaitTime"])

    # PLACES
    instance["N_places"] = number_of_places(data["places"])
    instance["places"] = get_places(data["places"])

    # VEHICLES
    vehicles = get_vehicles(data["vehicles"])
    instance["vehicles"] = vehicles[0]
    instance["N_vehicles"] = len(vehicles[0])
    instance["Unique_vehicles"] = vehicles[1]
    instance["category_set"] = vehicles[2]

    # PATIENTS
    instance["N_patients"] = number_of_patients(data["patients"])
    instance["patients"] = get_patients(data["patients"])
    instance["N_requested_trips"] = 2 * instance["N_patients"]
    instance["patients_category"] = get_categories(data["patients"])
 
    # DISTANCE
    instance["dist_matrix"] = data["distMatrix"]




def hours_format(num):

    hours = int(num/60)
    if (hours < 10):
        hours = "0" + str(hours)
    else:
        hours = str(hours)

    minutes = num%60
    if (minutes < 10):
        minutes = "0" + str(minutes)
    else:
        minutes = str(minutes)
    return hours + "h" + minutes


class StartOrder:
    def __init__(self,i,start,dur):
        self.i = i 
        self.start = start
        self.dur = dur

def custom_sort_key(o):
    return (o.start)

def getMinimumPatient(patients,curr,sorted_order):

    min_pat = -1
    for i in range(len(patients)): 
        if (sorted_order[patients[i]].start + sorted_order[patients[i]].dur < sorted_order[curr].start):
            if (min_pat == -1):
                min_pat = patients[i]
            
            elif (sorted_order[patients[i]].start + sorted_order[patients[i]].dur < sorted_order[min_pat].start + sorted_order[min_pat].dur):
                min_pat = patients[i]
    return min_pat

def getPatientsIDS(patients,N_places,N_vehicles,N_patients):
    ret = []
    first_id = N_places + N_vehicles

    for e in patients:
        _id = first_id + e
        ret += [_id]
    
    return ret

def create_vehicle_json(result,instance,_id):

    N_places = instance["N_places"]
    N_vehicles = instance["N_vehicles"]
    N_patients = instance["N_patients"]

    dist_matrix = instance["dist_matrix"]

    all_vehicles_activities = result["activities_vehicles"]
    starts = result["start_activities"]
    dur = result["dur_activities"]

    filtered_with_vehicle = []

    i = 0
    for e in all_vehicles_activities:
        if (e == _id):
            filtered_with_vehicle += [i]
        
        i += 1

    vehicle = instance["vehicles"][_id-1]


    all_patients = instance["patients"]

    orders = []
    for e in filtered_with_vehicle:
        

        st = StartOrder(e,starts[e],dur[e])
        orders += [st]


    sorted_order = sorted(orders,key=custom_sort_key)

    vehicle_info = {}
    
    N_e_vehicles_patients = 0
    N_e_patients_vehicles = 0
    if (instance["vehicles"][0]["true_id"] < instance["patients"][0]["true_id"]): 
        N_e_vehicles_patients = instance["vehicles"][len(instance["vehicles"]) - 1]["true_id"] - N_places + 1
    else:
        N_e_patients_vehicles = instance["patients"][len(instance["patients"]) - 1]["true_id"] - N_places + 1


    vehicle_info["id"] = instance["vehicles"][_id-1]["true_id"]
    #vehicle_info["id"] = _id + N_e_patients_vehicles + N_places - 1

    trips = []
    for e in sorted_order:
        if (all_patients[e.i]["origin"] == 0 or all_patients[e.i]["destination"] == 0):
            sorted_order.remove(e)

    all_patients = sorted(all_patients, key= lambda x: x["id"])

    trip = {}
    trip["origin"] = vehicle["start"] 
    trip["destination"] = all_patients[sorted_order[0].i]["origin"] - 1
    trip["arrival"] = hours_format(sorted_order[0].start)
    trip["patients"] = []
    trips += [trip]
    vehicle_info["trips"] = trips
    
    previous_dest = trip["destination"]

    # CREATE HELP ACTION STRUTURE
    PICKUP = 0
    DROP = 20000
    curr_patients = []
    actions = []
    for i in range(len(sorted_order)):
        edited = True
        while(edited):
            edited = False
            drop_patient = getMinimumPatient(curr_patients,i,sorted_order)
            if (drop_patient != -1):
                actions += [DROP + drop_patient]
                curr_patients.remove(drop_patient)
                edited = True
        
        curr_patients += [i]
        actions += [PICKUP + i]
    
    for e in curr_patients:
        actions += [DROP + e]




    # USE ACTION STRUCTURE
    patients = []
    iter_a = 0

    #all_patients = sorted(all_patients, key= lambda x: x["id"])

    for e in actions:
        iter_a += 1
        # ITS A DROP
      
        if (e >= DROP):
            j = e - DROP
            trip = {}

            trip["origin"] = previous_dest
            curr_dest = all_patients[sorted_order[j].i]["destination"] - 1
            trip["destination"] = curr_dest
            trip["arrival"] = hours_format(sorted_order[j].start + sorted_order[j].dur - all_patients[sorted_order[j].i]["srvDuration"])
            trip["patients"] = getPatientsIDS(patients.copy(),N_places,N_e_vehicles_patients ,N_patients) # patients.copy()
            
            # MUDEI AQUI
            j = sorted_order[j].i

            try:
                if (j >= N_patients):
                    patients.remove(j-N_patients)
                else:
                    patients.remove(j)
            except:
                pass

            previous_dest = trip["destination"]
            if (trip["origin"] != trip["destination"]):
                trips += [trip]

        # ITS A PICKUP
        else:
           
            j = e
            trip = {}

            trip["origin"] = previous_dest
            curr_dest = all_patients[sorted_order[j].i]["origin"] - 1
            trip["destination"] = curr_dest
            
            if (actions[iter_a-1] < DROP):
                trip["arrival"] = hours_format(sorted_order[j].start)
            else:
                trip["arrival"] = hours_format(sorted_order[j].start - all_patients[sorted_order[j].i]["srvDuration"])
            
            trip["patients"] = getPatientsIDS(patients.copy(),N_places,N_vehicles,N_patients) # patients.copy()

            # MUDEI AQUI
            j = sorted_order[j].i

            if (j >= N_patients):
                patients += [j - N_patients]
            else:
                patients += [j]

            previous_dest = trip["destination"]
            if (trip["origin"] != trip["destination"]):
                trips += [trip]
            else:
                #patients.remove(j)
                pass

    # RETURN TO FINAL STOP 
    trip = {}
    trip["origin"] = previous_dest
    trip["destination"] = vehicle["end"]
    trip["arrival"] = hours_format(sorted_order[-1].start + sorted_order[-1].dur + dist_matrix[previous_dest][vehicle["end"]])
    trip["patients"] = []
    trips += [trip]
    vehicle_info["trips"] = trips


    vehicle_info_str = json.dumps(vehicle_info, indent=2)

    return vehicle_info

def get_one_vehicle_json(result,instance,_id):

    N_requests = instance["N_requested_trips"]
    vehicles_per_activitie = result["activities_vehicles"]
    flag = False
    for i in range(N_requests):
        if (_id == vehicles_per_activitie[i]):
            flag = True
    
    if (not(flag)):
        return {"id" : _id, "trips" : []}

    else:
        return create_vehicle_json(result,instance,_id)


def get_vehicles_json(result,instance):

    ret = []

    # DECISION VARIABLES
    N_places = instance["N_places"]
    N_patients = instance["N_patients"]
    N_vehicles = instance["N_vehicles"]
    N_requests = instance["N_requested_trips"]
    



    vehicles = instance["vehicles"]
    patients = instance["patients"]

    requests = result["requests"]
    activities = result["activities"]
    starts = result["start_activities"]
    durations = result["dur_activities"]
    vehicles_per_activitie = result["activities_vehicles"]

    for i in range(N_vehicles):
        vehicle = get_one_vehicle_json(result,instance,i+1)
        if (vehicle["trips"] != []):
            ret += [vehicle]

    print(ret)
    FINAL_RET = []
    prev = -1
    for e in ret:
        if (e["id"] == prev):
            del FINAL_RET[-1]["trips"][-1]
            del e["trips"][0]
            FINAL_RET[-1]["trips"] += e["trips"] 

        else:
            FINAL_RET += [e]
        prev = e["id"]

    return FINAL_RET


def create_solution_json(result,instance):

    # Final response
    ret = {}

    # REQUEST
    requests = result["OBJETIVO"]
    ret["requests"] = int(requests)

    # VEHICLES
    vehicles = get_vehicles_json(result,instance)
    ret["vehicles"] = vehicles

    return ret



                
