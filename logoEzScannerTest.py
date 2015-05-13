#-*- coding: shift_jis -*-

import unittest
from logoScanner import *


class LogoEzScannerTest(unittest.TestCase):
    def testScanWords(self):
        source = 'print "hogehoge 42 aria99 3.14 :hoge "hoge28 :arg1'

        scanner = LGEzScanner( source )

        scanner.advance()
        self.assertEqual( scanner.getTokenValue(), 'print')
        self.assertEqual( scanner.getTokenType(),  LGTokenType.Word )

        scanner.advance()
        self.assertEqual( scanner.getTokenValue(), '"hogehoge')
        self.assertEqual( scanner.getTokenType(),  LGTokenType.QWrd )

        scanner.advance()
        self.assertEqual( scanner.getTokenValue(), '42')
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )

        scanner.advance()
        self.assertEqual( scanner.getTokenValue(), 'aria99')
        self.assertEqual( scanner.getTokenType(),  LGTokenType.Word )

        scanner.advance()
        self.assertEqual( scanner.getTokenValue(), '3.14')
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )

        scanner.advance()
        self.assertEqual( scanner.getTokenValue(), ':hoge')
        self.assertEqual( scanner.getTokenType(),  LGTokenType.DWrd )

        scanner.advance()
        self.assertEqual( scanner.getTokenValue(), '"hoge28')
        self.assertEqual( scanner.getTokenType(),  LGTokenType.QWrd )

        scanner.advance()
        self.assertEqual( scanner.getTokenValue(), ':arg1')
        self.assertEqual( scanner.getTokenType(),  LGTokenType.DWrd )

        try:
            scanner.advance()
            self.fail( 'stop Iteration' )
        except StopIteration:
            pass

    def testScanList1(self):
        source = 'print [ sum 42   :arg ]'

        scanner = LGEzScanner( source )

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.Word )
        self.assertEqual( scanner.getTokenValue(), 'print')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.LOpn )
        self.assertEqual( scanner.getTokenValue(), '[')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.Word )
        self.assertEqual( scanner.getTokenValue(), 'sum')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '42')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.DWrd )
        self.assertEqual( scanner.getTokenValue(), ':arg')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.LCls )
        self.assertEqual( scanner.getTokenValue(), ']')


    def testScanList2(self):
        source = 'print [ print [ sum 42   :arg ] ]'

        scanner = LGEzScanner( source )

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.Word )
        self.assertEqual( scanner.getTokenValue(), 'print')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.LOpn )
        self.assertEqual( scanner.getTokenValue(), '[')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.Word )
        self.assertEqual( scanner.getTokenValue(), 'print')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.LOpn )
        self.assertEqual( scanner.getTokenValue(), '[')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.Word )
        self.assertEqual( scanner.getTokenValue(), 'sum')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '42')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.DWrd )
        self.assertEqual( scanner.getTokenValue(), ':arg')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.LCls )
        self.assertEqual( scanner.getTokenValue(), ']')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.LCls )
        self.assertEqual( scanner.getTokenValue(), ']')


    def testScanGroup1(self):
        source = 'print ( sum 42 -55 3.3 -2.1 +40 +6.6 )'

        scanner = LGEzScanner( source )

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.Word )
        self.assertEqual( scanner.getTokenValue(), 'print')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.GOpn )
        self.assertEqual( scanner.getTokenValue(), '(')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.Word )
        self.assertEqual( scanner.getTokenValue(), 'sum')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '42')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '-55')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '3.3')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '-2.1')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '+40')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '+6.6')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.GCls )
        self.assertEqual( scanner.getTokenValue(), ')')

    def testScanGroup2(self):
        source = 'print ( sum 42 ( -55 3.3 -2.1 ) +40 ( +6.6 ) )'

        scanner = LGEzScanner( source )

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.Word )
        self.assertEqual( scanner.getTokenValue(), 'print')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.GOpn )
        self.assertEqual( scanner.getTokenValue(), '(')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.Word )
        self.assertEqual( scanner.getTokenValue(), 'sum')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '42')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.GOpn )
        self.assertEqual( scanner.getTokenValue(), '(')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '-55')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '3.3')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '-2.1')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.GCls )
        self.assertEqual( scanner.getTokenValue(), ')')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '+40')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.GOpn )
        self.assertEqual( scanner.getTokenValue(), '(')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '+6.6')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.GCls )
        self.assertEqual( scanner.getTokenValue(), ')')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.GCls )
        self.assertEqual( scanner.getTokenValue(), ')')
