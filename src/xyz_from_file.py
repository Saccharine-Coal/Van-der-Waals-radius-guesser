"""Handles extracting geometry data from the following custom defined file types .frag, .xyz .mol"""
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

FILETYPE_TO_FUNC = {
    ".frag": geom_from_frag,
    ".xyz": geom_from_xyz,
    ".mol": geom_from_mol,
}


def get_geometry_data(path: str) -> dict:
    valid = True    # handles whether to raise an error
    SEP = "."
    if os.path.exists(path) and (SEP in path):
        split_by_sep = os.path.split(path)[-1].split(SEP)
        filename, filetype = split_by_sep[0], SEP + split_by_sep[-1]
        if filetype in SUPPORTED_FILETYPES:
            with open(path, mode="r") as file:
                func = FILETYPE_TO_FUNC.get(filetype)
                return func(file)
        else: valid = False
    else: valid = False
    if not valid:
        raise ValueError(f"path={path}")


if __name__ == "__main__":
    file = "Te.xyz"
    tbl = get_geometry_data(file)
    tbl.print()
