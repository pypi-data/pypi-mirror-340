import unittest
import tempfile
import os
from pywmm.coefficients import read_coefficients

class DummyInstance:
    def __init__(self):
        # Minimal attributes expected by read_coefficients
        self.coeff_file = None
        self.epoch = None
        self.defaultDate = None
        # Allocate 13x13 arrays for c and cd
        self.c = [[0.0 for _ in range(13)] for _ in range(13)]
        self.cd = [[0.0 for _ in range(13)] for _ in range(13)]

class TestReadCoefficients(unittest.TestCase):
    def setUp(self):
        # Create a temporary dummy WMM.COF file.
        # The file contains:
        #   - A header line with 3 tokens to set epoch (e.g. "2020.0 0.0 0.0")
        #   - Two coefficient lines (each with 6 tokens)
        #   - A terminating line (with a single token) to end reading.
        self.dummy_cof_content = (
            "2020.0 0.0 0.0\n"         # Header: epoch set to 2020.0; defaultDate should be 2022.5
            "1 0 1000.0 0.0 0.0 0.0\n"  # For n=1, m=0; should set dummy.c[0][1]=1000.0 and dummy.cd[0][1]=0.0
            "1 1 200.0 50.0 0.0 0.0\n"  # For n=1, m=1; should set dummy.c[1][1]=200.0, dummy.cd[1][1]=0.0,
                                       # and since m != 0, also dummy.c[1][0]=50.0 and dummy.cd[1][0]=0.0
            "0\n"                      # A single token line to signal termination.
        )
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.temp_file.write(self.dummy_cof_content)
        self.temp_file.close()

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_read_coefficients_custom_file(self):
        dummy = DummyInstance()
        # Override the default by setting a custom coefficients file.
        dummy.coeff_file = self.temp_file.name
        read_coefficients(dummy)
        
        # Verify header values.
        self.assertEqual(dummy.epoch, 2020.0)
        self.assertEqual(dummy.defaultDate, 2020.0 + 2.5)
        
        # Verify coefficient line for n=1, m=0.
        self.assertEqual(dummy.c[0][1], 1000.0)
        self.assertEqual(dummy.cd[0][1], 0.0)
        
        # Verify coefficient line for n=1, m=1.
        self.assertEqual(dummy.c[1][1], 200.0)
        self.assertEqual(dummy.cd[1][1], 0.0)
        # For m != 0, it should also set c[n][m-1] and cd[n][m-1].
        self.assertEqual(dummy.c[1][0], 50.0)
        self.assertEqual(dummy.cd[1][0], 0.0)

if __name__ == '__main__':
    unittest.main()
