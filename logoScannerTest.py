#-*- coding: shift_jis -*-

import unittest
from logoScanner import *


class LogoScannerTest(unittest.TestCase):
    def testScanWords(self):
        source = 'print "hogehoge 42 aria99 3.14 :hoge "hoge28 :arg1'

        scanner = LGScanner( source )

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.Word )
        self.assertEqual( scanner.getTokenValue(), 'print')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.QWrd )
        self.assertEqual( scanner.getTokenValue(), '"hogehoge')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '42')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.Word )
        self.assertEqual( scanner.getTokenValue(), 'aria99')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '3.14')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.DWrd )
        self.assertEqual( scanner.getTokenValue(), ':hoge')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.QWrd )
        self.assertEqual( scanner.getTokenValue(), '"hoge28')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.DWrd )
        self.assertEqual( scanner.getTokenValue(), ':arg1')

        try:
            scanner.advance()
            self.fail( 'stop Iteration' )
        except StopIteration:
            pass

    def testScanList1(self):
        source = 'print [sum 42   :arg]'

        scanner = LGScanner( source )

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
        source = 'print [print[sum 42   :arg]]'

        scanner = LGScanner( source )

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
        source = 'print (sum 42 -55 3.3 -2.1 +40 +6.6)'

        scanner = LGScanner( source )

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
        source = 'print (sum 42 (-55 3.3 -2.1) +40 (+6.6))'

        scanner = LGScanner( source )

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


    def testScanBinOpe(self):
        source = '1 + 2 - 3 * 4 / 5 < 6 > 7 = 8'

        scanner = LGScanner( source )

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '1')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.BOpe )
        self.assertEqual( scanner.getTokenValue(), '+')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '2')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.BOpe )
        self.assertEqual( scanner.getTokenValue(), '-')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '3')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.BOpe )
        self.assertEqual( scanner.getTokenValue(), '*')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '4')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.BOpe )
        self.assertEqual( scanner.getTokenValue(), '/')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '5')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.BOpe )
        self.assertEqual( scanner.getTokenValue(), '<')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '6')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.BOpe )
        self.assertEqual( scanner.getTokenValue(), '>')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '7')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.BOpe )
        self.assertEqual( scanner.getTokenValue(), '=')

        scanner.advance()
        self.assertEqual( scanner.getTokenType(),  LGTokenType.NWrd )
        self.assertEqual( scanner.getTokenValue(), '8')
