import os
import unittest

try:
    import h5py
    from atooms.trajectory import TrajectoryHDF5
    from atooms.system import System, Cell, Particle, Interaction
    from atooms.trajectory.hdf5 import _CutOff, _PairPotential
    HAS_HDF5 = True
except:
    HAS_HDF5 = False


class Test(unittest.TestCase):

    @unittest.skipIf(not HAS_HDF5, 'no h5py module')
    def test_write_initial_state(self):
        p = [_PairPotential("lennard_jones", {"epsilon": 1.0, "sigma": 1.0},
                            [1, 1], _CutOff("CS", 2.5))]
        i = [Interaction()]
        i[0].name = "atomic"
        i[0].potential = p
        s = System()
        s.particle = [Particle(position=[1.0, 1.0, 1.0],
                               velocity=[0.0, 0.0, 0.0])]
        s.cell = Cell([1.0, 1.0, 1.0])
        with TrajectoryHDF5('/tmp/test_hdf5.h5', 'w') as t:
            t.write_interaction(i)
            t.write(s, 0)

        with TrajectoryHDF5('/tmp/test_hdf5.h5', 'r') as t:
            i = t.read_interaction()
            s = t[0]

    @unittest.skipIf(not HAS_HDF5, 'no h5py module')
    def test_strings(self):
        import numpy
        with h5py.File('/tmp/test_hdf5.h5', 'w') as fh:
            # fh['test'] = ['hello']  # this will fail with python3
            fh['test'] = [b'hello']
        with h5py.File('/tmp/test_hdf5.h5', 'r') as fh:
            self.assertEqual(fh['test'][0].decode(), 'hello')

    def tearDown(self):
        os.remove('/tmp/test_hdf5.h5')


if __name__ == '__main__':
    unittest.main()
