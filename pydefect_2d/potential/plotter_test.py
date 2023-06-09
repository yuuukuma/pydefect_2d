# -*- coding: utf-8 -*-
#  Copyright (c) 2023 Kumagai group.
import numpy as np
from matplotlib import pyplot as plt

from pydefect_2d.potential.epsilon_distribution import EpsilonDistribution, \
    EpsilonGaussianDistribution
from pydefect_2d.potential.grids import Grid, Grids
from pydefect_2d.potential.plotter import ProfilePlotter
from pydefect_2d.potential.slab_model_info import GaussChargePotential, \
    FP1dPotential, SlabModel, GaussChargeModel


def test_plot_profile():
    grid_plot = Grid(10.0, 10)
    electronic_eps = np.array(
        [[1.0, 1.0, 1.0, 1.5, 2.0, 2.0, 2.0, 1.5, 1.0, 1.0],
         [1.0, 1.0, 1.0, 2.5, 4.0, 4.0, 4.0, 2.5, 1.0, 1.0],
         [1.0, 1.0, 1.0, 3.5, 6.0, 6.0, 6.0, 3.5, 1.0, 1.0]])
    ionic_eps = np.array([[0.0, 0.0, 0.0, 0.5, 1.0, 1.0, 1.0, 0.5, 0.0, 0.0],
                          [0.0, 0.0, 0.0, 1.5, 3.0, 3.0, 3.0, 1.5, 0.0, 0.0],
                          [0.0, 0.0, 0.0, 2.5, 5.0, 5.0, 5.0, 2.5, 0.0, 0.0]])

    epsilon = EpsilonGaussianDistribution(grid=grid_plot,
                                          ave_electronic_epsilon=[2.]*3,
                                          ave_ionic_epsilon=[3.]*3,
                                          center=5.0,
                                          sigma=1.0)
    grid_xy = Grid(1.0, 2)
    charges = [0.0, 1.0, 2.0, 4.0, 2.0, 1.0, 0.0, 0.0, 0.0, 0.0]
    charge = GaussChargeModel(grids=Grids([grid_xy, grid_xy, grid_plot]),
                              sigma=1.0,
                              defect_z_pos=0.0,
                              epsilon_x=epsilon.static[0],
                              epsilon_y=epsilon.static[1],
                              charges=np.array([[charges]*2]*2))
    pot = [-1.0, 1.0, 2.0, 4.0, 2.0, 1.0, -1.0, -2.0, -3.0, -2.0]
    potential = GaussChargePotential(
        grids=Grids([grid_xy, grid_xy, grid_plot]),
        potential=np.array([[pot]*2]*2))

    fp_pot = FP1dPotential(grid_plot, [-1.5, 1.5, 2.5, 4.5, 2.5, 1.5, -1.5, -2.5, -3.5, -1.5])

    slab_model = SlabModel(1, epsilon, charge, potential, fp_pot)
    plotter = ProfilePlotter(plt, slab_model)
    plotter.plt.show()