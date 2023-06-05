# -*- coding: utf-8 -*-
#  Copyright (c) 2023 Kumagai group.
from dataclasses import dataclass
from functools import cached_property
from typing import List

import numpy as np
from monty.json import MSONable
from numpy import linspace
from numpy.testing import assert_array_almost_equal, assert_almost_equal
from scipy.fftpack import fft
from tabulate import tabulate
from vise.util.mix_in import ToJsonFileMixIn

from pydefect_2d.potential.distribution import make_gaussian_distribution, \
    rescale_distribution


@dataclass
class Grid(MSONable):
    base_length: float  # in Å
    base_num_grid: int
    mul: int = 1

    @property
    def length(self):
        return self.base_length * self.mul

    @property
    def num_grid(self):
        return self.base_num_grid * self.mul

    @property
    def grid_points(self):
        return list(linspace(0, self.length, self.num_grid, endpoint=False))


@dataclass
class EpsilonDistribution(MSONable, ToJsonFileMixIn):
    grid: Grid
    electronic: List[List[float]]  # [epsilon_x, epsilon_y, epsilon_z]
    ionic: List[List[float]]  # [epsilon_x, epsilon_y, epsilon_z]

    def __eq__(self, other):
        try:
            assert self.grid == other.grid
            assert_almost_equal(self.electronic, other.electronic)
            assert_almost_equal(self.ionic, other.ionic)
        except AssertionError:
            return False
        return True

    @property
    def ion_clamped(self) -> List[List[float]]:
        return list(np.array(self.electronic) + 1.)

    @property
    def static(self):
        return list(np.array(self.ion_clamped) + np.array(self.ionic))

    @property
    def effective(self):
        clamped = np.array(self.ion_clamped)
        ionic = np.array(self.ionic)
        return list(clamped + clamped**2/ionic)

    @property
    def ave_ele(self) -> np.array:
        return np.array(self.electronic).mean(axis=1)

    @property
    def ave_ion(self) -> np.array:
        return np.array(self.ionic).mean(axis=1)

    def __str__(self):
        result = []
        header = ["pos (Å)"]
        for e in ["ε_inf", "ε_ion", "ε_0"]:
            for direction in ["x", "y", "z"]:
                header.append(f"{e}_{direction}")
        list_ = []
        for i, pos in enumerate(self.grid.grid_points):
            list_.append([pos])
            for e in [self.ion_clamped, self.ionic, self.static]:
#            for e in [self.ion_clamped, self.ionic, self.static, self.effective]:
                list_[-1].extend([e[0][i], e[1][i], e[2][i]])

        result.append(tabulate(list_, tablefmt="plain", floatfmt=".2f",
                               headers=header))

        return "\n".join(result)

    def to_plot(self, plt):
        ax = plt.gca()
        ax.set_ylabel("$\epsilon$ ($\epsilon_{vac}$)")
        for e, direction in zip(self.ion_clamped, ["x", "y", "z"]):
            ax.plot(self.grid.grid_points, e, label=f"ε_inf_{direction}")
        for e, direction in zip(self.ionic, ["x", "y", "z"]):
            ax.plot(self.grid.grid_points, e, label=f"ε_ion_{direction}")
        for e, direction in zip(self.static, ["x", "y", "z"]):
            ax.plot(self.grid.grid_points, e, label=f"ε_0_{direction}")
        ax.legend()

    @cached_property
    def reciprocal_static(self):
        return [fft(e) for e in self.static]


@dataclass
class EpsilonGaussianDistribution(EpsilonDistribution):
    center: float  # in Å
    sigma: float  # in Å

    def __str__(self):
        result = [f"center: {self.center:.2f} Å",
                  f"sigma: {self.sigma:.2f} Å",
                  super().__str__()]
        return "\n".join(result)


def make_epsilon_gaussian_dist(length: float,
                               num_grid: int,
                               ave_electronic_epsilon: List[float],
                               ave_ionic_epsilon: List[float],
                               position: float,
                               sigma: float,
                               mul: int = 1):
    grid = Grid(length, num_grid, mul)
    dist = make_gaussian_distribution(grid.grid_points, position, sigma)
    ave_electronic_epsilon = list(np.array(ave_electronic_epsilon) / mul)
    ave_ionic_epsilon = list(np.array(ave_ionic_epsilon) / mul)

    electronic = [rescale_distribution(dist, ave_ele)
                  for ave_ele in ave_electronic_epsilon]
    ionic = [rescale_distribution(dist, ave_ionic)
             for ave_ionic in ave_ionic_epsilon]
    return EpsilonGaussianDistribution(grid, electronic, ionic, position, sigma)


