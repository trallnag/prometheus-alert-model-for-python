import os
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
    should_debug = True

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
    source = pathlib.Path(FILE).parent.joinpath("data")
    destination = tmp_path

    for item in os.listdir(source):
        s = os.path.join(source, item)
        print(s)
        d = os.path.join(destination, item)
        print(d)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks=False, ignore=None)
        else:
            shutil.copy2(s, d)

    return tmp_path


# ==============================================================================
