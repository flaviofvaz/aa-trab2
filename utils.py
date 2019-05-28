import queue
from itertools import permutations


def breadth_first_search(graph_obj):
    num_components = 0

    graph = graph_obj[0]
    state_to_idx = graph_obj[1]

    visited_states = []
    for i in range(len(graph)):
        visited_states.append(0)

    for idx in range(len(graph)):
        visited_states[idx] = 1

        found_new = False
        to_be_visited = queue.Queue()
        to_be_visited.put(idx)

        while to_be_visited.qsize() != 0:
            state = to_be_visited.get()
            for neighbour in graph[state]:
                if visited_states[state_to_idx[neighbour]] == 0:
                    found_new = True
                    visited_states[state_to_idx[neighbour]] = 1
                    to_be_visited.put(state_to_idx[neighbour])

        if found_new:
            num_components += 1

    return num_components


def BFS_adapted(graph_obj, initial_state):
    graph = graph_obj[0]
    state_to_idx = graph_obj[1]

    visited_states = []
    for i in range(len(graph)):
        visited_states.append(0)

    visited_states[state_to_idx[initial_state]] = 1

    layers = []
    layers.append([initial_state])

    i = 0
    while True:
        layer = []        
        for state in layers[i]:
            for neighbour in graph[state_to_idx[state]]:
                if visited_states[state_to_idx[neighbour]] == 0:
                    layer.append(neighbour)
                    visited_states[state_to_idx[neighbour]] = 1

        if len(layer) == 0:
            return layers

        layers.append(layer)
        i += 1

    return layers


def make_states_graph(side_size):
    ''' Creates the states graph for the problem based on an initial instance

        Arguments
        ------------------------------
        initial_instance: is a string with L x L digits. 
        Each character is a digit, and represents where the piece with that number is located in the LxL board.
        The number 0 represents an empty space at the board.

        Returns
        ------------------------------
        The states graph for the problem as an adjacency list.

    '''

    # get permutations of the string initial_state - that is, all possible states in the board
    all_states = [''.join(e) for e in permutations('123456780')]

    # string set with the states visited so far
    visited_states = set()

    # adjacency list
    graph = []

    # dictionary state_string : index in graph list
    idx_to_state = {}
    state_to_idx = {}

    # keep going until there are no more states to visit
    idx = 0
    for initial_state in all_states:
        if (initial_state not in visited_states):
            visited_states.add(initial_state)

            # string queue with the states we need to visit
            states_stack = []
            states_stack.append(initial_state)

            # integer stack with the empty position on the board for the current state
            empty_space_stack = []

            # locating where is the empty space in the initial state
            for i in range(len(initial_state)):
                if initial_state[i] == '0':
                    empty_space_stack.append(i)

            while (len(states_stack) > 0):
                empty_space_int = int(empty_space_stack.pop())
                empty_space = (int(empty_space_int//side_size),
                        int(empty_space_int % side_size))

                # getting current state to be visited - we have marked it as visited before because we don't want duplicates in our list
                current_state = states_stack.pop()

                # filling dictionaries
                state_to_idx[current_state] = idx
                idx_to_state[idx] = current_state

                # updating index
                idx += 1

                # list for state neighbours
                neighbours = []

                if empty_space[1] + 1 < side_size:
                    # we can go right
                    new_state, new_empty_space = move_piece(
                    current_state, empty_space, (empty_space[0], empty_space[1] + 1), side_size)

                    if new_state not in visited_states:
                        empty_space_stack.append(new_empty_space)
                        states_stack.append(new_state)
                        visited_states.add(new_state)

                    # add edge from new state to old state
                    neighbours.append(new_state)

                if empty_space[0] + 1 < side_size:
                    # we can go down
                    new_state, new_empty_space = move_piece(
                        current_state, empty_space, (empty_space[0] + 1, empty_space[1]), side_size)

                    if new_state not in visited_states:
                        empty_space_stack.append(new_empty_space)
                        states_stack.append(new_state)
                        visited_states.add(new_state)

                    # add edge from new state to old state
                    neighbours.append(new_state)

                if empty_space[0] - 1 >= 0:
                    # we can go up
                    new_state, new_empty_space = move_piece(
                        current_state, empty_space, (empty_space[0] - 1, empty_space[1]), side_size)

                    if new_state not in visited_states:
                        empty_space_stack.append(new_empty_space)
                        states_stack.append(new_state)
                        visited_states.add(new_state)

                    # add edge from new state to old state
                    neighbours.append(new_state)

                if empty_space[1] - 1 >= 0:
                    # we can go left
                    new_state, new_empty_space = move_piece(
                        current_state, empty_space, (empty_space[0], empty_space[1] - 1), side_size)

                    if new_state not in visited_states:
                        empty_space_stack.append(new_empty_space)
                        states_stack.append(new_state)
                        visited_states.add(new_state)

                    # add edge from new state to old state
                    neighbours.append(new_state)

                graph.append(neighbours)

    return (graph, state_to_idx, idx_to_state) 


def move_piece(current_state, empty_space, piece_space, side_size):
    empty_1D_pos = empty_space[0] * side_size + empty_space[1]
    piece_1D_pos = piece_space[0] * side_size + piece_space[1]

    state_as_list = list(current_state)

    state_as_list[empty_1D_pos] = state_as_list[piece_1D_pos]
    state_as_list[piece_1D_pos] = '0'

    return ''.join(state_as_list), piece_1D_pos


graph = make_states_graph(3)

# counting edges
num_edges = 0
for edge_list in graph[0]:
    num_edges += len(edge_list)

# each edge is counted twice
num_edges = num_edges/2

# size of the list is the number of nodes in the graph
graph_size = len(graph[0])

print(graph_size)
print(num_edges)

# getting number of components
num_components = breadth_first_search(graph)

print(num_components)

# Get layers starting from our desired configuration
BFS_layers = BFS_adapted(graph, '123456780')

# nodes from the last layer are the more distant from cfg* 
for e in BFS_layers[-1]:
    print(e)

# checking if the number of nodes found was as expected (9!/2) 
num_nodes = 0
for nodes in BFS_layers:
    num_nodes += len(nodes)

print(num_nodes)

