"""
Problem Overview:
    The Function that accepts an input graph of
    nodes representing the total network and
    identifies the node with the most number
    of connections And Return the label of the node. 

Complexity : 
        o(n)    
 
Returns:
    _type_: str
"""


def identify_router(graph):
    router_dict = dict()
    nodes = graph.split(" -> ")

    for index, node in enumerate(nodes, start=0):
        if index == 0:
            router_dict[node] = 1
        elif index + 1 == len(nodes):
            router_dict[node] += 1
        else:
            if node in router_dict:
                value = router_dict[node]
                value += 2
                router_dict[node] = value
            else:
                router_dict[node] = 2

    max_router_values = max(router_dict.values())
    router = [
        key for key, value in router_dict.items() if value == max_router_values
        ]

    network_point = ", "
    network_point = network_point.join(router)
    return network_point
