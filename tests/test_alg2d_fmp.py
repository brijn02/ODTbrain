"""Test Fourier mapping algorithm"""
import os
import sys

import numpy as np
import odtbrain
import pytest

from common_methods import create_test_sino_2d, cutout, \
    get_test_parameter_set, write_results, get_results

WRITE_RES = False

# See https://github.com/RI-imaging/ODTbrain/issues/13
CI_FAILS = (os.environ.get("RUNNER_OS", "None") == "Linux"
            or os.environ.get("RUNNER_OS", "None") == "macOS")


@pytest.mark.xfail(CI_FAILS, reason="Unexplained issue #13")
@pytest.mark.filterwarnings(
    "ignore::odtbrain.warn.ImplementationAmbiguousWarning")
def test_2d_fmap():
    myframe = sys._getframe()
    sino, angles = create_test_sino_2d()
    parameters = get_test_parameter_set(1)
    r = []
    for p in parameters:
        f = odtbrain.fourier_map_2d(sino, angles, **p)
        r.append(cutout(f))
    if WRITE_RES:
        write_results(myframe, r)
    assert np.allclose(np.array(r).flatten().view(float), get_results(myframe))


if __name__ == "__main__":
    # Run all tests
    loc = locals()
    for key in list(loc.keys()):
        if key.startswith("test_") and hasattr(loc[key], "__call__"):
            loc[key]()
