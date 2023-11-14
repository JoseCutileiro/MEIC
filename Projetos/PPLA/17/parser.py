def hours_deformat(str):
    parts = str.split('h')
    return int(parts[0]) * 60 + int(parts[1])

def number_of_places(places):
    return len(places)

def get_places(places):
    ret = []
    for e in places:
        ret += [e['category']]
    
    return ret

def number_of_vehicles(vehicles):
    return len(vehicles)

def canTake_parsing(L):
    L = sorted(L)
    ret = 0
    mul = 1
    for e in L:
        ret = ret + e * mul
        mul *= 10 
    return ret

def parse_time_range(time_range):
    parts = time_range.split(':')
        
    start_time, end_time = parts
    
    start_hours, start_minutes = map(int, start_time[:-1].split('h'))
    end_hours, end_minutes = map(int, end_time[:-1].split('h'))
    
    start_total_minutes = start_hours * 60 + start_minutes
    end_total_minutes = end_hours * 60 + end_minutes
    
    return [start_total_minutes, end_total_minutes]

def get_vehicles(vehicles):

    ret = []
    i = 1

    category = []

    for e in vehicles:
        new_e = {}
        new_e["id"] = i
        new_e["true_id"] = e["id"]
        new_e["canTake"] = canTake_parsing(e['canTake'])
        
        new_e["start"] = e['start']
        new_e["end"] = e['end']
        new_e["capacity"] = e['capacity']

        for t in e['availability']:
            availability = parse_time_range(t)
            new_e["available_begin"] = availability[0]
            new_e["available_end"] = availability[1]
            category += [(set(e["canTake"]))]
            ret += [new_e.copy()]

        i += 1
    
    # print(category)
    return [ret,i,category]

def number_of_patients(patients):
    return len(patients)

def get_patients(patients):
    ret = []
    num_req = 0
    i = 1

    num_pac = 0
    for patient in patients:
        num_pac += 1

    for patient in patients:

        # FORWARD ACTIVITIE
        new_e_F = {}
        new_e_F["id"] = i
        new_e_F["true_id"] = patient["id"]
        new_e_F["category"] = patient["category"]
        new_e_F["load"] = patient["load"]
        new_e_F["rdvTime"] = hours_deformat(patient["rdvTime"])
        new_e_F["rdvDuration"] = hours_deformat(patient["rdvDuration"])
        new_e_F["srvDuration"] = hours_deformat(patient["srvDuration"])
        new_e_F["origin"] = patient["start"] + 1
        new_e_F["destination"] = patient["destination"] + 1
        ret += [new_e_F]

        # BACKWARD ACTIVITIE
        new_e_B = {}
        new_e_B["id"] = i + num_pac
        new_e_B["true_id"] = patient["id"]
        new_e_B["category"] = patient["category"]
        new_e_B["load"] = patient["load"]
        new_e_B["rdvTime"] = hours_deformat(patient["rdvTime"])
        new_e_B["rdvDuration"] = hours_deformat(patient["rdvDuration"])
        new_e_B["srvDuration"] = hours_deformat(patient["srvDuration"])
        new_e_B["origin"] = patient["destination"] + 1
        new_e_B["destination"] = patient["end"] + 1
        ret += [new_e_B]

        i += 1

    
    return ret
