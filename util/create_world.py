from django.contrib.auth.models import User
from adventure.models import Player, Room


Room.objects.all().delete()

def fillGrid():
    grid = [[None] * 10 for x in range(10)]
    counter = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            count_string = f'{counter}th'
            if counter == 1: count_string = '1st'
            if counter == 2: count_string = '2nd'
            if counter == 3: count_string = '3rd'
            grid[i][j] = Room(title=f"The {count_string} Room", description=f"""This is the description for the {count_string} room, the {count_string} description written.""")
            grid[i][j].save()
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
                        room.connectRooms(conn_room, direction)
                        conn_room.connectRooms(room, opposite)
                        connected = True
    return grid[0][0]

first_room = mapGenerator()

players=Player.objects.all()
for p in players:
    p.currentRoom=first_room.id
    p.save()
