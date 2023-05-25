
"""## Question 3
Done with Omema Rizvi or06360
"""

# Right now conser
import numpy as np
from statistics import mean 


WORLD_SIZE = 5
A_POS = [0, 1]
A_PRIME_POS = [4, 1]
B_POS = [0, 3]
B_PRIME_POS = [2, 3]
DISCOUNT = 0.9
TERMINAL = [WORLD_SIZE-1, WORLD_SIZE-1]
# left, up, right, down
ACTIONS = [np.array([0, -1]),
           np.array([-1, 0]),
           np.array([0, 1]),
           np.array([1, 0])]

       



def step(state, action):
    terminal = False
    if state == A_POS:
        return A_PRIME_POS, 10
    if state == B_POS:
        return B_PRIME_POS, 5
    if state == TERMINAL:
        print(f"the terminal state is reached")
        return None, 0,  #next_state ==  None --> state <-- Terminal  
 
    next_state = (np.array(state) + action).tolist()
    x, y = next_state
    if x < 0 or x >= WORLD_SIZE or y < 0 or y >= WORLD_SIZE:
        reward = -1.0
        next_state = state
    else:
        reward = 0
    return next_state, reward


def greedy_policy(value):
    '''
    Reused from Question 2
    '''

    policy = np.zeros((WORLD_SIZE, WORLD_SIZE), dtype=object)
    for i in range(WORLD_SIZE):
        for j in range(WORLD_SIZE):
            values = []
            for action_idx, action in enumerate(ACTIONS):
                if i == WORLD_SIZE -1 and j == WORLD_SIZE -1:
                    values.append(0)
                    continue
                (next_i, next_j), reward = step([i, j], action)
                values.append(reward + DISCOUNT * value[next_i, next_j])
            
            best_actions = np.argwhere(values == np.max(values)).flatten().tolist()
            policy[i, j] = np.array(best_actions)
    return policy


def moving_avg(v, n, G):
    '''
    Args:
    G: Return Value
    v: value of of state s belonging to S
    n: number of times s has been visited before, in previous episodes
    Return:
    
    '''
    v = n/(n+ 1)* (v+1/n * G)
    return  v


def generates_episode(Policy):
    '''
    Args:
    Policy: Policy pi
    Return:
    EP: Episode list: [()]
    '''

    too_long = False
    random = np.random.randint(25)
    i = random//5
    j = random%5 
    curr_state = [i,j] # State initialization 
    EP = list()
    terminal  = False
    while not terminal:
        action_index = np.random.choice(Policy[i, j])
        action = ACTIONS[action_index]
        next_state, reward = step(curr_state, action)
        EP.append((curr_state, action.tolist(), reward))
        if next_state == None:
            terminal = True
            break
        curr_state = next_state
        i,j = curr_state[0], curr_state[1]
        if len(EP) >= 100:
            too_long = True
            print('The Episode was stuck in a loop')
            break
    if too_long == True:
        EP = generates_episode(Policy)
        # print(f'(curr_state, action, reward) = {(curr_state, action, reward)}')

    return EP

def MC_first_Visit(policy):
    '''
    Args:
    N: number of states

    '''
    V = np.zeros((WORLD_SIZE, WORLD_SIZE))
    Returns = value = np.zeros((WORLD_SIZE* WORLD_SIZE), dtype = 'object')
    for i in range(len(Returns)):
        Returns[i] = list()  
    epsilon =  1e-2
    ep = 0
    while True:
        ep += 1
        episode = generates_episode(policy)
        print(f'The episode {ep} is: \n {episode}')
        old_value = V.copy() # For episode ep - 1
        # print(f'The oldvalue assighnment \n {old_value}')
        G = 0
        reverse_ep = episode.copy()
        reverse_ep.reverse()
        visited = reverse_ep.copy()
        
        for curr_state, action, reward in reverse_ep:
    
            visited.remove((curr_state, action, reward))
            G = DISCOUNT * G + reward
            # print(f'The state is = {curr_state}')
            # print(f'The visited is = \n ={visited}\n ')
            # print(f'The value of G = {G}')
            if not ((curr_state, action, reward) in visited):
                Returns[curr_state[0]*curr_state[1]].append(G)
                V[curr_state[0],curr_state[1]] = mean(Returns[curr_state[0]*curr_state[1]])
                # print('Value update = ',V[curr_state], 'The updated Value = ',V, sep = '\n')
            else: 
                print('Already Visited')
        # print(f"The updated value in episode {ep} is = \n {V}")  

        if np.sum(np.abs(V - old_value)) < 1e-2:
            print('__________________________________________________')
            # print(old_value)
            print('__________________________________________________')
            print(f'The value function converges at episode {ep} \n at the value is = \n{V}')
            print('__________________________________________________')
            print('__________________________________________________')
            break

    return V


def policy_iteration_MC(start_policy):
    policy = start_policy
    epoch = 0
    while True: 
        value =  MC_first_Visit(policy)
        epoch += 1

        stable = True
        new_policy = greedy_policy(value)
        print(f' The new policy at epoch {epoch} \n {new_policy}\n --------------------------')

        for i in range(len(new_policy)):
            for j in range(len(new_policy[i])):
                

                if not (new_policy[i, j].tolist() == policy[i,j].tolist()):
                    stable = False
        if stable == True:
            optimalPolicy = policy
            optimal_value =  value
            break
        
        policy = new_policy
        

        return policy

policy = [[np.array([0,1,2,3]), np.array([0,1,2,3]), np.array([0,1,2,3]),np.array([0,1,2,3]),np.array([0,1,2,3])],
          [np.array([0,1,2,3]),np.array([0,1,2,3]),np.array([0,1,2,3]),np.array([0,1,2,3]),np.array([0,1,2,3])],
          [np.array([0,1,2,3]),np.array([0,1,2,3]),np.array([0,1,2,3]),np.array([0,1,2,3]),np.array([0,1,2,3])],
          [np.array([0,1,2,3]),np.array([0,1,2,3]),np.array([0,1,2,3]),np.array([0,1,2,3]),np.array([0,1,2,3])],
          [np.array([0,1,2,3]),np.array([0,1,2,3]),np.array([0,1,2,3]),np.array([0,1,2,3]),np.array([0,1,2,3])]]
policy = np.array(policy)
# episode = generates_episode(policy)
# left, up, right, down
ACTIONS = [np.array([0, -1]),
           np.array([-1, 0]),
           np.array([0, 1]),
           np.array([1, 0])]
# MC_first_Visit(policy)
policy = policy_iteration_MC(policy)

left, up, right, down = 0,1,2,3
arrow_dic = dict([(0 , "left"), (1 ,"up"), (2 , "right"), (3, "down")])

Arrow = np.zeros_like(policy, dtype='object')
# print(Arrow)
for i in range(len(policy)):
    for j in range(len(policy[i])):
        temp = []
        for index in range(len(policy[i,j])):
            x= arrow_dic[policy[i,j][index]]
            temp.append(x)
        Arrow[i,j] = temp    
# print(Arrow.tolist())

for i in range(len(policy)):
    for j in range(len(policy[i])):
        # for index in range(len(policy[i,j])):
        print(Arrow[i, j], end = ' , ')
    print()
