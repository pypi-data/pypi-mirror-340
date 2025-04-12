import warnings
from collections import OrderedDict

import numpy as np

from kliff.models.parameter import Parameter, ParameterError
from kliff.transforms.parameter_transforms import LogParameterTransform


def test_parameter():
    # scalar
    try:
        p = Parameter(1.1)
    except ParameterError:
        pass

    # 2D array
    try:
        p = Parameter([[1.1]])
        # ideally 2D array should be numpy array
        # but this is permitted for backward compatibility
    except ParameterError:
        pass

    p = Parameter(np.asarray([2.2, 3.3]), index=0, opt_mask=np.array([True, True]))
    # without the opt mask there is nothing to report bounds on,
    # as bounds is same shape as masked opt params
    assert np.allclose(p, [2.2, 3.3])
    # TODO: appropriate tests for fixed, lower_bound, upper_bound
    # assert p.fixed == [False, False]
    assert (p.lower_bound == np.asarray([None, None])).all()
    assert (p.upper_bound == np.asarray([None, None])).all()
    assert p.name is None
    assert len(p) == 2
    assert p[0] == 2.2
    assert p[1] == 3.3
    assert p.name is None
    assert len(p) == 2
    assert p[0] == 2.2
    assert p[1] == 3.3

    p[0] = 4.4
    assert np.allclose(p, [4.4, 3.3])
    # p.set_fixed(0, True)
    # assert p.fixed == [True, False]
    # not sure if this is necessary
    p.add_bounds_model_space(np.array([[1.1, None], [5.5, None]]))
    assert p.bounds[0].tolist() == [1.1, None]
    assert p.bounds[1].tolist() == [5.5, None]

    # as dict and from dict
    # d = {
    #     "@module": p.__class__.__module__,
    #     "@class": p.__class__.__name__,
    #     "value": [4.4, 3.3],
    #     "fixed": [True, False],
    #     "lower_bound": [1.1, None],
    #     "upper_bound": [5.5, None],
    #     "name": None,
    #     "index": 0,
    # }
    d = {
        "@module": p.__class__.__module__,
        "@class": p.__class__.__name__,
        "@value": [4.4, 3.3],  # internal container value for safekeeping state
        "name": None,
        "transform_function": None,
        "bounds": np.array([[1.1, None], [5.5, None]], dtype=object),
        "index": 0,
        "_is_transformed": False,
        "opt_mask": np.array([True, True]),
        "_bounds_transformed": False,
    }

    for items_p, items_d in zip(
        OrderedDict(sorted(p.as_dict().items())), OrderedDict(sorted(d.items()))
    ):
        if type(items_d) == np.ndarray:
            assert np.allclose(items_p, items_d)
        assert items_p == items_d

    p1 = Parameter.from_dict(d)
    assert np.allclose(p1, p)
    # assert p1.fixed == p.fixed
    assert (p1.lower_bound == p.lower_bound).all()
    assert (p1.upper_bound == p.upper_bound).all()
    assert p1.name == p.name


def create_all_possible_input(v):
    inp = []
    for ud in ["default", v + 0.01]:
        inp.append([ud])
        inp.append([ud, "fix"])
        for lb in [None, v - 0.1]:
            for ub in [None, v + 0.1]:
                inp.append([ud, lb, ub])
    return inp


# TODO: appropriate tests for mutable parameters
# def test_optimizing_parameter():
#     # model params
#     p1 = np.array([1.1])
#     p2 = np.array([2.2, 3.3])
#     names = ["p1", "p2"]
#     mp = {
#         names[0]: Parameter(p1, name=names[0], index=0),
#         names[1]: Parameter(p2, name=names[1], index=1)
#     }
#     # op = Parameter(mp)
#
#     # fitting params
#     with warnings.catch_warnings():  # context manager to ignore warning
#         warnings.simplefilter("ignore")
#
#         v0 = p1[0]
#         inp0 = create_all_possible_input(v0)
#         v1 = p2[0]
#         inp1 = create_all_possible_input(v1)
#         v2 = p2[1]
#         inp2 = create_all_possible_input(v2)
#         for i in inp0:
#             for j in inp1:
#                 for k in inp2:
#                     op.set(p1=[i])
#                     op.set_one("p2", [j, k])
#
#     assert op.get_num_opt_params() == 3
#     a = op.get_opt_params()
#     assert np.allclose(op.get_opt_params(), [1.11, 2.21, 3.31])
#
#     # interface to optimizer
#     # restore to default parameter values
#     x0 = np.concatenate((p1, p2))
#     op.update_opt_params(x0)
#
#     assert np.array_equal(op.get_opt_params(), x0)
#
#     for i in range(3):
#         n, v, p, c = op.get_opt_param_name_value_and_indices(i)
#         assert v == x0[i]
#         if i == 0:
#             assert n == "p1"
#             assert p == 0
#             assert c == 0
#         else:
#             assert n == "p2"
#             assert p == 1
#             assert c == (i - 1) % 2
#
#     bounds = [[i - 0.1, i + 0.1] for i in x0]
#     assert np.array_equal(op.get_opt_params_bounds(), bounds)
#     assert op.opt_params_has_bounds() == True
#
#     import sys
#
#     op.echo_opt_params(filename=sys.stdout)
