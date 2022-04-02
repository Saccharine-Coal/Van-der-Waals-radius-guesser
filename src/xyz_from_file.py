"""Handles extracting geometry data from the following custom defined file types .frag, .xyz .mol"""
from __future__ import annotations    # type hinting

import os

from tables import XYZTable

SUPPORTED_FILETYPES = (".frag", ".xyz", ".mol")
ESCAPE_CHARACTERS = ("$", "!", "--", "0 1")

def trim_escape_lines(file) -> list:
    trimmed_lines = []
    for line in file:
        if not any(char in line for char in ESCAPE_CHARACTERS):
            trimmed_lines.append(line)
    return trimmed_lines


def geom_from_frag(file: object) -> XYZTable:
    """xyz from .frag"""
    # TODO: separate by fragments
    raise NotImplementedError
    trimmed_lines = trimmed_lines(file)
    return XYZTable(trimmed_lines)


def geom_from_xyz(file) -> XYZTable:
    """xyz from .xyz"""
    trimmed_lines = trim_escape_lines(file)
    trimmed_lines.pop(0)    # number of atoms line
    trimmed_lines.pop(0)    # blank line
    return XYZTable(trimmed_lines)


def geom_from_mol(file) -> XYZTable:
    """xyz from .mol"""
    trimmed_lines = trim_escape_lines(file)
    return XYZTable(trimmed_lines)

"""
 ******************************
 **  OPTIMIZATION CONVERGED  **
 ******************************
"""


def geom_from_out(file: list[str]) -> XYZTable:
    """xyz from .out"""
    # TODO add functionality to pull xyz from non
    # converged .out
    # check if opt has converged
    converged_str = "OPTIMIZATION CONVERGED"
    z_mx_str = "Z-matrix Print:"
    converged = False
    for line in file:
        if converged_str in line:
            converged = True
            break
    if not converged:
        raise NotImplementedError(".out has not converged!")
    yanked_lines = yank(file, converged_str, z_mx_str)
    lines = yanked_lines[5:-1]  # gets only atoms with xyz
    lines = [line[7:] for line in lines]    # remove atom number column
    return XYZTable(lines)


def yank(file, start_flag: str, end_flag: str) -> list[str]:
    """Pull the lines that are between two flags. NotImplemented: Inclusive=True include the flags themselves."""
    yanked_lines = []
    yanking = False
    for line in file:
        #print(start_flag in line, line, start_flag)
        if start_flag in line:
            print("yanking=True", line)
            yanking = True
        if end_flag in line:
            print("yanking=False", line)
            yanking = False
        if yanking:
            yanked_lines.append(line)
    return yanked_lines



FILETYPE_TO_FUNC = {
    ".frag": geom_from_frag,
    ".xyz": geom_from_xyz,
    ".mol": geom_from_mol,
    ".out": geom_from_out
}


def main(path: str) -> XYZTable:
    """get_geometry_data"""
    valid = True    # handles whether to raise an error
    SEP = "."
    if os.path.exists(path) and (SEP in path):
        split_by_sep = os.path.split(path)[-1].split(SEP)
        filename, filetype = split_by_sep[0], SEP + split_by_sep[-1]
        if filetype in FILETYPE_TO_FUNC.keys():
            with open(path, mode="r") as file:
                lines = file.readlines()
                func = FILETYPE_TO_FUNC.get(filetype)
                return func(lines)
        else: valid = False
    else: valid = False
    if not valid:
        raise ValueError(f"path={path}")


if __name__ == "__main__":
    pass
    #
    #file = "../docs/example/Cyano.out"
    #tbl = get_geometry_data(file)
    #tbl.print()
