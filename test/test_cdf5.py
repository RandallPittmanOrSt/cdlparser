"""
Unit tests for the CDF-5 constant types.
"""
import os
import tempfile
import unittest
from cdlparser import cdf5parser
import numpy as np

#---------------------------------------------------------------------------------------------------
class TestCDF5(unittest.TestCase) :
#---------------------------------------------------------------------------------------------------
    def setUp(self) :
        cdltext = r"""netcdf cdf5_constants {
        dimensions:
            dim1 = 5;
        variables:
            ubyte var_ub(dim1);
                var_ub:_FillValue = 250ub;
            ushort var_us(dim1);
                var_us:_FillValue = 65534us;
            uint var_ui(dim1);
                var_ui:_FillValue = 1;
            int64 var_i8(dim1);
                var_i8:_FillValue = -1;
            uint64 var_ui8(dim1);
                var_ui8:_FillValue = 42;
            // global attributes
            :ubyte_attr = 255UB;
            :ushort_attr = 65535US;
            :uint_attr = 4294967295U;
            :int64_attr = -9223372036854775806LL;
            :uint64_attr = 18446744073709551614ULL;
        data:
            var_ub = 250ub, 0x27, 255ub, 4, _;
            var_us = 0x3456, 65534us, 65535us, 65530us, _;
            var_ui = 0xfedcba98u, 4294967295U, 1, 07654321765u, _;  // hex, max val, FillValue, octal
            var_ui8 = 0xfedcba9876543210ull, 18446744073709551615ULL, 0765432107654321076543ULL, 42, _;  // hex, max val, octal, FillValue, fill test
            var_i8 = -9223372036854775807LL, 9223372036854775807LL, 0xfedcba987654321LL, 0765432107654321076543LL, -1;
        }"""
        parser = cdf5parser.CDF5Parser()
        self.tmpfh, self.tmpfile = tempfile.mkstemp(suffix='.nc')
        self.dataset = parser.parse_text(cdltext, ncfile=self.tmpfile)

    def tearDown(self):
        self.dataset.close()
        os.close(self.tmpfh)  # Needed on Windows to be able to delete the file
        if os.path.exists(self.tmpfile) : os.remove(self.tmpfile)

    def test_attrs(self):
        self.assertTrue(self.dataset.ubyte_attr == 255)
        self.assertTrue(type(self.dataset.ubyte_attr) == np.uint8)
        self.assertTrue(self.dataset.ushort_attr == 65535)
        self.assertTrue(type(self.dataset.ushort_attr) == np.uint16)
        self.assertTrue(self.dataset.uint_attr == 4294967295)
        self.assertTrue(type(self.dataset.uint_attr) == np.uint32)
        self.assertTrue(self.dataset.uint64_attr == 18446744073709551614)
        self.assertTrue(type(self.dataset.uint64_attr) == np.uint64)

    @unittest.expectedFailure
    def test_int64_attr(self):
        # netcdf4-python <= 1.4.2 lacks support for int64 attrs in CDF-5 files
        # Will be fixed soon (prob 1.4.3) -- see https://github.com/Unidata/netcdf4-python/issues/878
        self.assertTrue(self.dataset.int64_attr == -9223372036854775806)
        self.assertTrue(type(self.dataset.int64_attr) == np.int64)


    def test_var_ubyte(self):
        self.assertTrue("var_ub" in self.dataset.variables.keys())
        var_ub = self.dataset["var_ub"]
        self.assertTrue(var_ub.dtype == np.dtype('uint8'))
        data = var_ub[:]
        self.assertTrue(np.ma.isMA(data))
        self.assertTrue(len(data) == 5)
        self.assertTrue(data[0] is np.ma.masked)
        self.assertTrue(data[1] == np.uint8(0x27))
        self.assertTrue(data[2] == np.uint8(255))
        self.assertTrue(data[3] == np.uint8(4))
        self.assertTrue(data[4] is np.ma.masked)

    def test_var_ushort(self):
        self.assertTrue("var_us" in self.dataset.variables.keys())
        var_us = self.dataset["var_us"]
        self.assertTrue(var_us.dtype == np.dtype('uint16'))
        data = var_us[:]
        self.assertTrue(np.ma.isMA(data))
        self.assertTrue(len(data) == 5)
        self.assertTrue(data[0] == np.uint16(0x3456))
        self.assertTrue(data[1] is np.ma.masked)
        self.assertTrue(data[2] == np.uint16(65535))
        self.assertTrue(data[3] == np.uint16(65530))
        self.assertTrue(data[4] is np.ma.masked)

    def test_var_uint(self):
        self.assertTrue("var_ui" in self.dataset.variables.keys())
        var_ui = self.dataset["var_ui"]
        self.assertTrue(var_ui.dtype == np.dtype('uint32'))
        data = var_ui[:]
        self.assertTrue(np.ma.isMA(data))
        self.assertTrue(len(data) == 5)
        self.assertTrue(data[0] == np.uint32(0xfedcba98))
        self.assertTrue(data[1] == np.uint32(4294967295))
        self.assertTrue(data[2] is np.ma.masked)
        self.assertTrue(data[3] == np.uint32(0o7654321765))
        self.assertTrue(data[4] is np.ma.masked)

    def test_var_int64(self):
        self.assertTrue("var_i8" in self.dataset.variables.keys())
        var_i8 = self.dataset["var_i8"]
        self.assertTrue(var_i8.dtype == np.dtype('int64'))
        data = var_i8[:]
        self.assertTrue(np.ma.isMA(data))
        self.assertTrue(len(data) == 5)
        self.assertTrue(data[0] == np.int64(-9223372036854775807))
        self.assertTrue(data[1] == np.int64(9223372036854775807))
        self.assertTrue(data[2] == np.int64(0xfedcba987654321))
        self.assertTrue(data[3] == np.int64(0o765432107654321076543))
        self.assertTrue(data[4] is np.ma.masked)

    def test_var_uint64(self):
        self.assertTrue("var_ui8" in self.dataset.variables.keys())
        var_ui8 = self.dataset["var_ui8"]
        self.assertTrue(var_ui8.dtype == np.dtype('uint64'))
        data = var_ui8[:]
        self.assertTrue(np.ma.isMA(data))
        self.assertTrue(len(data) == 5)
        self.assertTrue(data[0] == np.uint64(0xfedcba9876543210))
        self.assertTrue(data[1] == np.uint64(18446744073709551615))
        self.assertTrue(data[2] == np.uint64(0o765432107654321076543))
        self.assertTrue(data[3] is np.ma.masked)
        self.assertTrue(data[4] is np.ma.masked)

if __name__ == '__main__':
    unittest.main()
