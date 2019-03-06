import unittest

#initialize the test suit
start_dir = 'tests/'
loader = unittest.TestLoader()
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)