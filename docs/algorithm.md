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
