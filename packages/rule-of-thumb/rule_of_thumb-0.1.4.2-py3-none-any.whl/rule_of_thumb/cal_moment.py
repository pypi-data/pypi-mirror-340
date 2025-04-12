import math 
def simple_b_udl(load_kN: float, span: float) -> float:
    """
    Calculates the minimum square footing size based on first principles.
    Formula: m = wl^2 / 8
    :param load_kN: Applied vertical load in kN
    :param span: span between two supports  in m
    :param safety_factor: Factor of safety to apply to bearing capacity (default = 1.5)
    """
    if span <= 0:
        raise ValueError("span must be greater than zero.")
    
    # Compute required footing area (m = wl^2 / 8)
    moment = load_kN * span**2 /8
    reaction = load_kN * span / 2 
    
    # Print results
    print(f"Calculated moment due to uniformally distributed load : {moment:.3f} kN-m")
    print(f"Calculated support reaction due to uniformally distributed load : {reaction:.3f} kN")
    print('---------------------------')

    return moment

# Example usage
#simple beam uniformally distributed load and its span(5, 10)
if __name__ == "__main__":
    simple_b_udl(5, 10)


def simple_b_udl_cons_mid_span(udl: float,con_load:float, span: float) -> float:
    """
    Calculates the minimum square footing size based on first principles.
    Formula: m = wl^2 / 8
    :param load_kN: Applied vertical load in kN
    :param span: span between two supports  in m
    :param safety_factor: Factor of safety to apply to bearing capacity (default = 1.5)
    """
    if span <= 0:
        raise ValueError("span must be greater than zero.")
    
    # Compute required footing area (m = wl^2 / 8)
    moment = udl * span**2 /8 + con_load * span /4
    reaction = udl * span / 2 + con_load / 2 
    
    # Print results
    print(f"Calculated moment due to udl and concentrated load of {con_load}kN : {moment:.3f} kN-m")
    print(f"Calculated support reaction due to udl and concentrated load of {con_load}kN : {reaction:.3f} kN")
    print('-------------------------------')


    return moment , reaction

# Example usage
#simply supported beam  with uniformally dis. load and concentrated load midspan(5,2, 10)
if __name__ == "__main__":
    simple_b_udl_cons_mid_span(5,2, 10)