import numpy as np
from copy import deepcopy


class FakeSparse():
    def __init__(self, array):
        self.array = array
    
    def __prod__(self, other):
        self.array = self.array * other

    def toarray(self):
        return self.array

class Geometry():
    def __init__(self):
        self.cell = None
        self.rcell = None
        self.xyz = None
        self.sc_off = None
        
    @property
    def nsc(self):
        class asd:
            def __init__(self, asdasd):
                self.sc_off = asdasd.sc_off
            def prod(self):
                return len(self.sc_off)
        asd = asd(self)
        return asd

    def sc_index(self, idx):
        return np.where((idx == self.sc_off).all(axis=1))[0][0]

class Lattice():
    def __init__(self):
        self.sc_off = None

    def sc_index(self, idx):
        return np.where((idx == self.sc_off).all(axis=1))[0][0]

class Spin():
    def __init__(self):
        self.spin = None

class FakeSislHamiltonian():
    def __init__(self, dat):
        self._spin = dat._spin
        self.na = dat.na
        
        self.H = dat.H
        self.S = dat.S
        self.fermi_level = dat.fermi_level
        
        self.sc_off = dat.sc_off
        self.xyz = dat.xyz[1:,1:]
        self.cell = dat.cell[1:,1:]
        self.rcell = dat.cell[1:,1:]

        self.geometry = Geometry()
        self.geometry.sc_off = self.sc_off
        self.geometry.cell = self.cell
        self.lattice = Lattice()
        self.lattice.sc_off = self.sc_off

        self.spin = Spin()
        self.spin.kind = self._spin


    @property
    def no(self):
        return self.H.shape[-1]
    
    @property
    def S_idx(self):
        return 2
    
    @property
    def n_s(self):
        return len(self.sc_off)

    def tocsr(self, dim=0):
        if dim == 0:
            return FakeSparse(self.H[0].transpose(1,0,2))
        if dim == 1:
            return FakeSparse(self.H[1].transpose(1,0,2))
        if dim == 2:
            return FakeSparse(self.S.transpose(1,0,2))

    def sc_index(self, idx):
        return np.where((idx == self.sc_off).all(axis=1))[0][0]

    def copy(self):
        return deepcopy(self)
    