# Algorithm pseudo code

## dead end calculation
```
def dead_end_calculation(wall)
    """
    calculate self side and transform the result to get symmetric result on the opponent's side
    """
    parent = {}
    dead_ends = location only has only one neighbor
    for dead_end in dead_ends
        parent[dead_end] = None
        
        # traverse the path
        stack <- dead_end
        while stack not empty
            loc <- pop stack
            # num_neighbors_in_parent means these neighbors are paths in dead end
            if num_neighbors_not_in_parent == 1
                parent[loc] = the_neighbor_not_in_parent
                stack <- the_neighbor_not_in_parent

    return res
```

## initial_offensive 
```
def initial_offensive_position_calculation(is_red):
    first_agent <- closest position # I can't assume that first_agent is the agent that is closest to the position among all agents
    rest_agents <- random by Counter(rest positions: dist_to_pos) # the more far, higher probility to be chosen
```

## offensive_food_selection
```
def offensive_food_selection(is_red):
    for food sorted by dist_to_agent:
        if save_to_go_to and has_path_to_go_to
            go to eat this food
```
