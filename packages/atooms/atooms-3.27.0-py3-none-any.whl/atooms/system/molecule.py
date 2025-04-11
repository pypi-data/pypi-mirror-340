import re
import copy
import numpy
from atooms.system.particle import Particle, cm_position, _periodic_vector_unfolded

# For the network models, like Keating, it does not make much sense to
# use Molecule actually: the system would be one big molecule. One
# could just abuse of the NeighborList so that it does not get updated
# during the simulation! This would also allow bond switches.

class Molecule:

    def __init__(self, particle, bond, angle=None, species=None, cell=None):
        # For consistency with System, we use singular names for variables:
        # particle, bond, etc.
        self.particle = copy.deepcopy(particle)
        self.bond = bond
        if angle is None:
            angle = []
        self.angle = angle
        self.dihedral = []
        self.improper = []
        self.species = species
        if species is None:
            self.species = self._default_species()
        self.cell = cell
        # Fold particles in cell when using PBCs
        if self.cell:
            for p in self.particle:
                p.fold(self.cell)

    def _default_species(self):
        return ''.join([str(p.species) for p in self.particle])

    @property
    def center_of_mass_unfolded(self):
        from atooms.system.particle import cm
        # This is a reliable way to determine the molecule CM
        assert hasattr(self.particle[0], 'position_unfolded')
        return cm(self.particle, 'position_unfolded')
    
    @property
    def center_of_mass(self):
        if self.cell is None:
            return cm_position(self.particle)
        particle = [self.particle[0].nearest_image_of(p, self.cell) for p in self.particle]
        cm = cm_position(particle)
        cm = _periodic_vector_unfolded(cm, self.cell.side)
        return cm

    @center_of_mass.setter
    def center_of_mass(self, position):
        position = numpy.array(position)
        cm = self.center_of_mass
        for p in self.particle:
            p.position += (position - cm)
        if self.cell:
            for p in self.particle:
                p.fold(self.cell)

    @property
    def orientation(self):
        """
        Get the current orientation of the particles in the molecule.

        The orientation is calculated as the displacement vectors of each particle
        relative to the center of mass. The calculation takes into account periodic boundaries
        if the cell information is provided.

        Returns:
            numpy.ndarray: An array of vectors representing the orientation of each particle
            relative to the center of mass.
        """
        o = []
        cm = self.center_of_mass
        for p in self.particle:
            rij = p.position - cm
            if self.cell:
                rij = _periodic_vector_unfolded(rij, self.cell.side)
            o.append(rij)
        return numpy.array(o)

    @orientation.setter
    def orientation(self, value):
        """
        Set the new orientation of the particles in the molecule.

        This method updates the positions of the particles by adding the provided
        orientation vectors to the current center of mass. The number of elements in
        the `value` must match the number of particles in the molecule.

        Args:
            value (numpy.ndarray): An array of new orientation vectors for each particle.
        """
        assert len(value) == len(self.particle), 'the number of orientations must match the number of particles'
        cm = self.center_of_mass
        for p, o in zip(self.particle, value):
            p.position[:] = cm + o

    def rotate(self, theta, axis=None):
        """
        Rotate the molecule by `theta`, around the given `axis` in 3D

        In 2D, the method applies a 2D rotation matrix to the molecule's orientation using
        the provided angle `theta`. The rotation is counterclockwise in the 2D plane.

        In 3D, the method applies a 3D rotation matrix to the molecule's orientation using
        Rodrigues' rotation formula. The axis of rotation must be provided as a 3D
        vector. The angle `theta` should be in radians.
        """
        if len(self.particle[0].position) == 2:
            self._rotate_2D(theta)
        elif len(self.particle[0].position) == 3:
            assert axis is not None, 'provide axis for rotation'
            self._rotate_3D(theta, axis=axis)
        else:
            raise ValueError('cannot rotate molecules in dimensions other than 2 or 3')

    def _rotate_2D(self, theta):
        """
        Rotate the 2D molecule by a given angle.

        This method applies a 2D rotation matrix to the molecule's orientation using
        the provided angle `theta`. The rotation is counterclockwise in the 2D plane.

        Args:
            theta (float): The angle of rotation in radians.
        """
        rotation_matrix = numpy.array([[numpy.cos(theta), -numpy.sin(theta)],
                                       [numpy.sin(theta), numpy.cos(theta)]])
        self._apply_rotation_matrix(rotation_matrix)

    def _rotate_3D(self, theta, axis):
        """
        Rotate the molecule in 3D by a given angle around a specified axis.

        This method applies a 3D rotation matrix to the molecule's orientation using
        Rodrigues' rotation formula. The axis of rotation must be provided as a 3D
        vector. The angle `theta` should be in radians.

        Args:
            theta (float): The angle of rotation in radians.
            axis (array-like or str): A 3D vector representing the axis of rotation.
            If a string is provided, it must be compatible with `orientation_vector()`
        """
        axis = numpy.array(axis)
        # Since orientation_vector accepts a string now, things are simpler
        # if numpy.issubdtype(axis.dtype, numpy.str_) or numpy.issubdtype(axis.dtype, numpy.object_):
        if isinstance(axis, str):
            axis = self.orientation_vector(axis)
        axis /= numpy.linalg.norm(axis)  # Ensure u is a unit vector

        ux, uy, uz = axis
        cos_theta = numpy.cos(theta)
        sin_theta = numpy.sin(theta)

        # Skew-symmetric cross-product matrix K
        k = numpy.array([[  0,   -uz,   uy],
                         [ uz,    0,  -ux],
                         [-uy,   ux,    0]])

        # Rodrigues' formula: R = I + sin(theta) * K + (1 - cos(theta)) * K^2
        rotation_matrix = numpy.eye(3) + sin_theta * k + (1 - cos_theta) * numpy.dot(k, k)
        self._apply_rotation_matrix(rotation_matrix)

    def _apply_rotation_matrix(self, rotation_matrix):
        """
        Apply a rotation matrix to the molecule's orientation.

        This method updates the molecule's orientation by applying the provided
        rotation matrix. The new orientation is calculated by multiplying the current
        orientation by the transpose of the rotation matrix.

        Args:
            rotation_matrix (numpy.ndarray): A 2x2 or 3x3 rotation matrix to apply to the orientation.
        """
        self.orientation = numpy.dot(self.orientation, rotation_matrix.T)

    def orientation_vector(self, orientation, normed=False):
        """
        Compute the orientation vector based on `orientation` string.
        Orientation strings can be :
        - `etoe` (end-to-end),
        - 'i-j' (vector from particle `i` to `j`, or `CM`, `i`, `j` from 1 to N)
        - 'i-jxk-l' (cross product of two vectors)

        Args:
            orientation: string specifying the orientation vector.
            normed (bool): orientation becomes unitary if True
        Returns:
            numpy.ndarray: Array of orientation vector.
        """
        s = orientation
        # TODO: eat these delicious spaghetti
        if s in ['etoe', 'end-to-end', 'e2e']:
            rij = self._extract_endtoend()
        else:
            rij = self._check_and_extract_vector(s)
            if rij is None:
                rij = self._check_and_extract_cross_product(s)
                if rij is None:
                    raise ValueError(f"Error: {s} is not a valid orientation")
            if self.cell:
                rij = _periodic_vector_unfolded(rij, self.cell.side)
        if normed:
            rij /= numpy.linalg.norm(rij)
        return numpy.array(rij)

    def custom_orientation(self, orientation, normed=False):
        """
        Compute the molecule orientation based on custom `orientation` strings.
        Orientation strings must be compatible with `orientation_vector`.

        Args:
            orientation (list): List of strings specifying the orientation vectors.
            normed (bool): orientation becomes unitary if True
        Returns:
            numpy.ndarray: Array of orientation vectors.
        """
        o = []
        for s in orientation:
            o.append(self.orientation_vector(s, normed))
        return numpy.array(o)

    def _extract_endtoend(self):
        """
        Check if the string specifies an end-to-end orientation and extract the vector.

        Args:
            s (str): Orientation string.

        Returns:
            numpy.ndarray or None: End-to-end vector if applicable, otherwise None.
        """
        def _unfold(particle, side):
            L = side
            old = particle[0].position.copy()
            new_pos = [old.copy()]
            for p in particle[1:]:
                pos = p.position.copy()
                dif = pos - old
                dif = dif - numpy.rint(dif / L) * L
                old += dif
                new_pos.append(old.copy())
            return new_pos[-1]

        if self.cell:
            last = _unfold(self.particle, self.cell.side)
        else:
            last = self.particle[-1].position
        rij = last - self.particle[0].position
        return rij

    def _check_and_extract_vector(self, s):
        """
        Check if the string specifies a vector orientation and extract the vector.

        Args:
            s (str): Orientation string.

        Returns:
            numpy.ndarray or None: Vector if applicable, otherwise None.
        """
        M = len(str(len(self.particle)))
        string_to_match = rf"^(CM|\d{{1,{M}}})-(CM|\d{{1,{M}}})$"
        pattern = re.compile(string_to_match)
        match = pattern.match(s)
        if match:
            x, y = match.groups()
            return self._get_vector(x, y)
        return None

    def _check_and_extract_cross_product(self, s):
        """
        Check if the string specifies a cross product orientation and extract the vector.

        Args:
            s (str): Orientation string.

        Returns:
            numpy.ndarray or None: Cross product vector if applicable, otherwise None.
        """
        M = len(str(len(self.particle)))
        string_to_match = rf"^(CM|\d{{1,{M}}})-(CM|\d{{1,{M}}})x(CM|\d{{1,{M}}})-(CM|\d{{1,{M}}})$"
        pattern = re.compile(string_to_match)
        match = pattern.match(s)
        if match:
            x, y, w, z = match.groups()
            vector_1 = self._get_vector(x, y)
            vector_2 = self._get_vector(w, z)
            cross_product = numpy.cross(vector_1, vector_2)
            if numpy.linalg.norm(cross_product) == 0:
                raise ValueError(f"Error: the cross product of {s} is zero. The orientation is not defined.")
            return cross_product
        return None

    def _get_vector(self, x, y):
        """
        Get the vector between two points specified by their indices or 'CM' (center of mass).

        Args:
            x (str): Index of the first point or 'CM' for center of mass.
            y (str): Index of the second point or 'CM' for center of mass.

        Returns:
            numpy.ndarray: Vector from point x to point y.

        Raises:
            ValueError: If x or y are not valid particle indices or 'CM'.
        """
        def get_position(index):
            return self.center_of_mass if index == "CM" else self.particle[int(index)-1].position

        try:
            position_x = get_position(x)
            position_y = get_position(y)
            return position_y - position_x
        except (ValueError, IndexError):
            raise ValueError(f"Error: {x if not x.isdigit() or int(x) >= self.len_molecule else y} is not a valid particle index,"
                             "ie 'CM' or an integer between 1 and {self.len_molecule}")
