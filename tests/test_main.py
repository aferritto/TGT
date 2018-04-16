"""
Tests main. The best way to test main is the run it, however.
"""
import pytest
from tgt import main
from tgt import preferences as prefs


def test_main():
    prefs.NGEN = 1
    prefs.UNIT_TEST = True
    main.main()  # mostly a UI method, so just ensure it does not crash
