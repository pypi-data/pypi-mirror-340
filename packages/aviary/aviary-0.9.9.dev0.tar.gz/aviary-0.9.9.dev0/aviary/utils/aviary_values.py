'''
Define utilities for using aviary values with associated units and testing
for compatibility with aviary metadata dictionary.

Utilities
---------
Units : type alias
    define a type hint for associated units

ValueAndUnits : type alias
    define a type hint for a single value paired with its associated units

OptionalValueAndUnits : type alias
    define a type hint for an optional single value paired with its associated units

class AviaryValues
    define a collection of named values with associated units
'''
from enum import EnumMeta

import numpy as np
from openmdao.utils.units import convert_units as _convert_units

from aviary.utils.named_values import (NamedValues, get_items, get_keys,
                                       get_values)
from aviary.variable_info.variable_meta_data import _MetaData


class AviaryValues(NamedValues):
    '''
    Define a collection of aviary values with associated units and aviary tests.
    '''

    def set_val(self, key, val, units='unitless', meta_data=_MetaData):
        '''
        Update the named value and its associated units.

        Note, specifying units of `None` or units of any type other than `str` will raise
        `Typerror`.

        Parameters
        ----------
        key : str
            the name of the item

        val : Any
            the new value of the item

        units : str ('unitless')
            the units associated with the new value, if any

        Raises
        ------
        TypeError
            if units of `None` were specified or units of any type other than `str`
        '''

        # Special handling to access an Enum member from either the member name or its value.
        my_val = val
        if key in _MetaData.keys():

            expected_types = _MetaData[key]['types']

            if not isinstance(expected_types, tuple):
                expected_types = (expected_types, )

            for _type in expected_types:
                if type(_type) is EnumMeta:
                    if self._is_iterable(val):
                        my_val = [self._convert_to_enum(
                            item, _type) for item in val]
                    else:
                        my_val = self._convert_to_enum(val, _type)
                    break

            # Special handling if the variable is supposed to be an array
            default_value = _MetaData[key]['default_value']
            # if the item is supposed to be an iterable...
            if self._is_iterable(default_value):
                # but the provided value is not...
                if not self._is_iterable(my_val):
                    # make object the correct iterable
                    if isinstance(default_value, tuple):
                        my_val = (my_val,)
                    else:
                        my_val = np.array([my_val], dtype=type(default_value[0]))

            self._check_type(key, my_val, meta_data=meta_data)
            self._check_units_compatability(key, my_val, units, meta_data=meta_data)

        super().set_val(key=key, val=my_val, units=units)

    def _check_type(self, key, val, meta_data=_MetaData):

        expected_types = meta_data[key]['types']
        if expected_types is None:
            # MetaData item has no type requirement.
            return

        if self._is_iterable(expected_types):
            expected_types = tuple(expected_types)

        # if val is not iterable, add it to a list (length 1), checks assume
        # val is iterable
        if not self._is_iterable(val):
            val = [val]
        # numpy arrays have special typings. Extract item of equivalent built-in python type
        # numpy arrays do not allow mixed types, only have to check first entry
        # empty arrays do not need this check
        if isinstance(val, np.ndarray) and len(val) > 0:
            # NoneType numpy arrays do not need to be "converted" to built-in python types
            if val.dtype == type(None):
                val = [val[0]]
            else:
                # item() gets us native Python equivalent object (i.e. int vs. numpy.int64)
                # wrap first index in np array to ensures works on any dtype
                val = [np.array(val[0]).item()]
        for item in val:
            has_bool = False  # needs some fancy shenanigans because bools will register as ints
            if (isinstance(expected_types, type)):
                if expected_types is bool:
                    has_bool = True
            elif bool in expected_types:
                has_bool = True
            if (not isinstance(item, expected_types)) or (
                    (has_bool == False) and (isinstance(item, bool))):
                raise TypeError(
                    f'{key} is of type(s) {meta_data[key]["types"]} but you '
                    f'have provided a value of type {type(item)}.')

    def _check_units_compatability(self, key, val, units, meta_data=_MetaData):
        expected_units = meta_data[key]['units']

        try:
            # NOTE the value here is unimportant, we only care if OpenMDAO will
            # convert the units
            _convert_units(10, expected_units, units)
        except ValueError:
            raise ValueError(
                f'The units {units} which you have provided for {key} are invalid.')
        except TypeError:
            raise TypeError(
                f'The base units of {key} are {expected_units}, and you have tried to set {key} with units of {units}, which are not compatible.')
        except BaseException:
            raise KeyError('There is an unknown error with your units.')

    def _is_iterable(self, val):
        return isinstance(val, _valid_iterables)

    def _convert_to_enum(self, val, enum_type):
        if isinstance(val, str):
            try:
                # see if str maps to ENUM value
                return enum_type(val)
            except ValueError:
                # str instead maps to ENUM name
                return enum_type[val.upper()]
        else:
            return enum_type(val)

    def items(self):
        """
        Return (name, value) for variables contained in this vector.

        Note that AviaryValues is not a dictionary, but this adds support for iterating over
        its contents.

        Yields
        ------
        str
            The name of an item.
        object
            The value of that item.
        """
        for key, val in self._mapping.items():
            yield key, val


_valid_iterables = (list, np.ndarray, tuple)
