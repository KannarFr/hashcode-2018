import numpy as np
import os

DATA_FOLDER = 'data' 


def distance(coords1, coords2):
    return (coords2[1] - coords1[1]) + (coords2[0] - coords1[0])

def parse_data(filename):
    data = np.loadtxt(filename)
    rows, columns, vehicles, rides, bonus, steps = tuple(data[0, :])
    info = {
        'rows': rows,
        'columns': columns,
        'rides': rides,
        'nb_vehicles': vehicles,
        'bonus': bonus,
        'nb_steps': steps
    }
    rides = data[1:, :]
    return info, rides

def main():
    data_files = os.listdir(DATA_FOLDER)
    for filename in data_files:
        info, rides = parse_data(os.path.join(DATA_FOLDER, filename))
        print(info, rides.shape)

if __name__ == '__main__':
    main()
