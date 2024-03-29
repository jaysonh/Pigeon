# Math functions to help
def map_data( data : float, in_min : float, in_max : float, out_min : float, out_max : float):
    return (data - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)