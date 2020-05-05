import copy

class Box:
    def __init__(self):
        self.top = 'none'
        self.bottom = 'none'
        self.right = 'none'
        self.left = 'none'
        self.front = 'none'
        self.back = 'none'

class Cube:
    def __init__(self):
        self.reset()

    def reset():
        self.boxes = [[[Box() for i in range(3)] for i in range(3)] for i in range(3)]

        for z in range(3):
            for y in range(3):
                for x in range(3):
                    if z == 0:
                        self.boxes[z][y][x].front = 'white'
                    if z == 2:
                        self.boxes[z][y][x].back = 'yellow'
                    
                    if y == 0:
                        self.boxes[z][y][x].top = 'red'
                    if y == 2:
                        self.boxes[z][y][x].bottom = 'orange'

                    if x == 0:
                        self.boxes[z][y][x].left = 'blue'
                    if x == 2:
                        self.boxes[z][y][x].right = 'green'

    # ROTATION METHODS
    def rot_z(self, layer):
        new_state = copy.deepcopy(self.boxes)
        for y in range(3):
            for x in range(3):
                target = self.boxes[layer][2-x][y]

                new_state[layer][y][x].top = target.left
                new_state[layer][y][x].right = target.top
                new_state[layer][y][x].bottom = target.right
                new_state[layer][y][x].left = target.bottom
        self.boxes = new_state

    def rot_y(self, layer):
        new_state = copy.deepcopy(self.boxes)
        for z in range(3):
            for x in range(3):
                target = self.boxes[x][layer][2-z]

                new_state[z][layer][x].front = target.right
                new_state[z][layer][x].left = target.front
                new_state[z][layer][x].back = target.left
                new_state[z][layer][x].right = target.back
        self.boxes = new_state

    def rot_x(self, layer):
        new_state = copy.deepcopy(self.boxes)
        for z in range(3):
            for y in range(3):
                target = self.boxes[y][2-z][layer]

                new_state[z][y][layer].top = target.front
                new_state[z][y][layer].back = target.top
                new_state[z][y][layer].bottom = target.back
                new_state[z][y][layer].front = target.bottom
        self.boxes = new_state
    # END ROTATION METHODS
    
    # FACE METHODS
    def print_front(self):
        z = 0
        for y in range(3):
            for x in range(3):
                print(cube.boxes[z][y][x].front, end=" ")
            print("")
    def print_back(self):
        z = 2
        for y in range(3):
            for x in range(3):
                print(cube.boxes[z][y][x].back, end=" ")
            print("")
    def print_top(self):
        y = 0
        for z in range(3):
            for x in range(3):
                print(cube.boxes[z][y][x].top, end=" ")
            print("")
    def print_bottom(self):
        y = 2
        for z in range(3):
            for x in range(3):
                print(cube.boxes[z][y][x].bottom, end=" ")
            print("")
    def print_left(self):
        x = 0
        for y in range(3):
            for z in range(3):
                print(cube.boxes[z][y][x].left, end=" ")
            print("")
    def print_right(self):
        x = 2
        for y in range(3):
            for z in range(3):
                print(cube.boxes[z][y][x].right, end=" ")
            print("")
    # END FACE METHODS


cube = Cube()
# r
cube.rot_x(layer=2)


print("FRONT")
cube.print_front()
print("BACK")
cube.print_back()

print("TOP")
cube.print_top()
print("BOTTOM")
cube.print_bottom()

print("LEFT")
cube.print_left()
print("RIGHT")
cube.print_right()