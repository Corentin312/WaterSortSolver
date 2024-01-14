from typing import List, Tuple

TUBE_SIZE = 4

class UnknownColorException(Exception):
    def __init__(self, unknown_position=None, tube_number=None, error_path=None):
        super().__init__()
        self.unknown_position = unknown_position
        self.tube_number = tube_number
        self.error_path = error_path

def init(nb_couleurs: int) -> List[Tuple[int, int, int, int]]:
    if nb_couleurs == 0:
        return [(1, 2, 3, 2), (2, 3, 3, 1), (1, 3, 1, 2), (0, 0, 0, 0), (0, 0, 0, 0)]
    else:
        return [(2, -1, 10, 9), (8, 4, 11, 6), (10, 10, 7, 4), (4, 8, 7, 5), (1, 6, 3, 12), (8, 12, 7, 6), (1, 11, 9, 2), (3, 12, 7, 11), (2, 3, 4, 11), (3, 8, 5, 5), (6, 12, 2, 1), (9, 9, 5, 10), (0, 0, 0, 0), (0, 0, 0, 0)]

def get_top(tube: Tuple[int, int, int, int]) -> Tuple[int, int, int]:
    top, top_size, empty_size = 0, 0, 0
    for v in tube:
        if v == 0 and top == 0:
            empty_size += 1
        elif top == 0:
            top, top_size = v, 1
        elif v == top:
            top_size += 1
        else:
            break
    return top, top_size, empty_size

def move(L: List[Tuple[int, int, int, int]], i_in: int, i_out: int) -> Tuple[List[Tuple[int, int, int, int]], bool]:
    if i_in == i_out:
        return L, False
    
    L2 = L.copy()
    t_in, t_out = L2[i_in], L2[i_out]
    top_in, top_size_in, empty_size_in = get_top(t_in)

    if top_in == -1:
        raise UnknownColorException(unknown_position=empty_size_in, tube_number=i_in)

    top_out, _, empty_size_out = get_top(t_out)

    if top_out == 0:  # Empty out
        if top_in == 0:  # Empty in
            return L2, False
        else:  # Move to the empty output
            l_in, l_out = list(t_in), list(t_out)
            for i in range(top_size_in):
                l_in[i + empty_size_in] = 0
                l_out[TUBE_SIZE - i - 1] = top_in   
            L2[i_in], L2[i_out] = tuple(l_in), tuple(l_out)
            return L2, True
        
    else:
        if empty_size_out == 0 or top_in != top_out:  # No place or different tops
            return L2, False
        else:
            n_to_move = min(empty_size_out, top_size_in)
            l_in, l_out = list(t_in), list(t_out)
            for i in range(n_to_move):
                l_in[i + empty_size_in] = 0
                l_out[empty_size_out - i - 1] = top_in   
            L2[i_in], L2[i_out] = tuple(l_in), tuple(l_out)
            return L2, True

def verify(L: List[Tuple[int, int, int, int]]) -> bool:
    return all(all(element == t[0] for element in t) for t in L)

def move_and_verify(L: List[Tuple[int, int, int, int]], i_in: int, i_out: int) -> Tuple[List[Tuple[int, int, int, int]], bool, bool]:
    try:
        L2, b_move = move(L, i_in, i_out)
    except UnknownColorException:
        raise
    b_verif = verify(L2)
    return L2, b_move, b_verif


if __name__ == "__main__":
    L = init(1)
    nbc = len(L) - 2
    Lnb = [0] * nbc
    for t in L:
        for e in t:
            if 1 <= e <= nbc:
                Lnb[e-1] += 1
    print(Lnb)





