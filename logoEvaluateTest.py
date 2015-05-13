#-*- coding: shift_jis -*-

import unittest
from logoParser import *
from logoScanner import *
from logoContext import *

class SumFunc(object):
    def requieredArgCount(self): return 2
    def evaluate(self, context, args):
        return LGNumWord( args[0].value + args[1].value )

class DifferenceFunc(object):
    def requieredArgCount(self): return 2
    def evaluate(self, context, args):
        return LGNumWord( args[0].value - args[1].value )

class PrintFunc(object):
    def __init__(self):
        self.output = []
    def requieredArgCount(self): return 1
    def evaluate(self, context, args):
        if type(args[0]) == LGQuoWord:
            self.output.append( args[0].value[1:] )
        else:
            self.output.append( args[0].__str__() )

class MakeFunc(object):
    def requieredArgCount(self): return 2
    def evaluate(self, context, args):
        context.makeVariable( args[0].value[1:], args[1] )

class NonParamFunc(object):
    def __init__(self): self.isEvaluated = False
    def requieredArgCount(self): return 0
    def evaluate(self, context, args):
        self.isEvaluated = True


class LogoEvaluateTest(unittest.TestCase):

    def test1ArgCommand(self):
        context = LGContext()
        printfunc = PrintFunc()
        context.makeFunction( 'sum', SumFunc() )
        context.makeFunction( 'print', printfunc )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'print "hello' )

        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret, None )
        self.assertEqual( printfunc.output[0], 'hello' )

    def testCommandInputOperation(self):
        context = LGContext()
        printfunc = PrintFunc()
        context.makeFunction( 'sum', SumFunc() )
        context.makeFunction( 'print', printfunc )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'print sum 40 2' )

        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret, None )
        self.assertEqual( printfunc.output[0], '42' )

    def testVariableAccess(self):
        context = LGContext()
        printfunc = PrintFunc()
        context.makeFunction( 'print', printfunc )
        context.makeFunction( 'make', MakeFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'make "hoge 42' )

        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( context.variables['hoge'].value, 42 )

        scanner = LGScanner( 'print :hoge' )

        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )
        self.assertEqual( printfunc.output[0], '42' )

        scanner = LGScanner( 'print (:hoge)' )

        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )
        self.assertEqual( printfunc.output[1], '42' )

    def testNonParamFunc(self):
        context = LGContext()
        printfunc = PrintFunc()
        context.makeFunction( 'print', printfunc )
        nopfunc   = NonParamFunc()
        context.makeFunction( 'nop', nopfunc )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'nop print "hoge' )

        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret, None )
        self.assertEqual( printfunc.output[0], 'hoge' )

        self.assertEqual( ret, None )
        self.assertEqual( nopfunc.isEvaluated, True )

    def testBinOpePlus_01(self):
        context = LGContext()
        printfunc = PrintFunc()
        context.makeFunction( 'print', printfunc )
        context.makeFunction( '+', SumFunc() )
        context.makeFunction( 'sum', SumFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( '1 + 2' )

        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 3 )
        self.assertEqual( type(ret), LGNumWord )


    def testBinOpePlus_02(self):
        context = LGContext()
        printfunc = PrintFunc()
        context.makeFunction( 'print', printfunc )
        context.makeFunction( '+', SumFunc() )
        context.makeFunction( 'sum', SumFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( '1 + 2 + 3' )

        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 6 )
        self.assertEqual( type(ret), LGNumWord )

    def testBinOpePlus_03(self):
        context = LGContext()
        printfunc = PrintFunc()
        context.makeFunction( 'print', printfunc )
        context.makeFunction( '+', SumFunc() )
        context.makeFunction( 'sum', SumFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'print 1 + 2' )

        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret, None )
        self.assertEqual( printfunc.output[0], '3' )

    def testBinOpePlus_04(self):
        context = LGContext()
        printfunc = PrintFunc()
        context.makeFunction( 'print', printfunc )
        context.makeFunction( '+', SumFunc() )
        context.makeFunction( 'sum', SumFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( '1 + 2 + sum 3 4' )

        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 10 )
        self.assertEqual( type(ret), LGNumWord )

    def testBinOpePlus_Group(self):
        context = LGContext()
        printfunc = PrintFunc()
        context.makeFunction( 'print', printfunc )
        context.makeFunction( '+', SumFunc() )
        context.makeFunction( 'sum', SumFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( '1 + (2 + 3) + 4' )

        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 10 )
        self.assertEqual( type(ret), LGNumWord )


    def testBinOpeMinusPlus(self):
        context = LGContext()
        printfunc = PrintFunc()
        context.makeFunction( 'print', printfunc )
        context.makeFunction( '+', SumFunc() )
        context.makeFunction( 'sum', SumFunc() )
        context.makeFunction( '-', DifferenceFunc() )
        context.makeFunction( 'defference', DifferenceFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( '1 + 2 - 3 + 4' )

        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 4 )
        self.assertEqual( type(ret), LGNumWord )


    def testBinOpeMinus_01(self):
        context = LGContext()
        printfunc = PrintFunc()
        context.makeFunction( 'print', printfunc )
        context.makeFunction( '-', DifferenceFunc() )
        context.makeFunction( 'defference', DifferenceFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( '1 - 2' )

        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, -1 )
        self.assertEqual( type(ret), LGNumWord )


    def testBinOpeMinus_02(self):
        context = LGContext()
        printfunc = PrintFunc()
        context.makeFunction( 'print', printfunc )
        context.makeFunction( '-', DifferenceFunc() )
        context.makeFunction( 'defference', DifferenceFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( '10 - 2 - 3' )

        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 5 )
        self.assertEqual( type(ret), LGNumWord )

    def testBinOpeMinus_03(self):
        context = LGContext()
        printfunc = PrintFunc()
        context.makeFunction( 'print', printfunc )
        context.makeFunction( '-', DifferenceFunc() )
        context.makeFunction( 'defference', DifferenceFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( '(10 - 2) - 3' )

        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 5 )
        self.assertEqual( type(ret), LGNumWord )
