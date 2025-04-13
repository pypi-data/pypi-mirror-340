import numpy as np

from cogrid.core.directions import Directions
from cogrid.core.grid_object import GridObj


class Agent:
    def __init__(self, agent_id, start_position, start_direction, **kwargs):
        """
        When developing a subclass, you must, at the very least, implement `consume()`. This
        defines how an agent interacts with their current position on the map and sets their reward
        for that turn.

        :param agent_id: unique identifier
        :param start_position: starting spawn position
        :param env: 2d grid environment
        :param obs_type: `position' or 'view'. Position simply returns (row, col) coordinates,
                view returns a matrix representing the FoV.
        :param image: (boolean) If true, a `view' observation will return an RGB image (e.g., for CNNs)
        :param row_view: how many rows in either direction the agent can view
        :param col_view: how many columns in either direction the agent can view
        :param actions: dict keyed by integers with corresponding string actions
        """
        self.id: str = agent_id
        self.pos: tuple[int, int] = start_position
        self.dir: Directions = start_direction
        self.role: str = None
        self.role_idx: int = None
        self.inventory_capacity: int = kwargs.get("inventory_capacity", 1)

        self.terminated: bool = False

        self.collision: bool = (
            False  # Some envs keep track of if an agent crashed into another agent/object/etc.
        )

        self.orientation: str = "down"
        self.inventory: list[GridObj] = []
        self.cell_toggled: GridObj | None = None
        self.cell_placed_on: GridObj | None = None
        self.cell_picked_up_from: GridObj | None = None
        self.cell_overlapped: GridObj | None = None

    def rotate_left(self):
        self.dir -= 1
        if self.dir < 0:
            self.dir += 4

    def rotate_right(self):
        self.dir = (self.dir + 1) % 4

    @property
    def front_pos(self):
        return self.pos + self.dir_vec

    @property
    def dir_vec(self):
        # dir_to_vec = [
        #     # Pointing right (positive X)
        #     np.array((0, 1)),
        #     # Down (positive Y)
        #     np.array((1, 0)),
        #     # Pointing left (negative X)
        #     np.array((0, -1)),
        #     # Up (negative Y)
        #     np.array((-1, 0)),
        # ]
        dir_to_vec = {
            Directions.Right: np.array((0, 1)),  # Increase col away from 0
            Directions.Down: np.array(
                (1, 0)
            ),  # Down increases the row number (0 is top)
            Directions.Left: np.array(
                (0, -1)
            ),  # Left decreases the col towards 0
            Directions.Up: np.array(
                (-1, 0)
            ),  # Up decreases the row to 0 (move towards the top)
        }
        return dir_to_vec[self.dir]

    @property
    def right_vec(self):
        # TODO(chase): check that this is correct
        dy, dx = self.dir_vec
        return np.array((dx, -dy))

    def set_orientation(self):
        self.orientation = {
            Directions.Up: "up",
            Directions.Down: "down",
            Directions.Left: "left",
            Directions.Right: "right",
        }[self.dir]

    def can_pickup(self, grid_object: GridObj) -> bool:
        return len(self.inventory) < self.inventory_capacity

    def pick_up_object(self, grid_object: GridObj):
        self.inventory.append(grid_object)

    @property
    def agent_number(self) -> int:
        """Converts agent id to integer, beginning with 1,
        e.g., agent-0 -> 1, agent-1 -> 2, etc.
        """
        return int(self.id[-1]) + 1 if isinstance(self.id, str) else self.id + 1
