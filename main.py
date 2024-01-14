from tools import *
from coords import *
from solver import solver_algo
from game import UnknownColorException

def aux(pos):
    try:
        print(pos)
        path = solver_algo(pos)
        return path
    except UnknownColorException as e:
        print(e.error_path)
        print("Unknown", e.tube_number, e.unknown_position)
        new_pos = handle_exception(pos, nb_couleurs, e.error_path, e.tube_number, e.unknown_position)
        reset()
        return aux(new_pos)

def solving(nb_couleurs):
    reset()
    infos = coords_dict[nb_couleurs]
    capture_screenshot(screenshot_path)
    print("Reading the image")
    initial_position = read_color(infos[color_coords], infos[empty_tube_count], nb_couleurs)
    print("Beginning solving algorithm")
    path = aux(initial_position)
    if path is None:
        print("Issue searching solution, solution not found")
        exit(0)
    print("Solution found")
    solving_path(path, infos[tube_coords])


if __name__ == "__main__":
    nb_couleurs = int(input("How many colors ? "))
    solving(nb_couleurs)
