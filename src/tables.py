from __future__ import annotations


class XYZRow:
    def __init__(self, row_data: str):
        # atom symbol | x | y | z
        strings = row_data.split(" ")
        filtered_strings = []
        for string in strings:
            if string:
                filtered_strings.append(string)
        strings = filtered_strings
        atom_symbol = strings[0]
        x = float(strings[1])
        y = float(strings[2])
        z = float(strings[3])
        col_headers = ("atom", "x", "y", "z")
        col_data = (atom_symbol, x, y, z)
        row_data = {key: val for key, val in zip(col_headers, col_data)}
        self.data = row_data
        self._ordered_headers = col_headers

    @property
    def headers(self) -> list:
        """Ordered"""
        return [key for key in self._ordered_headers]

    @property
    def values(self) -> list:
        """Ordered"""
        return [self.data.get(key) for key in self.headers]

    def __repr__(self) -> str:
        return str(self.data.values())

    def column(self, col_name: str):
        return self.data.get(col_name)

class XYZTable:
    def __init__(self, row_lines: list[str]):
        self.rows = []
        self.ordered_headers = ["atom", "x", "y", "z"]
        for line in row_lines:
            self.rows.append(XYZRow(line))

    @property
    def headers(self) -> list:
        return self.ordered_headers

    @property
    def num_rows(self) -> int:
        return len(self.rows)

    def column(self, col_name: str) -> list:
        if col_name in self.headers:
            column_list = []
            for row in self.rows:
                column_list.append(row.column(col_name))
            return column_list
        else:
            raise KeyError

    def print(self):
        print(self.ordered_headers)
        for row in self.rows:
            print(row.values)

