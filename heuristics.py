import numpy as np
from state import get_pos_2d
import config



class Heuristic:
    def get_evaluation(self, state):
        pass


class ExampleHeuristic(Heuristic):
    def get_evaluation(self, state):
        return 0

class Hamming(Heuristic):

    def get_evaluation(self, state):

        arr_state = np.array(state)
        final_state = np.array([i for i in range(1, config.N * config.N)])
        final_state = np.append(final_state, 0)
        num_out_of_pos_tiles = sum(~(arr_state == final_state))
        if(state[-1] != 0):
            num_out_of_pos_tiles = num_out_of_pos_tiles - 1

        return num_out_of_pos_tiles

class Manhattan(Heuristic):

    def get_evaluation(self, state):

        sum_of_manhattan_distance = 0

        for i in range(len(state)):
            if(state[i] == 0):
                continue

            x1, y1 = get_pos_2d(i)
            x2, y2 = get_pos_2d(state[i] - 1)
            sum_of_manhattan_distance += abs(x1 - x2) + abs(y1 - y2)

        return sum_of_manhattan_distance



