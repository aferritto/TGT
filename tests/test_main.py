'''
Tests main. The best way to test main is the run it, however.
'''
import pytest
from tgt import main

def test_main():
    main.main() # mostly a UI method, so just ensure it does not crash