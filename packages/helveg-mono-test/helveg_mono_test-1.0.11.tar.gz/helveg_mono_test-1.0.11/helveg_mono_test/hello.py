"""Sample Hello World application."""
from helveg_mono_test_dep.hello import hello as _hello

def hello():
    """Return a friendly greeting."""
    return "Hello helveg-mono-test"

def hello_dep():
    """Return a dependency greeting"""
    return "From dep:" + _hello()