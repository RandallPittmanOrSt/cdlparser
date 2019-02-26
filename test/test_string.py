"""
Unit tests for the CDF-5 constant types.
"""
import os
import tempfile
import unittest
import cdf4parser
import numpy as np

#---------------------------------------------------------------------------------------------------
class TestStrings(unittest.TestCase) :
#---------------------------------------------------------------------------------------------------
    def setUp(self) :
        cdltext = r"""netcdf cdf5_constants {
            dimensions:
                dim1 = 5;
            variables:
                string strvar(dim1);
                strvar:_FillValue = "؆";
                // string strvar:stratt = "ǐ\tǒƯ";
            data:
                strvar = "abc", "defg", "_", "def", "\nƷƬƫ";
            }"""
        parser = cdf4parser.CDF4Parser()
        self.tmpfh, self.tmpfile = tempfile.mkstemp(suffix='.nc')
        self.dataset = parser.parse_text(cdltext, ncfile=self.tmpfile)

    def tearDown(self):
        self.dataset.close()
        os.close(self.tmpfh)  # Needed on Windows to be able to delete the file
        if os.path.exists(self.tmpfile) : os.remove(self.tmpfile)

    @unittest.expectedFailure
    def test_attrs(self):
        raise Exception("Need to test string attributes")

    def test_strvar(self):
        self.assertTrue("strvar" in self.dataset.variables.keys())
        strvar = self.dataset["strvar"]
        self.assertTrue(strvar.dtype == np.dtype('str'))
        data = strvar[:]
        self.assertTrue(len(data) == 5)
        self.assertTrue(data[0] == u"abc")
        self.assertTrue(data[1] == u"defg")
        self.assertTrue(data[2] == u"؆")
        self.assertTrue(data[3] == u"def")
        self.assertTrue(data[4] == u"\nƷƬƫ")

if __name__ == '__main__':
    unittest.main()
