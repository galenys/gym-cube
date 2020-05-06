import gym
from gym import spaces

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
                face[y][x] = COLOR_DICT[self.boxes[z][y][x].front]
        return face
    def back_face(self):
        face = np.zeros([3, 3])
        z = 2
        for y in range(3):
            for x in range(3):
                face[y][x] = COLOR_DICT[self.boxes[z][y][x].back]
        return face
    def top_face(self):
        face = np.zeros([3, 3])
        y = 0
        for z in range(3):
            for x in range(3):
                face[z][x] = COLOR_DICT[self.boxes[z][y][x].top]
        return face
    def bottom_face(self):
        face = np.zeros([3, 3])
        y = 2
        for z in range(3):
            for x in range(3):
                face[z][x] = COLOR_DICT[self.boxes[z][y][x].bottom]
        return face
    def right_face(self):
        face = np.zeros([3, 3])
        x = 2
        for y in range(3):
            for z in range(3):
                face[y][z] = COLOR_DICT[self.boxes[z][y][x].right]
        return face
    def left_face(self):
        face = np.zeros([3, 3])
        x = 0
        for y in range(3):
            for z in range(3):
                face[y][z] = COLOR_DICT[self.boxes[z][y][x].left]
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




class CubeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(CubeEnv, self).__init__()

        self.cube = Cube()
        self.cube.scramble(n = 20)
        self.current_step = 0

        # F, B, T, D, R, L and counterparts
        self.action_space = spaces.Discrete(12)

        # 3X3 blocks per face * 6 faces, 6 possible colors
        # faces are in order F, B, T, D, R, L
        observation_low = np.zeros([3, 18])
        observation_high = np.ones([3, 18]) * 5
        self.observation_space = spaces.Box(observation_low, 
                                            observation_high)
    
    def step(self, action):
        self.current_step += 1

        # F
        if action == 0:
            self.cube.rot_z(layer=0)
        # F'
        elif action == 1:
            for i in range(3):
                self.cube.rot_z(layer=0)
        # B
        elif action == 2:
            for i in range(3):
                self.cube.rot_z(layer=2)
        # B'
        elif action == 3:
            self.cube.rot_z(layer=2)
        
        # T
        elif action == 4:
            self.cube.rot_y(layer=0)
        # T'
        elif action == 5:
            for i in range(3):
                self.cube.rot_y(layer=0)
        # D
        elif action == 6:
            for i in range(3):
                self.cube.rot_z(layer=2)
        # D'
        elif action == 7:
            self.cube.rot_z(layer=2)
        
        # R
        elif action == 8:
            self.cube.rot_x(layer=2)
        # R'
        elif action == 9:
            for i in range(3):
                self.cube.rot_x(layer=2)
        # L
        elif action == 10:
            for i in range(3):
                self.cube.rot_x(layer=0)
        # L'
        elif action == 11:
            self.cube.rot_x(layer=0)

        obs = self.cube.machine_output()
        reward = self._get_reward()
        done = (
            reward == 5 * 6
            # or self.current_step >= 1e5
        )
        
        return obs, reward, done, {}

    def reset(self):
        self.current_step = 0
        self.cube.reset()

    def render(self):
        # temporary render, eventually 3D display
        print("MACHINE OUTPUT")
        print(self.cube.machine_output())

    def _get_reward(self):
        # 5 points for each solved face
        reward = 5 * (
            np.unique(self.cube.front_face()).size == 1 +
            np.unique(self.cube.back_face()).size == 1 +
            np.unique(self.cube.top_face()).size == 1 +
            np.unique(self.cube.bottom_face()).size == 1 +
            np.unique(self.cube.right_face()).size == 1 +
            np.unique(self.cube.left_face()).size == 1
        )
        return reward