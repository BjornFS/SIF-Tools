# Test suite for SIFconvert and related functions
#     EXECUTE: "PYTHONPATH=$(pwd) pytest -v"
import os
import numpy as np
import pytest

# Import modules
from sif_tools.conversion import SIFconvert
from sif_tools.source import source
from sif_tools.calibration import extract_calibration

# Path to UnitTest.sif file
TEST_FILE = os.path.join(os.path.dirname(__file__), 'UnitTest.sif')


def test_conversion_runs_without_exception():
    """End-to-end test that SIFconvert runs and returns a NumPy array."""
    result = SIFconvert(TEST_FILE)
    assert isinstance(result, np.ndarray), "Output is not a NumPy array"
    assert result.shape[1] == 2, "Output does not have two columns (wavelengths, counts)"


def test_source_parse_returns_expected_structure():
    """Test that source.parse returns a tuple of (np.ndarray, OrderedDict)."""
    data, info = source.parse(TEST_FILE)
    assert isinstance(data, np.ndarray), "Parsed data is not NumPy array"
    assert isinstance(info, dict), "Info is not a dictionary"
    assert data.shape[1] == 2, "Parsed data should have 2 columns"


def test_extract_calibration_returns_correct_type():
    """Test that extract_calibration returns correct calibration data."""
    _, info = source.parse(TEST_FILE)
    calibration = extract_calibration(info)
    assert calibration is None or isinstance(calibration, np.ndarray), "Calibration is not NumPy array or None"


def test_conversion_fails_on_invalid_path():
    """Test that SIFconvert correctly raises an exception on invalid input."""
    with pytest.raises(RuntimeError):
        SIFconvert("non_existent_file.sif")