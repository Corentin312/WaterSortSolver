from collections import deque
import time
from game import *

def is_in_set(position_set, newL):
    return tuple(sorted(newL)) in position_set

def solver_algo(L, max_iter=1000, affichage=False):
    nb_tubes = len(L)
    nb_iter = 0
    seen_positions = set([tuple(sorted(L))])
    positions_to_explore = deque([(L.copy(), [])])
    b_verif = False

    while positions_to_explore and nb_iter < max_iter and not b_verif:
        nb_iter += 1
        nb_position_iter = len(positions_to_explore)
        t_s_i = time.time()

        for _ in range(nb_position_iter):
            position, path = positions_to_explore.popleft()
            
            for i in range(nb_tubes):
                for j in range(nb_tubes):
                    new_path = path + [(i, j)]
                    try:
                        newL, b_move, b_verif = move_and_verify(position, i, j)
                    except UnknownColorException as e:
                        raise UnknownColorException(unknown_position=e.unknown_position,
                                                    tube_number=e.tube_number,
                                                    error_path=path) from e                     

                    if b_verif:
                        return new_path

                    elif b_move and not is_in_set(seen_positions, newL):
                        positions_to_explore.append((newL, new_path))
                        seen_positions.add(tuple(sorted(newL)))
        if affichage:
            t_f_i = time.time()
            print("Iteration", nb_iter)
            print(len(seen_positions), "seen positions")
            print(len(positions_to_explore), "positions to explore")
            print("Iteration time : ", t_f_i - t_s_i, "seconds")
            print()

    return None

def print_path(path, L, write_file=None):
    Lecr_file = []
    Lecr_print = []
    L2 = L.copy()
    for i, j in path:
        L2, _, _ = move_and_verify(L2, i, j)
        if write_file is not None:
            Lecr_file.append(str((i, j)) + "  \t" + str(L2))
        Lecr_print.append(str((i, j)))
    if write_file is not None:
        write_file.write("\n".join(Lecr_file))
    print("\n".join(Lecr_print))

def solver(L):
    t_s = time.time()
    try:
        path = solver_algo(L, affichage=True)
        t_f = time.time()
        print("Elapsed time :", t_f - t_s, "seconds")
        if path is None:
            print("Not Found")
        else:
            with open("files/solution.txt", mode='w', encoding="utf-8") as fd:
                print_path(path, L, write_file=fd)
    except UnknownColorException as e:
        i = e.tube_number
        print("Unknown color faced using the following path")
        print_path(e.error_path, L)
        print("Error there with tube", i, L[i])
        print("Please change the initial position")
    

if __name__ == "__main__":
    initial_position = init(1)
    solver(initial_position)
