import sys
import os

from tables import XYZTable
import xyz_from_file


def write_as_mol(table: XYZTable, filepath: str) -> None:
    """Write xyz table in .mol format."""
    start = "$molecule\n"
    mult = "0 1\n"
    end = "$end\n"
    with open(filepath, "w+") as file:
        file.write(start)
        file.write(mult)
        for line in table.as_strings():
            file.write(line)
        file.write(end)


def write_as_xyz(table: XYZTable, filepath: str) -> None:
    """Write xyz table in .xyz format."""
    num_molecules = table.num_rows
    spacing = "\n"
    with open(filepath, "w+") as file:
        file.write(str(num_molecules) + "\n")
        file.write(spacing)
        for line in table.as_strings():
            file.write(line)


def write_as_frag(table: XYZTable, filepath: str) -> None:
    """Write xyz table in .frag format."""
    raise NotImplementedError
    num_molecules = table.num_rows
    spacing = "\n"
    with open(filepath, "w+") as file:
        file.write(num_molecules)
        file.write(spacing)
        for line in table.as_strings():
            file.write(line)


TYPE_TO_FUNC = {
    ".mol": write_as_mol,
    ".frag": write_as_frag,
    ".xyz": write_as_xyz,
}


def main(sys_args: list) -> None:
    """Main"""
    sys_args.pop(0)     # this is the path to this file
    path_to_file: str = sys_args.pop(0)  # this is the first argument that is given that is not this file
    target_file: str = sys_args.pop(0)   # name.type
    print(path_to_file, target_file)
    xyz_table = xyz_from_file.main(path_to_file)
    file = os.path.split(target_file)[-1]
    if "." in file:
        filename, filetype = file.split(".")[:]
        formatted_type = "." + filetype
        if (formatted_type) in  TYPE_TO_FUNC.keys():
            func = TYPE_TO_FUNC.get(formatted_type)
            func(xyz_table, target_file)
        else:
            raise ValueError
    else: raise ValueError(f"file={target_file} does not have an explicit file extension.")

main(sys.argv.copy())
