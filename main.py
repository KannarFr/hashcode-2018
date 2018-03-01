import numpy as np
import pandas as pd
import os

DATA_FOLDER = 'data' 

class Vehicle(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.rides = []

    def dist_to_ride(self, ride):
        return np.abs(self.x - ride.start_x) + np.abs(self.y - ride.start_y)

def distance(coords1, coords2):
    return (coords2[1] - coords1[1]) + (coords2[0] - coords1[0])

def parse_data(filename):
    data = np.loadtxt(filename)
    rows, columns, vehicles, rides, bonus, steps = tuple(data[0, :])
    info = {
        'rows': rows,
        'columns': columns,
        'nb_rides': int(rides),
        'nb_vehicles': vehicles,
        'bonus': bonus,
        'nb_steps': steps
    }
    rides = data[1:, :]
    rides_df = pd.DataFrame(data=rides, columns=["start_x", "start_y", "end_x", "end_y", "min_start", "max_finish"])
    return info, rides_df

def get_ride_distance(ride):
    return np.abs(ride.start_x - ride.end_x) + np.abs(ride.start_y - ride.end_y)


def assign_vehicle_to_ride(vehicle, ride, current_timestamp):
    vehicle_to_ride = vehicle.dist_to_ride(ride)
    ride_distance = get_ride_distance(ride)
    return int(current_timestamp + max(vehicle_to_ride, int(ride.min_start) - current_timestamp) + ride_distance)


def perform_simulation(info, rides, filename):
    sorted_rides = rides.sort_values(['min_start', 'max_finish'])
    fleet = [Vehicle() for _ in range(int(info['nb_vehicles']))]
    availability_by_timestamps = [[] for _ in range(int(info['nb_steps']))]

    current_time = 0
    ride_cursor = 0
    # Initialisation
    for i in range(len(fleet)):
        availability_by_timestamps[0].append(fleet[i])

    print(fleet[0])
    print(availability_by_timestamps[0][0])
    for i in range(len(availability_by_timestamps)):
        while len(availability_by_timestamps[i]) and ride_cursor < len(sorted_rides):
            cur_vehicle = availability_by_timestamps[i].pop()
            ride = sorted_rides.iloc[ride_cursor, :]
            ride_cursor += 1
            next_availability = assign_vehicle_to_ride(cur_vehicle, ride, i)
            if next_availability > len(availability_by_timestamps):
                availability_by_timestamps[i].append(cur_vehicle)
                continue
            cur_vehicle.x = ride.end_x
            cur_vehicle.y = ride.end_y
            cur_vehicle.rides.append(ride.name)
            availability_by_timestamps[next_availability].append(cur_vehicle)
    generate_result(fleet, filename)

def generate_result(fleet, filename):
    with open(filename, 'a') as f:
        for idx, vehicle in enumerate(fleet):
            f.write(str(len(vehicle.rides)) + " ")
            for i in range(len(vehicle.rides)):
                f.write(str(vehicle.rides[i]) + " ")
            f.write(str("\n"))


def main():
    data_files = os.listdir(DATA_FOLDER)
    for filename in data_files:
        info, rides = parse_data(os.path.join(DATA_FOLDER, filename))
        print(info, rides.shape)
        perform_simulation(info, rides, 'results/' + filename)
    #info, rides = parse_data(os.path.join(DATA_FOLDER, "a_example.in"))
    #print(info, rides.shape)
    #perform_simulation(info, rides)



if __name__ == '__main__':
    main()
