import pytest
import sys
import os

# Adiciona o diretório do pacote ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from module.core import hello_world

def test_hello_world():
    assert hello_world() == "Hello, world!"
