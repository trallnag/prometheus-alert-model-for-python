# Copyright © 2020 Tim Schwenke <tim.and.trallnag+code@gmail.com>
# Licensed under Apache License 2.0 <http://www.apache.org/licenses/LICENSE-2.0>

from typing import Dict, List


def intersect(list_of_dcts: List[Dict[str, str]]) -> Dict[str, str]:
    """Calculates the key-value intersection of a list of dictionaries.

    Args:
        list_of_dcts (List[Dict[str, str]]): List of dictionaries to intersect.
            Will not be mutated.

    Returns:
        Dict[str, str]: A new dictionary that contains the intersection of all
            key-value combinations. Meaning all key-values that occur in very
            single dictionary in the given list. If the given list is empty,
            an empty `dict` will be returned. If the given list contains only
            one `dict`, this `dict` will be copied and returned.
    """

    if len(list_of_dcts) == 0:
        return {}
    elif len(list_of_dcts) == 1:
        return list_of_dcts[0].copy()

    list_of_sets = [set(dct.items()) for dct in list_of_dcts]

    intersection_set = list_of_sets[0].intersection(*list_of_sets[1:])

    return dict(intersection_set)
