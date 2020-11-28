import pathlib
import shutil
import sys
from typing import Optional

import pytest
from devtools import debug

# ==============================================================================


class Helpers:
    """Contains (possibly) useful random utilities

    Combined with the fixture that returns this class it is easy to share
    common functions across multiple tests. Simply use `helpers` as a parameter
    for the respective test function.

    Helpers should be static methods generally.
    """

    separator = "-" * 80
    should_debug = False

    @staticmethod
    def wrapped_debug(element, description: Optional[str] = None) -> None:
        if Helpers.should_debug:
            print(f"\n{Helpers.separator}\n")
            if description:
                print(f"{description}\n")
            debug(element)
            print(f"\n{Helpers.separator}\n")


@pytest.fixture
def helpers():
    return Helpers


# ==============================================================================


FILE = __file__


@pytest.fixture
def data_path(tmp_path):
    shutil.copytree(
        pathlib.Path(FILE).parent.joinpath("data"), tmp_path, dirs_exist_ok=True
    )

    return tmp_path


# ==============================================================================
