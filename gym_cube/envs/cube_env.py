import gym
from gym import spaces

import numpy as np
import cube

solved_cube = Cube().boxes

class CubeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, cube):
        super(CubeEnv, self).__init__()

        self.cube = cube
        cube.scramble(n = 20)
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
        print(self.cube.machine_output())

    def _get_reward(self):
        # 5 points for each solved face
        reward = 5 * (
            np.unique(self.cube.front_face).size +
            np.unique(self.cube.back_face).size +
            np.unique(self.cube.top_face).size +
            np.unique(self.cube.bottom_face).size +
            np.unique(self.cube.right_face).size +
            np.unique(self.cube.left_face).size
        )
        return reward