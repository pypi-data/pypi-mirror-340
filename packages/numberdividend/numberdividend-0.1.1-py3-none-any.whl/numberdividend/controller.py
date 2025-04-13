def check_type_list(data):
    if isinstance(data, list):
        return True
    else:
        raise TypeError("Input data must be a list.")
    
def check_type_float(data):
    data = float(data)
    if isinstance(data, float):
        return True
    else:
        raise TypeError("Input data must be a float.")
    
def check_type_int(data):
    if isinstance(data, int):
        return True
    else:
        raise TypeError("Input data must be an int.")
