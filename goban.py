import enum


class Status(enum.Enum):
    """
    Enum representing the Status of a position on a goban
    """

    WHITE = 1
    BLACK = 2
    EMPTY = 3
    OUT = 4


def adjacent_points(x, y):
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


class Goban(object):
    def __init__(self, goban):
        self.goban = goban

    def get_status(self, x, y):
        """
        Get the status of a given position

        Args:
            x: the x coordinate
            y: the y coordinate

        Returns:
            a Status
        """
        if (
                not self.goban
                or x < 0
                or y < 0
                or y >= len(self.goban)
                or x >= len(self.goban[0])
        ):
            return Status.OUT
        elif self.goban[y][x] == ".":
            return Status.EMPTY
        elif self.goban[y][x] == "o":
            return Status.WHITE
        elif self.goban[y][x] == "#":
            return Status.BLACK

    def is_taken(self, x_coord, y_coord):

        def is_form_blocked(coordinate_square, form_status, checked_coordinates):
            unchecked_coordinates = (coord for coord in coordinate_square if coord not in checked_coordinates)
            coord_and_status = {(x, y): self.get_status(x, y) for (x, y) in unchecked_coordinates}
            if Status.EMPTY in coord_and_status.values():
                return False
            return are_adjacent_points_blocked(coord_and_status, checked_coordinates, form_status)

        def are_adjacent_points_blocked(coord_and_status, checked_coordinates, form_status):
            for (x, y), status in coord_and_status.items():
                checked_coordinates.append((x, y))
                if not is_point_blocked(x, y, status, form_status, checked_coordinates):
                    return False
            return True

        def is_point_blocked(x, y, status, form_status, checked_coordinates):
            if status == Status.EMPTY:
                return False
            if status == form_status:
                if not is_form_blocked(adjacent_points(x, y), form_status, checked_coordinates):
                    return False
            return True

        return is_form_blocked(adjacent_points(x_coord, y_coord), self.get_status(x_coord, y_coord), [])

