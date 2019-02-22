import numpy as np
import cdlparser

cdlparser.default_fill_values.update({
    np.dtype('uint8'): np.uint8(255),
    np.dtype('uint16'): np.uint16(65535),
    np.dtype('uint32'): np.uint32(4294967295),
    np.dtype('uint64'): np.uint64(18446744073709551614),
    np.dtype('int64'): np.int64(-9223372036854775806),
})

cdlparser.numeric_min_max.update({
   np.dtype('uint8'): (0, 255),
   np.dtype('uint16'): (0,65535),
   np.dtype('uint32'): (0, 4294967295),
   np.dtype('uint64'): (0, 18446744073709551615),
   np.dtype('int64'): (-9223372036854775807, 9223372036854775807),
})

cdlparser.NC_NP_DATA_TYPE_MAP.update({
   'ubyte':   'u1',
   'ushort':  'u2',
   'uint':    'u4',
   'int64':   'i8',
   'uint64':  'u8',
})

# ---------------------------------------------------------------------------------------------------
class CDF5Parser(cdlparser.CDL3Parser):
    # ---------------------------------------------------------------------------------------------------
    """
    Class for parsing a CDL file with the classic data model, but extended with the unsigned and 64-bit
    integer types (CDF-5). Please refer to this module's docstring and also the docstrings in the
    CDLParser base class for information regarding recommended usage patterns.
    """

    def __init__(self, file_format='NETCDF3_64BIT_DATA', **kwargs):
        """
        Construct a CDF5Parser instance. See the CDLParser.__init__ docstring for a description of the
        currently supported keyword arguments.

        By default for this parser, file_format='NETCDF3_64_BIT_DATA' (CDF-5), but it is also
        compatible with 'NETCDF4'.
        """
        super(CDF5Parser, self).__init__(file_format=file_format, **kwargs)

    # netCDF-3 reserved words - mainly data types
    reserved_words = {
        'ubyte': 'UBYTE_K',
        'ushort': 'USHORT_K',
        'uint64': 'UINT64_K',
        'uint': 'UINT_K',
        'byte': 'BYTE_K',
        'char': 'CHAR_K',
        'short': 'SHORT_K',
        'int64': 'INT64_K',
        'int': 'INT_K',
        'integer': 'INT_K',
        'long': 'INT_K',
        'float': 'FLOAT_K',
        'real': 'FLOAT_K',
        'double': 'DOUBLE_K',
        'unlimited': 'NC_UNLIMITED_K'
    }

    # the full list of CDL tokens to parse - mostly named exactly as per the ncgen.l file
    tokens = [
                 'NETCDF', 'DIMENSIONS', 'VARIABLES', 'DATA', 'IDENT', 'TERMSTRING',
                 'UBYTE_CONST', 'USHORT_CONST', 'UINT64_CONST', 'UINT_CONST',
                 'BYTE_CONST', 'CHAR_CONST', 'SHORT_CONST', 'INT64_CONST', 'INT_CONST',
                 'FLOAT_CONST', 'DOUBLE_CONST',
                 'FILLVALUE', 'COMMENT', 'EQUALS', 'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN', 'EOL'
             ] + list(set(reserved_words.values()))

    def t_UBYTE_CONST(self, t):
        r'[+-]?[0-9]+[Uu][Bb]'
        return cdlparser.numeric_token(t, 2, int, np.uint8, "unsigned byte")

    def t_USHORT_CONST(self, t):
        r'[+-]?([0-9]+|0[xX][0-9a-fA-F]+)[uU][sS]'
        return cdlparser.numeric_token(t, 2, int, np.uint16, "unsigned short")

    def t_UINT64_CONST(self, t):
        r'[+-]?([0-9]+|0[xX][0-9a-fA-F]+)[uU][lL][lL]'
        return cdlparser.numeric_token(t, 3, int, np.uint64, "unsigned 64-bit integer")

    def t_UINT_CONST(self, t):
        r'[+-]?([0-9]+|0[xX][0-9a-fA-F]+)[uU](?![lLsS])'
        return cdlparser.numeric_token(t, 1, int, np.uint32, "unsigned integer")

    def t_INT64_CONST(self, t):
        r'[+-]?([0-9]+|0[xX][0-9a-fA-F]+)[lL][lL]'
        return cdlparser.numeric_token(t, 2, int, np.int64, "64-bit integer")

    def p_type(self, p):
        """type : UINT64_K
                | USHORT_K
                | UBYTE_K
                | UINT_K
                | BYTE_K
                | CHAR_K
                | SHORT_K
                | INT64_K
                | INT_K
                | FLOAT_K
                | DOUBLE_K"""
        super(CDF5Parser, self).p_type(p)

    def p_attconst(self, p):
        """attconst : UBYTE_CONST
                    | USHORT_CONST
                    | UINT64_CONST
                    | UINT_CONST
                    | BYTE_CONST
                    | CHAR_CONST
                    | SHORT_CONST
                    | INT64_CONST
                    | INT_CONST
                    | FLOAT_CONST
                    | DOUBLE_CONST
                    | TERMSTRING"""
        super(CDF5Parser, self).p_attconst(p)

    def p_const(self, p):
        """const : UBYTE_CONST
                 | USHORT_CONST
                 | UINT64_CONST
                 | UINT_CONST
                 | BYTE_CONST
                 | CHAR_CONST
                 | SHORT_CONST
                 | INT64_CONST
                 | INT_CONST
                 | FLOAT_CONST
                 | DOUBLE_CONST
                 | TERMSTRING
                 | FILLVALUE"""
        super(CDF5Parser, self).p_const(p)

