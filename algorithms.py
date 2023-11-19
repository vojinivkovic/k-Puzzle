import random
import time

import numpy as np

import config
import numpy
from heuristics import Hamming, Manhattan
from queue import Queue


def add_new_state(previous_states, state):
    temp_arr = previous_states[:]
    temp_arr.append(state)
    return temp_arr

def add_new_action(actions, action):
    temp_arr = actions[:]
    temp_arr.append(action)
    return temp_arr


class Node:
    def __init__(self, state, actions, steps=0):
        self.state = state

        #if(previous_states == None):
         #   self.previous_states = []
        #else:
         #   self.previous_states = previous_states

        if(actions == None):
            self.actions = []
        else:
            self.actions = actions

        self.steps = steps



   # def get_previous_states(self):
    #    return self.previous_states

    def get_state(self):
        return self.state

    def get_actions(self):
        return self.actions

    def get_steps(self):
        return self.steps


class Algorithm:
    def __init__(self, heuristic=None):
        self.heuristic = heuristic
        self.nodes_evaluated = 0
        self.nodes_generated = 0

    def get_legal_actions(self, state):
        self.nodes_evaluated += 1
        max_index = len(state)
        zero_tile_ind = state.index(0)
        legal_actions = []
        if 0 <= (up_ind := (zero_tile_ind - config.N)) < max_index:
            legal_actions.append(up_ind)
        if 0 <= (right_ind := (zero_tile_ind + 1)) < max_index and right_ind % config.N:
            legal_actions.append(right_ind)
        if 0 <= (down_ind := (zero_tile_ind + config.N)) < max_index:
            legal_actions.append(down_ind)
        if 0 <= (left_ind := (zero_tile_ind - 1)) < max_index and (left_ind + 1) % config.N:
            legal_actions.append(left_ind)
        return legal_actions

    def apply_action(self, state, action):
        self.nodes_generated += 1
        copy_state = list(state)
        zero_tile_ind = state.index(0)
        copy_state[action], copy_state[zero_tile_ind] = copy_state[zero_tile_ind], copy_state[action]
        return tuple(copy_state)

    def get_steps(self, initial_state, goal_state):
        pass

    def get_solution_steps(self, initial_state, goal_state):
        begin_time = time.time()
        solution_actions = self.get_steps(initial_state, goal_state)
        print(f'Execution time in seconds: {(time.time() - begin_time):.2f} | '
              f'Nodes generated: {self.nodes_generated} | '
              f'Nodes evaluated: {self.nodes_evaluated}')
        return solution_actions


class ExampleAlgorithm(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        solution_actions = []
        while state != goal_state:
            legal_actions = self.get_legal_actions(state)
            action = legal_actions[random.randint(0, len(legal_actions) - 1)]
            solution_actions.append(action)
            state = self.apply_action(state, action)
        return solution_actions

class BFS(Algorithm):

    def get_steps(self, initial_state, goal_state):

        first_node = Node(initial_state, None)
        queue_of_nodes = Queue(maxsize=0)
        queue_of_nodes.put(first_node)
        visited_states = set()

        while queue_of_nodes:

            node = queue_of_nodes.get()
            visited_states.add(node.get_state())

            if(node.get_state() == goal_state):
                solution_actions = node.get_actions()
                break

            legal_actions = self.get_legal_actions(node.get_state())

            for action in legal_actions:
                new_state = self.apply_action(node.get_state(), action)
                if(new_state not in visited_states):
                    new_node = Node(new_state, add_new_action(node.get_actions(), action))
                    queue_of_nodes.put(new_node)



        return solution_actions

class BestFirstSearch(Algorithm):

    def get_steps(self, initial_state, goal_state):

        first_node = Node(initial_state, None)
        queue_of_nodes = [first_node]

        queue_of_values = [self.heuristic.get_evaluation(first_node.get_state())]
        visited_states = set()


        while True:

            node = queue_of_nodes.pop(0)
            visited_states.add(node.get_state())
            queue_of_values.pop(0)

            if(node.get_state() == goal_state):
                solution_actions = node.get_actions()
                break

            legal_actions = self.get_legal_actions(node.get_state())

            for action in legal_actions:
                new_state = self.apply_action(node.get_state(), action)
                if (new_state not in visited_states):
                    new_node = Node(new_state, add_new_action(node.get_actions(), action))
                    value = self.heuristic.get_evaluation(new_node.get_state())

                    flag = 0

                    for i in range(len(queue_of_values)):
                        if (value < queue_of_values[i]):
                            flag = 1
                            idx = i
                            break
                        if (value == queue_of_values[i]):
                            if (new_node.get_state() < queue_of_nodes[i].get_state()):
                                flag = 1
                                idx = i
                                break


                    if (flag == 0):
                        queue_of_nodes.append(new_node)
                        queue_of_values.append(value)
                    else:
                        queue_of_nodes.insert(idx, new_node)
                        queue_of_values.insert(idx, value)




        return solution_actions



class A_star(Algorithm):

    def get_steps(self, initial_state, goal_state):

        first_node = Node(initial_state, None)

        queue_of_nodes = [first_node]
        value = self.heuristic.get_evaluation(first_node.get_state()) + first_node.get_steps()
        queue_of_values = [value]
        visited_states = set()

        while True:

            node = queue_of_nodes.pop(0)
            visited_states.add(node.get_state())
            queue_of_values.pop(0)

            if(node.get_state() == goal_state):
                solution_actions = node.get_actions()
                break

            legal_actions = self.get_legal_actions(node.get_state())

            for action in legal_actions:
                new_state = self.apply_action(node.get_state(), action)

                if (new_state not in visited_states):

                    new_node = Node(new_state, add_new_action(node.get_actions(), action), node.get_steps() + 1)
                    value = self.heuristic.get_evaluation(node.get_state()) + new_node.get_steps()

                    flag = 0
                    for i in range(len(queue_of_values)):
                        if(value < queue_of_values[i]):
                            flag = 1
                            idx = i
                            break
                        if(value == queue_of_values[i]):
                            if(new_node.get_state() < queue_of_nodes[i].get_state()):
                                flag = 1
                                idx = i
                                break
                    if(flag == 0):
                        queue_of_nodes.append(new_node)
                        queue_of_values.append(value)
                    else:
                        queue_of_nodes.insert(idx, new_node)
                        queue_of_values.insert(idx, value)


        return solution_actions

