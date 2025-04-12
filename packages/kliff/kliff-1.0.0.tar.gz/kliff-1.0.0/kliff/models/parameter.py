import pickle
import warnings
from typing import TYPE_CHECKING, List, Tuple, Union

import numpy as np

if TYPE_CHECKING:
    from kliff.transforms.parameter_transforms import ParameterTransform

from loguru import logger


class Parameter(np.ndarray):
    """Parameter class for containing physics-based model parameters.

    This class provides utilities for managing model parameters between the "model space"
    and the "parameter space". See the glossary below for the definition of these spaces.
    Modeled on `torch.nn.Parameters`, it inherits from `numpy.ndarray`. It is a numpy
    array with additional attributes such as name, transform, etc.

    Glossary:
        - Model space: The space in which the model expects the parameters to be in. Currently,
            all models in OpenKIM expect the parameters to be in the affine cartesian space.
        - Parameter space: Parameter space is the space in which you want to sample/optimize
            the parameters. Most often parameters are transformed using bijective transformations
            of the model inputs for ease of optimization/sampling. For example, the log
            transform is used in searching for the optimal parameters of sloppy model parameters.
            There can be cases where transformation functions are not bijective, e.g. ceiling function for
            mapping continuous parameters to discrete values. Parameter space is mostly
            used for optimization, and not the model itself. If no transform_function is
            provided then parameter space and model space are same.

        All functions that needs input/output in the model space, will use the suffix
        `_model_space` and `_param_space` for the transformed parameter space.

        Below is the list of such twinned functions, and their designed use cases:
        1. `get_numpy_array_model_space` and `get_numpy_array_param_space`: These functions
            return the numpy array of parameters in the model space and parameter space.
            These functions should be used for getting the pure numpy array of parameters
            where the ``Parameters`` class might not work, e.g for feeding values to the model.
            They are also used in case of comparing the parameter state etc.
        2. `copy_from_model_space` and `copy_from_param_space`: These functions copy the
            provided array to self in the model space and parameter space. They are useful
            for copying values during optimization etc. NOTE: These functions expect the
            incoming array to be of the same type and shape as self, compensated for opt_mask.
        3. `add_bounds_model_space` and `add_bounds_param_space`: These functions add bounds
            to the parameter in the model space and parameter space.
        4. `get_bounds_model_space` and `get_bounds_param_space`: These functions return the
            bounds in the model space and parameter space.
        5. `get_opt_numpy_array_param_space`: This function returns the numpy array of parameters
            in the parameter space, with the opt_mask applied. This should be the de-facto method
            for getting the numpy array of parameters for optimization. At present, it
            does not have `_model_space` version, as there are no applications for it.
            If needed, it can be added later.

    Attributes:
        name: Name of the parameter.
        transform_function: Instance of  ``ParameterTransform`` object to be applied to the parameter.
        index: Index of the parameter in the parameter vector. used for setting the parameter
            in the KIMPY.
        bounds: Bounds for the parameter, must be numpy array of shape n x 2, with [n,0] as
            lower bound, and [n,1] as the upper bound. If None, no bounds are applied.
        opt_mask: A boolean or boolean array of the same shape as the parameter. For a
            vector parameter ``opt_mask`` acts as a binary mask to determine which vector
            components will be optimized, e.g. for a parameter with value [1., 2., 3.],
            and opt_mask [True, False, True], only the first and third components will be
            optimized, and second one will be presumed constant.
    """

    name: str
    transform_function: "ParameterTransform"
    index: int
    bounds: np.ndarray
    opt_mask: Union[np.ndarray, bool]

    def __new__(
        cls,
        input_array: Union[np.ndarray, float, int],
        name: str = None,
        transform_function: "ParameterTransform" = None,
        bounds: np.ndarray = None,
        index: int = None,
        opt_mask: [np.ndarray, bool] = None,
    ):
        """Initializes and returns a new instance of Parameter.

        Args:
            input_array: Input numpy array to initialize the parameter with.
            name: Name of the parameter
            transform_function: Instance of  ``ParameterTransform`` object to be applied to the parameter.
            bounds: n x 2 array of lower and upper bounds for the parameter. If None, no
                bounds are applied
            index: Index of the parameter in the parameter vector. Used for setting the
             parameter in the KIMPY.
            opt_mask: Boolean array of the same shape as the parameter. The values
                marked ``True`` are optimized, and ``False`` are not optimized. Single
                boolean value can also be provided, in which case it will be applied to
                all the components of the parameter.

        Returns:
            A new instance of Parameter.
        """
        array_in = np.array(input_array)
        obj = array_in.view(cls)
        obj.name = name
        obj.transform_function = transform_function
        obj.index = index
        obj._is_transformed = False
        obj.bounds = bounds
        if opt_mask is not None:
            if isinstance(opt_mask, bool):
                opt_mask = np.ones_like(obj, dtype=bool) * opt_mask
            obj.opt_mask = opt_mask
        else:
            obj.opt_mask = np.zeros(obj.shape, dtype=bool)
        obj._bounds_transformed = False
        return obj

    # TODO: This seems a bit off, the signature should match np.array, need to look more in it
    # but the format matches the one in numpy examples.
    def __array_finalize__(self, obj):
        """Finalizes a parameter, needed for numpy object cleanup."""
        if obj is None:
            return
        self.name = getattr(obj, "name", None)
        self.transform_function = getattr(obj, "transform_function", None)
        self.bounds = getattr(obj, "bounds", None)
        self.index = getattr(obj, "index", None)
        self._is_transformed = getattr(obj, "_is_transformed", False)
        self.opt_mask = getattr(obj, "opt_mask", None)
        self._bounds_transformed = getattr(obj, "_bounds_transformed", False)

    def __repr__(self):
        return f"Parameter {self.name} {np.ndarray.__repr__(self)}."

    def transform(self):
        """Apply the transform to the parameter.

        This method simple applies the function ~:kliff.transforms.ParameterTransform.__call__
        to the parameter (or equivalently, ~:kliff.transforms.ParameterTransform.transform).
        """
        if self._is_transformed:
            # warnings.warn("Parameter {0} has already been transformed.".format(self.name))
            # Warnings become quite noisy, so commenting it out for now.
            # TODO: figure out a better solution for this.
            return
        else:
            if self.transform_function is not None:
                transformed_array = self.transform_function(self)
                self[:] = transformed_array
            self._is_transformed = True

    def inverse_transform(self):
        """Apply the inverse transform to the parameter.

        Simply applies the function :kliff.transforms.ParameterTransform.inverse_transform()
        in place, to the parameters."""
        if not self._is_transformed:
            warnings.warn(f"Parameter {self.name} has not been transformed.")
            return
        else:
            if self.transform_function is not None:
                inv_transformed_array = self.transform_function.inverse_transform(self)
                self[:] = inv_transformed_array
            self._is_transformed = False

    def copy_from_param_space(self, arr: np.ndarray):
        """Copy array to self in the parameter space.

        Array can be a numpy array or a Parameter object.
        This method assumes that the array is of the same type and shape as self,
        compensated for opt_mask. If not, it will raise an error.
        This method also assumes that the incoming array is in the same space, as the parameter
        currently (i.e. "Parameter space", see glossary above for detail).

        Args:
            arr: Array to copy to self.
        """
        # convert to numpy array
        if (not isinstance(arr, (np.ndarray, Parameter))) and isinstance(
            arr, (float, int)
        ):
            arr = np.asarray(arr)

        tmp_arr = np.zeros_like(self)
        tmp_arr[self.opt_mask] = arr
        tmp_arr[~self.opt_mask] = self[~self.opt_mask]
        arr = tmp_arr
        arr = arr.astype(self.dtype)
        self[:] = arr

    def copy_from_model_space(self, arr: np.array):
        """Copy arr from model space.

        Array can be a numpy array or a Parameter object. This method assumes that the
        incoming array is in the model space and would need transformation to the parameter
        space before copying. It is a safer method to use in most cases. If the parameter
        is not transformed, it will transform it first for maintaining consistency.
        This method requires the copied array to have consistent opt_mask applied.

        Args:
            arr: Array to copy to self.
        """
        # ensure that the parameter is transformed
        if not self._is_transformed:
            self.transform()
        if self.transform_function is not None:
            arr = self.transform_function.transform(arr)
        self.copy_from_param_space(arr)

    def get_numpy_array_model_space(self) -> np.ndarray:
        """Get a numpy array of parameters in the model space.

        This method should be uses for getting the numpy array of parameters where the
        ``Parameters`` class might not work, for feeding values to the model.

        Returns:
            A numpy array of parameters in the original space.
        """
        if (self.transform_function is not None) and self._is_transformed:
            return self.transform_function.inverse_transform(self)
        else:
            return np.array(self)

    def get_numpy_array_param_space(self):
        """Applies the transform to the parameter, and returns the transformed array."""
        self.transform()
        return np.array(self)

    def get_opt_numpy_array_param_space(self) -> np.ndarray:
        """Get a masked numpy array of parameters in the transformed space.

        This method is similar to :get_numpy_array_param_space but additionally does apply the
        opt_mask, and returns the array. This ensures the correctness of the array for
        optimization/other applications. *This should be the de-facto method for getting
        the numpy array of parameters.*

        Returns:
            A numpy array of parameters in the original space.
        """
        np_arr = self.get_numpy_array_param_space()  # in transformed space
        if self.opt_mask is not None:
            np_arr = np_arr[self.opt_mask]
        return np_arr

    def copy_at_param_space(
        self, arr: Union[int, float, np.ndarray, List], index: Union[int, List[int]]
    ):
        """Copy values at a particular index or indices in parameter space.

        This method directly copies the provided data, and does not perform any checks.

        Args:
            index: Index or indices to copy the values at.
            arr: Array to copy to self.
        """
        if isinstance(index, int) and isinstance(arr, (int, float)):
            index = [index]
            arr = np.array([arr])
        elif isinstance(index, list) and isinstance(arr, (list, np.ndarray)):
            index = np.array(index)
            arr = np.array(arr)
        elif isinstance(index, np.ndarray) and isinstance(arr, np.ndarray):
            if index.shape != arr.shape:
                raise ParameterError("Index and value are array of different shapes.")
        else:
            raise ParameterError(
                "Either index and value should both be scalar, or both be list/array of same length."
            )

        arr = arr.astype(self.dtype)
        for i, j in zip(index, arr):
            self[i] = j

    def add_transform(self, transform: "ParameterTransform"):
        """Save a transform object with the parameter.

        Args:
            transform: Instance of  ``ParameterTransform`` object to be applied to the parameter.
        """
        self.transform_function = transform
        self.transform()
        self._is_transformed = True
        if self.bounds is not None and not self._bounds_transformed:
            self.bounds = self.transform_function(self.bounds)

    def add_bounds_model_space(self, bounds: np.ndarray):
        """Add bounds to the parameter.

        Bounds should be supplied in the model space. The bounds will be transformed if
        the transform_function is provided to the parameter.

        Args:
            bounds: numpy array of shape (n, 2)
        """
        if bounds.shape[1] != 2:
            raise ParameterError("Bounds must have shape (n, 2).")
        if self.transform_function is not None:
            self.bounds = self.transform_function(bounds)
            self._bounds_transformed = True
        else:
            self.bounds = bounds

    def add_bounds_param_space(self, bounds: np.ndarray):
        """Add bounds to the parameter.

        Add bounds to the parameter in parameter space. It does not do any additional checks
        or perform any transformations.

        Args:
            bounds: numpy array of shape (n, 2)
        """
        if bounds.shape[1] != 2:
            raise ParameterError("Bounds must have shape (n, 2).")
        self.bounds = bounds
        self._bounds_transformed = True

    def add_opt_mask(self, mask: Union[np.ndarray, bool]):
        """Set mask for optimizing vector quantities.

        It expects an input array of shape (n,), where n is the dimension of the vector
        quantity to be optimized. This array must contain n booleans indicating which
        properties to optimize.

        Args:
            mask: boolean array of same shape as the vector quantity to be optimized
        """
        if isinstance(mask, bool):
            mask = np.ones_like(self, dtype=bool) * mask
        if mask.shape != self.shape:
            raise ParameterError("Mask must have shape {0}.".format(self.shape))
        self.opt_mask = mask

    def get_bounds_param_space(self) -> List[Tuple[int, int]]:
        """Returns bounds array that is used by scipy optimizer.

        Returns:
            A list of tuples of the form (lower_bound, upper_bound)
        """
        arr = self.get_opt_numpy_array_param_space()
        bounds = []
        if self.bounds is not None:
            if (self.bounds.shape[0] == arr.shape[0]) and (self.bounds.shape[1] == 2):
                for i in range(arr.shape[0]):
                    bounds.append((self.bounds[i, 0], self.bounds[i, 1]))
            else:
                raise ValueError("Bounds must have shape: {0}x2.".format(arr.shape))
        else:
            bounds = [(None, None) for i in range(arr.shape[0])]
        return bounds

    def get_bounds_model_space(self) -> np.ndarray:
        """Get the bounds in the original space.

        Returns:
            A numpy array of bounds in the original space.
        """
        if self.transform_function is not None:
            return self.transform_function.inverse_transform(self.bounds)
        else:
            return self.bounds

    def has_bounds(self) -> bool:
        """Check if bounds are set for optimizing quantities

        Returns:
            True if bounds are set, False otherwise.
        """
        return self.bounds is not None

    def as_dict(self):
        """Return a dictionary containing the state of the object."""
        state_dict = self.__dict__.copy()
        # Original dict will not have values
        state_dict["@value"] = self.get_numpy_array_model_space()
        state_dict["@module"] = self.__class__.__module__
        state_dict["@class"] = self.__class__.__name__
        return state_dict

    def save(self, filename):
        """Save the parameter to disk."""
        state_dict = self.as_dict()
        with open(filename, "wb") as f:
            pickle.dump(state_dict, f)

    @classmethod
    def from_dict(cls, state_dict):
        """Update the object's attributes based on the provided state dictionary.

        Args:
            state_dict (dict): The dictionary containing the state of the object.
                               This dictionary should include the "value" key.
        """

        # Extract the value from the state dictionary
        value = state_dict.pop("@value")
        class_name = state_dict.pop("@class")
        module_name = state_dict.pop("@module")
        is_transformed = state_dict.pop("_is_transformed")
        bounds_transformed = state_dict.pop("_bounds_transformed")
        # Update the object's attributes with the remaining key-value pairs
        # Copy the extracted value to a parameter
        obj = cls(value, **state_dict)
        obj._is_transformed = is_transformed
        obj._bounds_transformed = bounds_transformed
        return obj

    @classmethod
    def load(cls, filename):
        """Load a parameter from disk.
        TODO: non classmethod version
        """
        with open(filename, "rb") as f:
            state_dict = pickle.load(f)
        return cls.from_dict(state_dict)

    def get_opt_param_name_value_and_indices(
        self,
    ) -> Tuple[str, Union[float, np.ndarray], int]:
        """Get the name, value, and indices of the optimizable parameters.

        Returns:
            A tuple of lists of names, values, and indices of the optimizable parameters.
        """
        return self.name, self.get_numpy_array_model_space(), self.index

    @property
    def lower_bound(self):
        """Get the lower bounds of the parameter.

        Always returns values in parameter space.

        Returns:
            A numpy array of lower bounds.
        """
        bounds = self.get_bounds_param_space()
        return np.array([b[0] for b in bounds])

    @property
    def upper_bound(self):
        """Get the upper bounds of the parameter.

        Always returns values in parameter space.

        Returns:
            A numpy array of upper bounds.
        """
        bounds = self.get_bounds_param_space()
        return np.array([b[1] for b in bounds])

    @property
    def is_mutable(self):
        """Check if the parameter is mutable.

        Returns:
            True if the parameter is mutable, False otherwise.
        """
        return np.any(self.opt_mask)


class ParameterError(Exception):
    def __init__(self, msg):
        super(ParameterError, self).__init__(msg)
        self.msg = msg
