import numpy as np
import pandas as pd
import os

DATA_FOLDER = 'data' 

class Vehicle(object):
    def __init__(self):
        


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

def perform_simulation(info, rides):
    sorted_rides = rides.sort_values(['min_start', 'max_finish'])
    available_vehicles = info['nb_vehicles']

    current_time = 0
    print(sorted_rides)


def main():
    data_files = os.listdir(DATA_FOLDER)
    for filename in data_files:
        info, rides = parse_data(os.path.join(DATA_FOLDER, filename))
        print(info, rides.shape)
        perform_simulation(info, rides)




if __name__ == '__main__':
    main()
