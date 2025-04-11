import pytest

from solidipes.scripts.main import main_PYTHON_ARGCOMPLETE_OK


def test_main_empty():
    """Test main with no arguments."""
    with pytest.raises(SystemExit):
        main_PYTHON_ARGCOMPLETE_OK()
