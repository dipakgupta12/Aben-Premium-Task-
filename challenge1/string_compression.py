"""
    The Function that takes string as as input
    parameter and will returns its compressed
    version and If the length of the string
    is not reduced,it will return the original string.
    
Explanation:
    If the length of string is == 1 
    so time Complexity is O(1)
    and if it is greater than 1 
    then the time complexity is O(n)
    An algorithm is said to have a linear time
    complexity when the running time increases
    at most linearly with the size of the input data.
    This is the best possible time complexity
    when the algorithm must examine all values
    in the input data.
 
Returns:
    _type_: str
"""


def compress(string):
    compression = ""
    count = 1
    if len(string) > 1:
        for i in range(len(string) - 1):
            if string[i] == string[i + 1]:
                count += 1
            else:
                compression = compression + string[i] + str(count)
                count = 1
        compression = compression + string[i + 1] + str(count)
        if len(compression) < len(string):
            return compression
    return string
