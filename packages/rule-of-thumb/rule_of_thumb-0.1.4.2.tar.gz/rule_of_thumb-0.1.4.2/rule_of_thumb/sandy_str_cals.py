import math
fck = 32  # MPa
c = 45  # mm AS 3600- Table 4.10.3.2 & Clause 4.10.3.5
soil_unit_weight = 20  # kN/m^3
soil_phi = 30  # degrees
Soil_c = 0
wall_height = 3.2 #meter

#Floor Load


# Active earth pressure coefficient
k_a = (1 - math.sin(math.radians(soil_phi))) / (1 + math.sin(math.radians(soil_phi)))
p_soil = k_a * soil_unit_weight * wall_height

print(f"Active earth pressure coefficient (k_a): {k_a:.3f}")
print(f"soil Pressure (P_soil): {p_soil:.3f} kPa")