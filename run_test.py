import unittest
import sys
import os

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Discover and run all tests
if __name__ == "__main__":
    loader = unittest.TestLoader()
    # look for files matching test*.py under the tests/ folder
    suite = loader.discover(start_dir=os.path.join(PROJECT_ROOT, "tests"), pattern="test*.py")

    runner = unittest.TextTestRunner(
        verbosity=2,  # 2 gives detailed test names + results
        buffer=True   # captures stdout/stderr for cleaner logs
    )

    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())
