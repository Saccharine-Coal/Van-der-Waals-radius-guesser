import math
import sys
import os

from limits_from_xyz import get_geometry_data

# ordered by atomic number
VDW_RADII = {
    # https://en.wikipedia.org/wiki/Van_der_Waals_radius
    "H": 1.2,
    "He": 1.4,
    "Li": 1.82,
    "Be": 1.53,
    "B": 1.92,
    "C": 1.7,
    "N": 1.55,
    "O": 1.52,
    "F": 1.47,
    "Na": 2.27,
    "Mg": 1.73,
    "Al": 1.84,
    "Si": 2.10,
    "P": 1.8,
    "S": 1.8,
    "Cl": 1.75,
    "Te": 2.06,
    }
def minimize(xyz, vdw_radius):
    return tuple(val - (vdw_radius) for val in xyz)

def maximize(xyz, vdw_radius):
    return minimize(xyz, -vdw_radius)

def get_vdw_radius(atom: str, scale: int) -> float:
    return VDW_RADII[atom] * scale

def write_limits(x_lim, y_lim, z_lim, n_points=50):

    def format_to_str(lim: tuple, n_points: int) -> str:
        return f"{n_points} {lim[0]} {lim[1]}\n"

    FILENAME = "limits.plot"
    if os.path.exists(FILENAME):
        raise OSError
    else:
        with open(FILENAME, "w+") as file:
            file.write(format_to_str(x_lim, n_points))
            file.write(format_to_str(y_lim, n_points))
            file.write(format_to_str(z_lim, n_points))
        print(f"Limits have been written to {FILENAME}")

def main() -> None:
    args = sys.argv.copy()
    args.pop(0)     # this is the path to this file
    path_to_file = args.pop(0)  # this is the first argument that is given that is not this file
    xyz_table = get_geometry_data(path_to_file)
    #xyz_table.print()
    print(xyz_table.column("atom"))
    table_dict = {
            "i": [],
            "atoms": [],
            "x": [],
            "y": [],
            "z": []
            }
    # print(args)
    table_dict["i"] = list(i for i in range(0, xyz_table.num_rows))
    table_dict["atoms"] = xyz_table.column("atom")
    table_dict["x"] = xyz_table.column("x")
    table_dict["y"] = xyz_table.column("y")
    table_dict["z"] = xyz_table.column("z")
    mins, maxes = [], []
    for i, atom in enumerate(table_dict["atoms"]):
        xyz = (
                table_dict["x"][i],
                table_dict["y"][i],
                table_dict["z"][i]
                )
        vdw_radius = get_vdw_radius(atom, 2)
        mins.append(minimize(xyz, vdw_radius))
        maxes.append(maximize(xyz, vdw_radius))
    xyz_limits = []
    for i in range(0, 3):
        min_vals = tuple(val[i] for val in mins)
        max_vals = tuple(val[i] for val in maxes)
        axis_limit = (math.floor(min(min_vals)), math.ceil(max(max_vals)))
        xyz_limits.append(axis_limit)
        print(f"limits for axis {i} = {axis_limit}")
    write_limits(*xyz_limits)
main()
