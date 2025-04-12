import numpy as np

from kliff.dataset.dataset import Configuration
from kliff.neighbor import NeighborList

target_coords = np.asarray(
    [
        [0.000000e00, 0.000000e00, 0.000000e00],
        [1.234160e00, 7.125400e-01, 0.000000e00],
        [0.000000e00, 0.000000e00, 3.355150e00],
        [1.234160e00, 7.125400e-01, 3.355150e00],
        [-2.468323e00, -1.425090e00, 0.000000e00],
        [-2.468323e00, -1.425090e00, 3.355150e00],
        [-1.234162e00, 7.125400e-01, 0.000000e00],
        [-1.234162e00, 7.125400e-01, 3.355150e00],
        [-1.000000e-06, -1.425090e00, 0.000000e00],
        [-1.000000e-06, -1.425090e00, 3.355150e00],
        [1.234161e00, 2.137630e00, 0.000000e00],
        [1.234161e00, 2.137630e00, 3.355150e00],
        [2.468322e00, 0.000000e00, 0.000000e00],
        [2.468322e00, 0.000000e00, 3.355150e00],
        [3.702483e00, 2.137630e00, 0.000000e00],
        [3.702483e00, 2.137630e00, 3.355150e00],
    ]
)

target_species = ["C"] * 16
target_species[0] = "O"
target_species[10] = "O"
target_species[12] = "O"
target_species[14] = "O"

all_indices = [[6, 1, 8], [0, 10, 12], [7, 3, 9], [2, 11, 13]]
all_numneigh = [len(i) for i in all_indices]


def test_neigh(test_data_dir):
    conf = Configuration.from_file(
        test_data_dir / "configs/bilayer_graphene/bilayer_sep3.36_i0_j0.xyz"
    )
    conf.species[0] = "O"

    neigh = NeighborList(conf, infl_dist=2, padding_need_neigh=False)
    coords = neigh.get_coords()
    species = neigh.get_species()

    assert np.allclose(coords, target_coords)
    assert np.array_equal(species, target_species)

    # contributing
    for i in range(conf.get_num_atoms()):
        nei_indices, nei_coords, nei_species = neigh.get_neigh(i)
        assert np.allclose(nei_indices, all_indices[i])

    # padding
    for i in range(conf.get_num_atoms(), len(coords)):
        nei_indices, nei_coords, nei_species = neigh.get_neigh(i)
        assert nei_indices.size == 0
        assert nei_coords.size == 0
        assert nei_species.size == 0

    numneigh, neighlist = neigh.get_numneigh_and_neighlist_1D(request_padding=False)
    np.array_equal(numneigh, all_numneigh)
    np.array_equal(neighlist, np.concatenate(all_indices))


def test_1D():
    """
    Simple test of a dimer, non-periodic.
    """

    cell = np.asarray([[200.0, 0.0, 0.0], [0.0, 200.0, 0.0], [0.0, 0.0, 200.0]])
    coords = np.asarray([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]])
    species = ["C", "O"]

    for P in [True, False]:
        atoms = Configuration(
            cell=cell,
            species=species,
            coords=coords,
            PBC=[P] * 3,
        )

        neigh = NeighborList(atoms, infl_dist=5.0)

        # atom 0
        idx = 0
        nei_idx = 1
        neighbors, neighbor_xyz, neighbor_species = neigh.get_neigh(idx)
        assert np.allclose(neighbors, [nei_idx])
        assert np.allclose(neighbor_xyz, [coords[nei_idx]])
        assert neighbor_species == [species[nei_idx]]

        # atom 1
        idx = 1
        nei_idx = 0
        neighbors, neighbor_xyz, neighbor_species = neigh.get_neigh(idx)
        assert np.allclose(neighbors, [nei_idx])
        assert np.allclose(neighbor_xyz, [coords[nei_idx]])
        assert neighbor_species == [species[nei_idx]]
