# -*- coding: utf-8 -*-
#  Copyright (c) 2023 Kumagai group.
import pytest
from pymatgen.core import Lattice, IStructure


@pytest.fixture(scope="session")
def single_BN():
    return IStructure.from_str("""B1 N1
1.0
   2.5127640010    0.0000000000    0.0000000000
  -1.2563820005    2.1761174586    0.0000000000
   0.0000000000    0.0000000000   10.0000000000
B N
1 1
direct
   0.0000000000    0.0000000000    0.5000000000 B
   0.3333333333    0.6666666667    0.5000000000 N""", fmt="poscar")


@pytest.fixture(scope="session")
def single_BN_2x2():
    return IStructure.from_str("""B4 N4
1.0
   5.0255280019999997    0.0000000000000000    0.0000000000000000
  -2.5127640009999999    4.3522349171999997    0.0000000000000000
   0.0000000000000000    0.0000000000000000   10.0000000000000000
B N
4 4
direct
   0.0000000000000000    0.0000000000000000    0.5000000000000000 B
   0.0000000000000000    0.5000000000000000    0.5000000000000000 B
   0.4999999999999999    0.0000000000000000    0.5000000000000000 B
   0.4999999999999999    0.5000000000000000    0.5000000000000000 B
   0.1666666666500000    0.3333333333500000    0.5000000000000000 N
   0.1666666666499999    0.8333333333499999    0.5000000000000000 N
   0.6666666666500000    0.3333333333500000    0.5000000000000000 N
   0.6666666666499999    0.8333333333499999    0.5000000000000000 N""",
                               fmt="poscar")