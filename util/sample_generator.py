# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.


class Room:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
    def __repr__(self):
        if self.e_to is not None:
            return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        return f"({self.x}, {self.y})"
    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)
    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 10
        self.height = 10
    def generate_rooms(self, size_x, size_y, num_rooms):
        def fillGrid():
            grid = [[None] * 10 for x in range(10)]
            counter = 0
            for i in range(10):
                for j in range(10):
                    count_string = f'{counter}th'
                    if counter == 1: count_string = '1st'
                    if counter == 2: count_string = '2nd'
                    if counter == 3: count_string = '3rd'
                    grid[i][j] = Room(id=counter, name=f"The {count_string} Room", description=f"""This is the description for the {count_string} room, the {count_string} description written.""")
                    counter += 1
                    # Update description generator once map generator is tested and proves working
            return grid

        from random import randint

        def mapGenerator():
            grid = fillGrid()
            for y, row in enumerate(grid):
                for x, room in enumerate(row):
                    directions = ['n', 's', 'e', 'w']
                    connected = False
                    if y - 1 < 0: directions.remove('n')
                    if y + 1 > len(grid) - 1: directions.remove('s')
                    if x + 1 > len(row) - 1: directions.remove('e')
                    if x - 1 < 0: directions.remove('w')
                    while not connected:
                        for direction in directions:
                            opposite = ''
                            if direction == 'n': 
                                opposite = 's'
                                conn_room = grid[y - 1][x]
                            if direction == 's':
                                opposite = 'n'
                                conn_room = grid[y + 1][x]
                            if direction == 'e':
                                opposite = 'w'
                                conn_room = grid[y][x + 1]
                            if direction == 'w':
                                opposite = 'e'
                                conn_room = grid[y][x - 1]
                            toConnect = randint(0, 1)
                            if toConnect:
                                room.connect_rooms(conn_room, direction)
                                conn_room.connect_rooms(room, opposite)
                                connected = True
            return grid
        self.grid = mapGenerator()

    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        for row in self.grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)


w = World()
num_rooms = 44
width = 8
height = 7
w.generate_rooms(width, height, num_rooms)
w.print_rooms()


print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
