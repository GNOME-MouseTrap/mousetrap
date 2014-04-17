from unittest import TestLoader
from unittest.runner import TextTestRunner

test_loader = TestLoader()
tests = test_loader.discover('src/mousetrap')

test_runner = TextTestRunner()

test_runner.run(tests)
