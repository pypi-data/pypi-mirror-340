import math

def moment_of_area(shape, **kwargs):
    """
    Calculate the second moment of area (I) about the centroidal axis for standard shapes.

    Supported shapes:
    - rectangle: b = base, h = height
    - circle: r = radius
    - hollow_circle: ro = outer radius, ri = inner radius
    - triangle: b = base, h = height
    - hollow_rectangle: bo = outer base, ho = outer height, bi = inner base, hi = inner height
    - i_beam: bf = flange width, tf = flange thickness, h = total height, tw = web thickness

    Returns:
    I in units^4
    """
    shape = shape.lower()
    
    if shape == "rectangle":
        b = kwargs['b']
        h = kwargs['h']
        return (b * h**3) / 12

    elif shape == "circle":
        r = kwargs['r']
        return (math.pi * r**4) / 4

    elif shape == "hollow_circle":
        ro = kwargs['ro']
        ri = kwargs['ri']
        return (math.pi * (ro**4 - ri**4)) / 4

    elif shape == "triangle":
        b = kwargs['b']
        h = kwargs['h']
        return (b * h**3) / 36  # centroidal axis

    elif shape == "hollow_rectangle":
        bo = kwargs['bo']
        ho = kwargs['ho']
        bi = kwargs['bi']
        hi = kwargs['hi']
        return ((bo * ho**3) - (bi * hi**3)) / 12

    elif shape == "i_beam":
        bf = kwargs['bf']
        tf = kwargs['tf']
        h = kwargs['h']
        tw = kwargs['tw']
        I_flange = (bf * tf**3) / 6
        d = (h - tf) / 2
        I_total = 2 * (I_flange + bf * tf * d**2) + (tw * (h - 2 * tf)**3) / 12
        return I_total

    else:
        raise ValueError(f"Unsupported shape: {shape}")

if __name__ == "__main__":
    # Example: Hollow circular section with ro = 0.2 m, ri = 0.15 m
    I = moment_of_area("hollow_circle", ro=0.2, ri=0.15)
    print(f"Second moment of area for hollow circle: {I:.6f} m^4")
