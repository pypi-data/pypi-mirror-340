import math

def aashto_cbr_thickness(N, CBR, k=17, r=0.25):
    """
    Estimate total pavement thickness using the AASHTO-style empirical CBR method.
    Parameters:
        N (float): Cumulative number of standard axle repetitions (ESALs)
        CBR (float): California Bearing Ratio (%)
        k (float): Empirical coefficient (default=17)
        r (float): Empirical exponent (default=0.25)
    Returns:
        float: Total pavement thickness in mm
    """
    thickness = k * (N / CBR) ** r
    print(f"AASHTO-style thickness: {thickness:.2f} mm for N={N} and CBR={CBR}")
    return thickness

def naasra_cbr_thickness(N, CBR):
    """
    Estimate total pavement thickness using revised NAASRA-style method approximation.
    Parameters:
        N (float): Cumulative number of standard axle repetitions (ESALs)
        CBR (float): California Bearing Ratio (%)
    Returns:
        float: Total pavement thickness in mm
    Note:
        This formula uses a more realistic coefficient and exponent for practical design.
    """
    thickness = 75 * (N / CBR) ** 0.2
    print(f"NAASRA thickness (adjusted): {thickness:.2f} mm for N={N} and CBR={CBR}")
    return thickness

def austroads_cbr_thickness(N, CBR):
    """
    Estimate pavement thickness using simplified Austroads (ARX) empirical method.
    Parameters:
        N (float): Design traffic in ESA (ESALs)
        CBR (float): Subgrade California Bearing Ratio (%)
    Returns:
        float: Total pavement thickness in mm
    Reference:
        Austroads Guide to Pavement Technology Part 2 (AGPT02-17), conceptually simplified.
    """
    thickness = 95 * (N / (365 * 20 * CBR)) ** 0.18   # 20-year life, 365 days/year
    print(f"Austroads thickness (simplified): {thickness:.2f} mm for N={N} and CBR={CBR}")
    return thickness

def austroads_empirical_thickness(N, CBR):
    """
    Estimate pavement thickness using the Austroads empirical method from Figure 8.4.
    Parameters:
        N (float): Design traffic in ESA (Equivalent Standard Axles)
        CBR (float): Subgrade California Bearing Ratio (%)
    Returns:
        float: Total pavement thickness in mm
    Reference:
        Austroads Guide to Pavement Technology Part 2 (AGPT02-17), Figure 8.4.
    """
    thickness = 820 * (N ** 0.22) * (CBR ** -0.25)
    print(f"Austroads empirical thickness: {thickness:.2f} mm for N={N} and CBR={CBR}")
    return thickness


if __name__ == "__main__":
    # Unified example inputs
    N = 1_000_000  # ESALs
    CBR = 5  # %

    aashto_cbr_thickness(N, CBR)
    naasra_cbr_thickness(N, CBR)
    austroads_cbr_thickness(N, CBR)
    austroads_empirical_thickness(N, CBR)
