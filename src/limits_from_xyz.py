import math
import sys
import os

import xyz_from_file

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
    "Se": 1.90,
    "Te": 2.06,
    }
def minimize(xyz, vdw_radius):
    return tuple(val - (vdw_radius) for val in xyz)

def maximize(xyz, vdw_radius):
    return minimize(xyz, -vdw_radius)

def get_vdw_radius(atom: str, scale: int) -> float:
    return VDW_RADII[atom] * scale

def input_to_bool(question: str) -> bool:
    """Gets user y/n response and returns a bool corresponding to y or n."""
    invalid = True
    while invalid:
        print(f"WARNING: {question} Continue? (y/n)")
        response = input()
        if response == "y" or response == "n":
            invalid = False
    return True if response == "y" else False


def write_limits(x_lim, y_lim, z_lim, n_points=50, target_dir=".", comment=""):

    def format_to_str(lim: tuple, n_points: int) -> str:
        return f"{n_points} {lim[0]} {lim[1]}\n"

    format_to_write = f"$plots\n {comment}\n{format_to_str(x_lim, n_points)}{format_to_str(y_lim, n_points)}{format_to_str(z_lim, n_points)}0 1 0 0\n0\n$end\n"
    FILENAME = "limits.plot"
    path_to_file = os.path.join(target_dir, FILENAME)
    if input_to_bool(f"{path_to_file} already exists. OVERWRITE?"):

        with open(path_to_file, "w+") as file:
            file.write(format_to_write)
            print(f"Limits have been written to {path_to_file}")
    else:
        print(f"Limits have not been written.")


def main() -> None:
    """Main"""
    args = sys.argv.copy()
    args.pop(0)     # this is the path to this file
    path_to_file = args.pop(0)  # this is the first argument that is given that is not this file
    xyz_table = xyz_from_file.main(path_to_file)
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
    axes = ("x", "y", "z")
    for i in range(0, 3):
        min_vals = tuple(val[i] for val in mins)
        max_vals = tuple(val[i] for val in maxes)
        axis_limit = (math.floor(min(min_vals)), math.ceil(max(max_vals)))
        xyz_limits.append(axis_limit)
        print(f"limits for axis {axes[i]} = {axis_limit}")
    head, tail = os.path.split(path_to_file)[:]
    comment = f"Auto Generated limits for {path_to_file}"
    write_limits(*xyz_limits, target_dir=head, comment=comment)
main()
