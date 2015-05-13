#-*- coding: shift_jis -*-

import unittest
from logoPrimitiveFunctions import *
from logoParser import *
from logoScanner import *
from logoContext import *


class PrintForTest( PrintFunc ):
    def __init__(self):
        self.output = []
    def print_(self,value):
        self.output.append( value )


class LogoPrimitiveFunctionsTest(unittest.TestCase):

    def testPrintQuoWord(self):
        context = LGContext()
        printfunc = PrintForTest()
        context.makeFunction( 'print', printfunc )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'print "hello' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret, None )
        self.assertEqual( printfunc.output[0], 'hello' )

    def testPrintNumWord(self):
        context = LGContext()
        printfunc = PrintForTest()
        context.makeFunction( 'print', printfunc )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'print 42' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret, None )
        self.assertEqual( printfunc.output[0], '42' )

    def testPrintSentence(self):
        context = LGContext()
        printfunc = PrintForTest()
        context.makeFunction( 'print', printfunc )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'print [hello world]' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret, None )
        self.assertEqual( printfunc.output[0], 'hello world' )

    def testSumIntArg(self):
        context = LGContext()
        context.makeFunction( 'sum', SumFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'sum 1 2' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 3 )
        self.assertEqual( type(ret), LGNumWord )

    def testSumRealArg(self):
        context = LGContext()
        context.makeFunction( 'sum', SumFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'sum 1.1 2.1' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 3.2 )
        self.assertEqual( type(ret), LGNumWord )

    def testSumIntStrArg(self):
        context = LGContext()
        context.makeFunction( 'sum', SumFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'sum "1 "2' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 3 )
        self.assertEqual( type(ret), LGNumWord )

    def testSumRealStrArg(self):
        context = LGContext()
        context.makeFunction( 'sum', SumFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'sum "1.1 "2.1' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 3.2 )
        self.assertEqual( type(ret), LGNumWord )

    def testSumGroupingArg(self):
        context = LGContext()
        context.makeFunction( 'sum', SumFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( '(sum 1 2 3 4)' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 10 )
        self.assertEqual( type(ret), LGNumWord )


    def testDifferenceIntArg(self):
        context = LGContext()
        context.makeFunction( 'difference', DifferenceFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'difference 5 3' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 2 )
        self.assertEqual( type(ret), LGNumWord )


    def testDifferenceRealArg(self):
        context = LGContext()
        context.makeFunction( 'difference', DifferenceFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'difference 5.5 3.1' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 2.4 )
        self.assertEqual( type(ret), LGNumWord )


    def testDifferenceIntStrArg(self):
        context = LGContext()
        context.makeFunction( 'difference', DifferenceFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'difference "5 "3' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 2 )
        self.assertEqual( type(ret), LGNumWord )

    def testDifferenceRealStrArg(self):
        context = LGContext()
        context.makeFunction( 'difference', DifferenceFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'difference "5.5 "3.1' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 2.4 )
        self.assertEqual( type(ret), LGNumWord )

    def testReminderFunc(self):
        context = LGContext()
        context.makeFunction( 'reminder', ReminderFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'reminder 10 3' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 1 )
        self.assertEqual( type(ret), LGNumWord )


    def testMakeVar(self):
        context = LGContext()
        context.makeFunction( 'make', MakeFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'make "hoge 42' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret, None )

        scanner = LGScanner( ':hoge' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 42 )
        self.assertEqual( type(ret), LGNumWord )


    def testListRun(self):
        context = LGContext()
        printfunc = PrintForTest()
        context.makeFunction( 'print', printfunc )
        context.makeFunction( 'run', RunFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'run[print "hello]' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret, None )
        self.assertEqual( printfunc.output[0], 'hello' )


    def testDefineFunctionNoArg(self):
        context = LGContext()
        context.makeFunction( 'define', DefineFunc() )
        printfunc = PrintForTest()
        context.makeFunction( 'print', printfunc )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'define "hoge [[][print "hello]]' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret, None )
        self.assertEqual( len(printfunc.output), 0 )

        scanner = LGScanner( 'hoge' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret, None )
        self.assertEqual( printfunc.output[0], 'hello' )


    def testDefineFunctionArg(self):
        context = LGContext()
        context.makeFunction( 'define', DefineFunc() )
        context.makeFunction( 'sum', SumFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        scanner = LGScanner( 'define "inc [[arg1][sum :arg1 1]]' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret, None )

        scanner = LGScanner( 'inc 42' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 43 )
        self.assertEqual( type(ret), LGNumWord )

    def testThingFunction(self):
        context = LGContext()
        context.makeFunction( 'make', MakeFunc() )
        context.makeFunction( 'thing', ThingFunc() )

        dparser = LGDataParser()
        pparser = LGProgramParser( context )

        #act1: make
        scanner = LGScanner( 'make "hoo 42' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret, None )

        #act2: thing

        scanner = LGScanner( 'thing "hoo' )
        lst = dparser.parse(scanner)
        tre = pparser.parse( lst )
        ret = tre.evaluate( context )

        self.assertEqual( ret.value, 42 )
        self.assertEqual( type(ret), LGNumWord )


