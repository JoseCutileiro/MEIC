include "cumulative.mzn";

%%%%%%%%%%%%%%%%%%%%%%
% O que eles nos dão %
%%%%%%%%%%%%%%%%%%%%%%

%% STANDARD

bool: sameVehicleBackward;


int: maxWaitTime; 

%% PLACES

int: N_places;
array [1..N_places] of var 0..2: places;

%% VEHICLES

type Vehicle = record (
    int: id,
    int: true_id,
    int: canTake,
    int: start,
    int: end,
    int: capacity,
    int: available_begin,
    int: available_end,
);

int: N_vehicles;
array [1..N_vehicles] of Vehicle: vehicles;
array [1..N_vehicles] of set of int: category_set;



% PATIENTS

type Patient = record (
    int: id,
    int: true_id,
    int: category,
    int: load,
    int: origin,
    int: destination,
    int: rdvTime,
    int: rdvDuration,
    int: srvDuration,
);

int: N_patients;
int: N_requested_trips;

array [1..N_requested_trips] of Patient: patients;
array [1..N_requested_trips] of int: patients_category;

% DISTANCES

array [1..N_places,1..N_places] of int: dist_matrix;

%%%%%%%%%%%%%%%%%%%%%%%
% Decision variables  %
%%%%%%%%%%%%%%%%%%%%%%%

array [1..N_patients] of var 0..1: requests;
array [1..N_requested_trips] of var 0..1: activities;

array [1..N_requested_trips] of var 0..1440: start_activities;
array [1..N_requested_trips] of var 0..maxWaitTime: dur_activities;
array [1..N_requested_trips] of var 1..N_vehicles: activities_vehicles;

%%%%%%%%%%%%%%%%%%%%%%%
%    Constraints      %
%%%%%%%%%%%%%%%%%%%%%%%

% TODO: Validar se o start ou o end for -1

% 4.1: Feito pelo parsing (já está)

% 4.2: Dominio binario (já está)

% 4.3
constraint forall (i in patients where i.id <= N_patients) ((start_activities[i.id] + dur_activities[i.id]) <= i.rdvTime); 


% 4.4
constraint forall (i in patients where i.id > N_patients) (start_activities[i.id] >= (i.rdvTime + i.rdvDuration));

% 4.5
constraint forall (i in patients where i.id <= N_patients) (
        (start_activities[i.id] >= i.rdvTime - maxWaitTime)
        /\ 
        ((start_activities[i.id + N_patients] + dur_activities[i.id + N_patients]) <= i.rdvTime + i.rdvDuration + maxWaitTime)
    );

% 4.6
constraint forall (i in patients where i.id <= N_patients) (
        (start_activities[i.id] >= i.rdvTime - maxWaitTime /\ start_activities[i.id] <= i.rdvTime)
    /\
        ((start_activities[i.id] + dur_activities[i.id]) >= i.rdvDuration /\ (start_activities[i.id] + dur_activities[i.id]) <= i.rdvTime)
    /\
        ((start_activities[i.id + N_patients]) >= i.rdvTime + i.rdvDuration /\ (start_activities[i.id + N_patients]) <= i.rdvTime + i.rdvDuration + maxWaitTime)
    /\
        ((start_activities[i.id + N_patients] + dur_activities[i.id + N_patients]) >= i.rdvTime + i.rdvDuration /\ (start_activities[i.id + N_patients] + dur_activities[i.id + N_patients]) <= i.rdvTime + i.rdvDuration + maxWaitTime)
);

/*
constraint forall (i in patients, v in vehicles) (
    if (v.id == activities_vehicles[i.id])
    then
       i.category == v.canTake \/ v.canTake == 210 \/
        (i.category == v.canTake mod 10) \/ (i.category == v.canTake div 10 /\ v.canTake >= 10) 
    endif
);
*/

/*
constraint forall (i in 1..N_requested_trips) (
    (
            patients[i].category in category_set[activities_vehicles[i]]
    )
);
*/

% 4.6
constraint forall (i in 1..N_requested_trips) (
    (
            patients_category[i] in category_set[activities_vehicles[i]]
    )
);


% 4.7
constraint forall (i in patients where i.id <= N_patients) ( if (activities[i.id] == 1 /\ activities[i.id + N_patients] == 1) then requests[i.id] == 1 endif);

% 4.8
constraint forall (i in patients where i.id <= N_patients) ( activities[i.id] == activities[i.id + N_patients]);

% 4.9
constraint
            forall (i,j in patients where i.id != j.id /\ i.id != j.id + N_patients /\ i.id < j.id) (
                if (i.origin != 0 /\ j.origin != 0 /\ i.destination != 0 /\ j.destination != 0 /\ (activities_vehicles[i.id] == activities_vehicles[j.id]))
                    then
                        (
                            (
                                (activities_vehicles[i.id] == activities_vehicles[j.id]) /\
                                (   
                                    (start_activities[j.id] - start_activities[i.id] >= dist_matrix[i.origin ,j.origin] + i.srvDuration)
                                    \/ 
                                    (start_activities[i.id] - start_activities[j.id] >= dist_matrix[j.origin ,i.origin] + j.srvDuration)
                                )
                            )

                            /\

                            (
                                (activities_vehicles[i.id] == activities_vehicles[j.id]) /\
                                (   
                                    (start_activities[j.id] - (start_activities[i.id] + dur_activities[i.id]) >= dist_matrix[i.origin ,j.destination])
                                    \/ 
                                    ((start_activities[i.id] + dur_activities[i.id]) - start_activities[j.id] >= dist_matrix[j.destination ,i.origin] + j.srvDuration + i.srvDuration)
                                )
                            )

                            /\

                            (
                                (activities_vehicles[i.id] == activities_vehicles[j.id]) /\
                                (   
                                    ((start_activities[j.id] + dur_activities[j.id]) - start_activities[i.id] >= dist_matrix[i.destination ,j.origin] + i.srvDuration + j.srvDuration)
                                    \/ 
                                    (start_activities[i.id] - (start_activities[j.id] + dur_activities[j.id]) >= dist_matrix[j.origin ,i.destination])
                                )
                            )

                            /\

                            (
                                (activities_vehicles[i.id] == activities_vehicles[j.id]) /\
                                (   
                                    ((start_activities[j.id] + dur_activities[j.id]) - (start_activities[i.id] + dur_activities[i.id]) >= dist_matrix[i.destination ,j.destination] + j.srvDuration)
                                    \/ 
                                    ((start_activities[i.id] + dur_activities[i.id]) - (start_activities[j.id] + dur_activities[j.id]) >= dist_matrix[j.destination ,i.destination] + i.srvDuration)
                                )
                            )
                        )
                    endif
            );

%4.10
constraint forall (i in patients where i.origin > 0 /\ i.destination > 0) (dur_activities[i.id] >= dist_matrix[i.origin,i.destination] + 2 * i.srvDuration);


% 4.11 CUMULATIVE: TODO
constraint forall (j in 1..N_vehicles) (
    cumulative( [if (activities_vehicles[i] == vehicles[j].id) then start_activities[i] else 0 endif | i in 1..(N_requested_trips)],
                [if (activities_vehicles[i] == vehicles[j].id) then dur_activities[i] else 0 endif | i in 1..(N_requested_trips)],
                [if (activities_vehicles[i] == vehicles[j].id) then patients[i].load else 0 endif | i in 1..(N_requested_trips)],
                vehicles[j].capacity)
);

/*
% 4.12 TODO VER SE ISTO É BOM 
constraint forall (i in patients, v in vehicles where i.origin > 0 /\ i.destination > 0) (
    if (v.id == activities_vehicles[i.id] /\ i.rdvTime - maxWaitTime >= v.available_begin /\ i.rdvTime + i.rdvDuration + maxWaitTime <= v.available_begin)
    then 
    start_activities[i.id] >= v.available_begin + dist_matrix[v.start, i.origin]
    /\
    start_activities[i.id] + dur_activities[i.id] <= v.available_end - dist_matrix[i.destination,v.end]
    endif
);
*/

constraint forall (i in patients where i.origin > 0 /\ i.destination > 0 /\ activities_vehicles[i.id] != -1) (
    start_activities[i.id] >= vehicles[activities_vehicles[i.id]].available_begin + dist_matrix[vehicles[activities_vehicles[i.id]].start, i.origin]
    /\
    start_activities[i.id] + dur_activities[i.id] <= vehicles[activities_vehicles[i.id]].available_end - dist_matrix[i.destination,vehicles[activities_vehicles[i.id]].end]
);

% 4.13 // TODO ?????

var int: sum_executed_activities;
var int : OBJETIVO;


constraint sum(a in activities)(activities[a]) == sum_executed_activities;
constraint sum(r in requests)(requests[r]) == OBJETIVO;

solve maximize OBJETIVO;

