import numpy as np
import cdlparser
from . import cdf5parser

cdlparser.default_fill_values.update({
    np.dtype('U'): u"",
})

cdlparser.NC_NP_DATA_TYPE_MAP.update({
   'string':  'U',
})

class CDL4Parser(cdf5parser.CDF5Parser):
    def __init__(self, **kwargs):
        """
        Construct a CDL4Parser instance. See the CDLParser.__init__ docstring for a description of the
        currently supported keyword arguments.
        """
        super(CDL4Parser, self).__init__(file_format='NETCDF4', **kwargs)
        self.groupstack = []

    extra_reserved_words = {
        'string': 'STRING_K',
        }
    reserved_words = cdf5parser.dict_merge(extra_reserved_words, cdf5parser.CDF5Parser.reserved_words)

    # the full list of CDL tokens to parse - mostly named exactly as per the ncgen.l file
    tokens = ['GROUP',] + list(set(extra_reserved_words.values())) + cdf5parser.CDF5Parser.tokens

    def t_GROUP(self, t) :
        r'(group|GROUP):[ \t]+[^\{]+'
        parts = t.value.split()
        if len(parts) < 2 :
            raise cdlparser.CDLSyntaxError("A group name is required")
        groupname = parts[1]
        t.value = cdlparser.deescapify(groupname)
        return t

    # def p_ncdesc(self, p) :
    #     """ncdesc : NETCDF init_netcdf LBRACE groupsection RBRACE"""
    #     if self.ncdataset :
    #         if self.close_on_completion : self.ncdataset.close()
    #         self.logger.info("Closed netCDF file " + self.ncfile)
    #     self.logger.info("Finished parsing")

    # def p_groupsection(self, p) :
    #     """groupsection : group dimsection vasection datasection
    #                     | empty"""
    def p_gattdecl(self, p):
        """gattdecl : gatt EQUALS attvallist
                    | type gatt EQUALS attvallist"""
        if self.ncdataset:
            if p[2] == "=":
                self.set_attribute(':' + p[1], p[3])
            else:
                self.set_attribute(':' + p[2], p[4], att_type=p[1])

    def p_attdecl(self, p):
        """attdecl : att EQUALS attvallist
                   | type att EQUALS attvallist"""
        if self.ncdataset:
            if p[2] == "=":
                self.set_attribute(p[1], p[3])
            else:
                self.set_attribute(p[2], p[4], att_type=p[1])

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
                | DOUBLE_K
                | STRING_K"""
        super(CDL4Parser, self).p_type(p)
