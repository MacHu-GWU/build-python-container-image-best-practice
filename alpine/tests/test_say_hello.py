# -*- coding: utf-8 -*-

import os
import pytest

from my_project.say_hello import say_hello


def test_say_hello():
    say_hello()
    say_hello(name="alice")
    
    
if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
