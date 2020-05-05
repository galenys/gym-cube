import numpy as np
import random
import copy

COLOR_DICT = {
    "white": 0,
    "yellow": 1,
    "red": 2,
    "orange": 3,
    "green": 4,
    "blue": 5,
}

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
        self.rot_funcs = [
            self.rot_x,
            self.rot_y,
            self.rot_z
        ]

    def reset(self):
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


    # SCRAMBLE METHODS
    def random_move(self):
        flip = random.random()
        if flip > 0.5:
            random.choice(self.rot_funcs)(0)
        else:
            random.choice(self.rot_funcs)(2)
    def scramble(self, n):
        for i in range(n):
            self.random_move()
    # END SCRAMBLE METHODS

    
    # OUT METHODS
    def front_face(self):
        face = np.zeros([3, 3])
        z = 0
        for y in range(3):
            for x in range(3):
                face[y][x] = COLOR_DICT[cube.boxes[z][y][x].front]
        return face
    def back_face(self):
        face = np.zeros([3, 3])
        z = 2
        for y in range(3):
            for x in range(3):
                face[y][x] = COLOR_DICT[cube.boxes[z][y][x].back]
        return face
    def top_face(self):
        face = np.zeros([3, 3])
        y = 0
        for z in range(3):
            for x in range(3):
                face[z][x] = COLOR_DICT[cube.boxes[z][y][x].top]
        return face
    def bottom_face(self):
        face = np.zeros([3, 3])
        y = 2
        for z in range(3):
            for x in range(3):
                face[z][x] = COLOR_DICT[cube.boxes[z][y][x].bottom]
        return face
    def right_face(self):
        face = np.zeros([3, 3])
        x = 2
        for y in range(3):
            for z in range(3):
                face[y][z] = COLOR_DICT[cube.boxes[z][y][x].right]
        return face
    def left_face(self):
        face = np.zeros([3, 3])
        x = 0
        for y in range(3):
            for z in range(3):
                face[y][z] = COLOR_DICT[cube.boxes[z][y][x].left]
        return face
    
    def machine_output(self):
        return np.concatenate((
            self.front_face(),
            self.back_face(),
            self.top_face(),
            self.bottom_face(),
            self.right_face(),
            self.left_face()
        ), axis=1)
    # END OUT METHODS