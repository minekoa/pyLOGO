#-*- coding: shift_jis -*-

import unittest
from logoScanner import *
from logoParser import *
from logoContext import *

class DummyFunction(object):
    def __init__(self, argc):
        self.argc = argc
    def requieredArgCount(self): return self.argc

class LogoProgramParserTest(unittest.TestCase):

    def test1ArgCommand(self):
        source= LGList()
        source.append( LGWord('print') )
        source.append( LGQuoWord('"hello') )

        context = LGContext()
        context.makeFunction( 'print', DummyFunction(1) )

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )

        self.assertEqual( ret.expressions[0].name, 'print' )
        self.assertEqual( type(ret.expressions[0]), LGOperation )
        self.assertEqual( len(ret.expressions[0].args), 1 )

        print_args = ret.expressions[0].args

        self.assertEqual( print_args[0].value, '"hello' )
        self.assertEqual( type(print_args[0]), LGQuoWord )

    def test2WordCommand(self):
        source= LGList()
        source.append( LGWord('sum') )
        source.append( LGNumWord('1') )
        source.append( LGNumWord('2') )

        context = LGContext()
        context.makeFunction( 'sum', DummyFunction(2) )

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )

        self.assertEqual( ret.expressions[0].name, 'sum' )
        self.assertEqual( type(ret.expressions[0]), LGOperation )
        self.assertEqual( len(ret.expressions[0].args), 2 )

        sum_args = ret.expressions[0].args

        self.assertEqual( sum_args[0].value, 1 )
        self.assertEqual( type(sum_args[0]), LGNumWord )

        self.assertEqual( sum_args[1].value, 2 )
        self.assertEqual( type(sum_args[1]), LGNumWord )

    def testOperationArgCommand(self):
        # print sum 1 2
        #     -> (print (sum 1 2))
        source= LGList()
        source.append( LGWord('print') )
        source.append( LGWord('sum') )
        source.append( LGNumWord('1') )
        source.append( LGNumWord('2') )

        context = LGContext()
        context.makeFunction( 'print', DummyFunction(1) )
        context.makeFunction( 'sum', DummyFunction(2) )

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )

        self.assertEqual( ret.expressions[0].name, 'print' )
        self.assertEqual( type(ret.expressions[0]), LGOperation )
        self.assertEqual( len(ret.expressions[0].args), 1 )

        print_args = ret.expressions[0].args

        self.assertEqual( print_args[0].name, 'sum' )
        self.assertEqual( type(print_args[0]), LGOperation )
        self.assertEqual( len(print_args[0].args), 2 )

        sum_args = print_args[0].args

        self.assertEqual( sum_args[0].value, 1 )
        self.assertEqual( type(sum_args[0]), LGNumWord )

        self.assertEqual( sum_args[1].value, 2 )
        self.assertEqual( type(sum_args[1]), LGNumWord )

    def testOpeOpeArgCommand(self):
        # sum sum 1 2 3
        #     -> (sum (sum 1 2) 3)
        source= LGList()
        source.append( LGWord('sum') )
        source.append( LGWord('sum') )
        source.append( LGNumWord('1') )
        source.append( LGNumWord('2') )
        source.append( LGNumWord('3') )

        context = LGContext()
        context.makeFunction( 'sum', DummyFunction(2) )

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )

        self.assertEqual( ret.expressions[0].name, 'sum' )
        self.assertEqual( type(ret.expressions[0]), LGOperation )
        self.assertEqual( len(ret.expressions[0].args), 2 )

        sumA_args = ret.expressions[0].args

        self.assertEqual( sumA_args[0].name, 'sum' )
        self.assertEqual( type(sumA_args[0]), LGOperation )
        self.assertEqual( len(sumA_args[0].args), 2 )

        sumB_args = sumA_args[0].args

        self.assertEqual( sumB_args[0].value, 1 )
        self.assertEqual( type(sumB_args[0]), LGNumWord )

        self.assertEqual( sumB_args[1].value, 2 )
        self.assertEqual( type(sumB_args[1]), LGNumWord )

        self.assertEqual( sumA_args[1].value, 3 )
        self.assertEqual( type(sumA_args[1]), LGNumWord )

    def testListArgCommand(self):
        # print["hello "world]
        #     -> (print ("hello "world))
        source= LGList()
        source.append( LGWord('print') )
        param = LGList()
        param.append( LGQuoWord('"hello') )
        param.append( LGQuoWord('"world') )
        source.append( param )

        context = LGContext()
        context.makeFunction( 'print', DummyFunction(1) )

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )

        self.assertEqual( ret.expressions[0].name, 'print' )
        self.assertEqual( type(ret.expressions[0]), LGOperation )
        self.assertEqual( len(ret.expressions[0].args), 1 )

        print_args = ret.expressions[0].args

        self.assertEqual( type(print_args[0]), LGList )
        self.assertEqual( len(print_args[0].values), 2 )

        arglist = print_args[0]

        self.assertEqual( arglist[0].value, '"hello' )
        self.assertEqual( type(arglist[0]), LGQuoWord )

        self.assertEqual( arglist[1].value, '"world' )
        self.assertEqual( type(arglist[1]), LGQuoWord )

    def testGroupArgCommand(self):
        # sum (sum 1 2 3) 4
        source = LGList()
        source.append( LGWord('sum') )
        param = LGGroup()
        param.append( LGWord('sum') )
        param.append( LGNumWord(1) )
        param.append( LGNumWord(2) )
        param.append( LGNumWord(3) )
        source.append( param )
        source.append( LGNumWord(4) )

        context = LGContext()
        context.makeFunction( 'sum', DummyFunction(2) )

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )

        self.assertEqual( ret.expressions[0].name, 'sum' )
        self.assertEqual( type(ret.expressions[0]), LGOperation )
        self.assertEqual( len(ret.expressions[0].args), 2 )

        sumA_args = ret.expressions[0].args

        self.assertEqual( sumA_args[0].name, 'sum' )
        self.assertEqual( type(sumA_args[0]), LGOperation)
        self.assertEqual( len(sumA_args[0].args), 3 )

        sumB_args = sumA_args[0].args

        self.assertEqual( sumB_args[0].value, 1)
        self.assertEqual( type(sumB_args[0]), LGNumWord )

        self.assertEqual( sumB_args[1].value, 2)
        self.assertEqual( type(sumB_args[1]), LGNumWord )

        self.assertEqual( sumB_args[2].value, 3)
        self.assertEqual( type(sumB_args[2]), LGNumWord )

        self.assertEqual( sumA_args[1].value, 4 )
        self.assertEqual( type(sumA_args[1]), LGNumWord  )


    def testGroupQuoWordOnly(self):
        # print ("hello)
        # -> print "hello
        source = LGList()
        source.append( LGWord('print') )
        param = LGGroup()
        param.append( LGQuoWord('"hello') )
        source.append( param )

        context = LGContext()
        context.makeFunction( 'print', DummyFunction(1) )

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )

        self.assertEqual( ret.expressions[0].name, 'print' )
        self.assertEqual( type(ret.expressions[0]), LGOperation )
        self.assertEqual( len(ret.expressions[0].args), 1 )

        print_args = ret.expressions[0].args

        self.assertEqual( print_args[0].value, '"hello' )
        self.assertEqual( type(print_args[0]), LGQuoWord )

    def testGroupNumWordOnly(self):
        # print (42)
        # -> print 42
        source = LGList()
        source.append( LGWord('print') )
        param = LGGroup()
        param.append( LGNumWord(42) )
        source.append( param )

        context = LGContext()
        context.makeFunction( 'print', DummyFunction(1) )

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )

        self.assertEqual( ret.expressions[0].name, 'print' )
        self.assertEqual( type(ret.expressions[0]), LGOperation )
        self.assertEqual( len(ret.expressions[0].args), 1 )

        print_args = ret.expressions[0].args

        self.assertEqual( print_args[0].value, 42 )
        self.assertEqual( type(print_args[0]), LGNumWord )


    def testAddSubBinOpeCommand(self):
        # 1 + 2 - 3 + 4

        source = LGList()
        source.append( LGNumWord(1) )
        source.append( LGBinOpe('+') )
        source.append( LGNumWord(2) )
        source.append( LGBinOpe('-') )
        source.append( LGNumWord(3) )
        source.append( LGBinOpe('+') )
        source.append( LGNumWord(4) )

        context = LGContext()
        context.makeFunction( '+', DummyFunction(2) )
        context.makeFunction( '-', DummyFunction(2) )

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )

        # (+ (?) 4)
        self.assertEqual( ret.expressions[0].name, '+' )
        self.assertEqual( type(ret.expressions[0]), LGOperation )
        self.assertEqual( len(ret.expressions[0].args), 2 )

        self.assertEqual( ret.expressions[0].args[1].value,  4 )
        self.assertEqual( type(ret.expressions[0].args[1]),  LGNumWord )

        # (+ (- (?) 3) 4)
        self.assertEqual( type(ret.expressions[0].args[0]),  LGOperation )
        self.assertEqual( ret.expressions[0].args[0].name,  '-' )
        self.assertEqual( len(ret.expressions[0].args[0].args), 2 )
        op2 = ret.expressions[0].args[0]

        self.assertEqual( op2.args[1].value,  3 )
        self.assertEqual( type(op2.args[1]), LGNumWord )

        # (+ (- (+ (?) 2) 3) 4)
        self.assertEqual( type(op2.args[0]),  LGOperation )
        self.assertEqual( op2.args[0].name,  '+' )
        self.assertEqual( len(op2.args[0].args), 2 )
        op3 = op2.args[0]

        self.assertEqual( op3.args[1].value,  2 )
        self.assertEqual( type(op3.args[1]), LGNumWord )

        # (+ (- (1) 2) 3) 4)
        self.assertEqual( op3.args[0].value,  1 )
        self.assertEqual( type(op3.args[0]), LGNumWord )


    def testMulDivBinOpeCommand(self):
        # 1 * 2 / 3 * 4

        source = LGList()
        source.append( LGNumWord(1) )
        source.append( LGBinOpe('*') )
        source.append( LGNumWord(2) )
        source.append( LGBinOpe('/') )
        source.append( LGNumWord(3) )
        source.append( LGBinOpe('*') )
        source.append( LGNumWord(4) )

        context = LGContext()
        context.makeFunction( '*', DummyFunction(2) )
        context.makeFunction( '/', DummyFunction(2) )

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )

        # (* (?) 4)
        self.assertEqual( ret.expressions[0].name, '*' )
        self.assertEqual( type(ret.expressions[0]), LGOperation )
        self.assertEqual( len(ret.expressions[0].args), 2 )

        self.assertEqual( ret.expressions[0].args[1].value,  4 )
        self.assertEqual( type(ret.expressions[0].args[1]),  LGNumWord )

        # (* (/ (?) 3) 4)
        self.assertEqual( type(ret.expressions[0].args[0]),  LGOperation )
        self.assertEqual( ret.expressions[0].args[0].name,  '/' )
        self.assertEqual( len(ret.expressions[0].args[0].args), 2 )
        op2 = ret.expressions[0].args[0]

        self.assertEqual( op2.args[1].value,  3 )
        self.assertEqual( type(op2.args[1]), LGNumWord )

        # (* (/ (* (?) 2) 3) 4)
        self.assertEqual( type(op2.args[0]),  LGOperation )
        self.assertEqual( op2.args[0].name,  '*' )
        self.assertEqual( len(op2.args[0].args), 2 )
        op3 = op2.args[0]

        self.assertEqual( op3.args[1].value,  2 )
        self.assertEqual( type(op3.args[1]), LGNumWord )

        # (+ (- (1) 2) 3) 4)
        self.assertEqual( op3.args[0].value,  1 )
        self.assertEqual( type(op3.args[0]), LGNumWord )


    def testArithmeticBinOpeCommand1(self):
        # 1 + 2 * 3 - 4

        source = LGList()
        source.append( LGNumWord(1) )
        source.append( LGBinOpe('+') )
        source.append( LGNumWord(2) )
        source.append( LGBinOpe('*') )
        source.append( LGNumWord(3) )
        source.append( LGBinOpe('-') )
        source.append( LGNumWord(4) )

        context = LGContext()
        context.makeFunction( '+', DummyFunction(2) )
        context.makeFunction( '-', DummyFunction(2) )
        context.makeFunction( '*', DummyFunction(2) )
        context.makeFunction( '/', DummyFunction(2) )

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )

        # (- (?) 4)
        # ~~     ~~
        self.assertEqual( type(ret.expressions[0]), LGOperation )
        op1 = ret.expressions[0]

        self.assertEqual( op1.name, '-' )
        self.assertEqual( len(op1.args), 2 )

        self.assertEqual( op1.args[1].value,  4 )
        self.assertEqual( type(op1.args[1]),  LGNumWord )

        # (- (+ 1 (?)) 4)
        #    ~~ ~    ~
        self.assertEqual( type(op1.args[0]), LGOperation )
        op2 = op1.args[0]

        self.assertEqual( op2.name, '+' )
        self.assertEqual( len(op2.args), 2 )

        self.assertEqual( op2.args[0].value,  1 )
        self.assertEqual( type(op2.args[0]),  LGNumWord )

        # (- (+ 1 (* (?) 3)) 4)
        #         ~~     ~~
        self.assertEqual( type(op2.args[1]), LGOperation )
        op3 = op2.args[1]

        self.assertEqual( op3.name, '*' )
        self.assertEqual( len(op3.args), 2 )

        self.assertEqual( op3.args[1].value,  3 )
        self.assertEqual( type(op3.args[1]),  LGNumWord )

        # (- (+ 1 (* (2) 3)) 4)
        #            ~~~
        self.assertEqual( op3.args[0].value,  2 )
        self.assertEqual( type(op3.args[0]),  LGNumWord )

    def testArithmeticBinOpeCommandGrp(self):
        # 1 + 2 * (3 - 4 / 2)

        source = LGList()
        source.append( LGNumWord(1) )
        source.append( LGBinOpe('+') )
        source.append( LGNumWord(2) )
        source.append( LGBinOpe('*') )
        param = LGGroup()
        param.append( LGNumWord(3) )
        param.append( LGBinOpe('-') )
        param.append( LGNumWord(4) )
        param.append( LGBinOpe('/') )
        param.append( LGNumWord(2) )
        source.append( param )

        context = LGContext()
        context.makeFunction( '+', DummyFunction(2) )
        context.makeFunction( '-', DummyFunction(2) )
        context.makeFunction( '*', DummyFunction(2) )
        context.makeFunction( '/', DummyFunction(2) )

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )

        # (+ 1 (?))
        # ~~ ~    ~
        self.assertEqual( type(ret.expressions[0]), LGOperation )
        op1 = ret.expressions[0]

        self.assertEqual( op1.name, '+' )
        self.assertEqual( len(op1.args), 2 )

        self.assertEqual( op1.args[0].value,  1 )
        self.assertEqual( type(op1.args[0]),  LGNumWord )

        # (+ 1 (* 2 (?)))
        #      ~~ ~    ~
        self.assertEqual( type(op1.args[1]), LGOperation )
        op2 = op1.args[1]

        self.assertEqual( op2.name, '*' )
        self.assertEqual( len(op2.args), 2 )

        self.assertEqual( op2.args[0].value,  2 )
        self.assertEqual( type(op2.args[0]),  LGNumWord )

        # (+ 1 (* 2 (- 3 (?))))
        #           ~~ ~    ~
        self.assertEqual( type(op2.args[1]), LGOperation )
        op3 = op2.args[1]

        self.assertEqual( op3.name, '-' )
        self.assertEqual( len(op3.args), 2 )

        self.assertEqual( op3.args[0].value,  3 )
        self.assertEqual( type(op3.args[0]),  LGNumWord )

        # (+ 1 (* 2 (- 3 (/ 4 2))))
        #                ~~ ~ ~~
        self.assertEqual( type(op3.args[1]), LGOperation )
        op4 = op3.args[1]

        self.assertEqual( op4.args[0].value,  4 )
        self.assertEqual( type(op4.args[0]),  LGNumWord )

        self.assertEqual( op4.args[1].value,  2 )
        self.assertEqual( type(op4.args[1]),  LGNumWord )

    def testGrpOpArithmeticBin(self):
        # (sum 1 + 2 * 3 1 * 2 + 3 5 - 4)

        source = LGList()
        param = LGGroup()
        param.append( LGWord('sum') )
        param.append( LGNumWord(1) )
        param.append( LGBinOpe('+') )
        param.append( LGNumWord(2) )
        param.append( LGBinOpe('*') )
        param.append( LGNumWord(3) )
        param.append( LGNumWord(1) )
        param.append( LGBinOpe('*') )
        param.append( LGNumWord(2) )
        param.append( LGBinOpe('+') )
        param.append( LGNumWord(3) )
        param.append( LGNumWord(5) )
        param.append( LGBinOpe('-') )
        param.append( LGNumWord(4) )
        source.append( param )

        context = LGContext()
        context.makeFunction( 'sum', DummyFunction(2) )
        context.makeFunction( '+', DummyFunction(2) )
        context.makeFunction( '-', DummyFunction(2) )
        context.makeFunction( '*', DummyFunction(2) )
        context.makeFunction( '/', DummyFunction(2) )

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )

        # (sum (a) (b) (c))
        self.assertEqual( type(ret.expressions[0]), LGOperation )
        op1 = ret.expressions[0]
        self.assertEqual( op1.name, 'sum' )
        self.assertEqual( len(op1.args), 3 )


        # a = (+ 1 (?))
        self.assertEqual( type(op1.args[0]), LGOperation )
        op_a = op1.args[0]
        self.assertEqual( op_a.name, '+' )
        self.assertEqual( len(op_a.args), 2 )

        self.assertEqual( op_a.args[0].value,  1 )
        self.assertEqual( type(op_a.args[0]),  LGNumWord )

        # a = (+ 1 (* 2 3))
        #          ~~~~~~~
        self.assertEqual( type(op_a.args[1]), LGOperation )
        op_a1 = op_a.args[1]
        self.assertEqual( op_a1.name, '*' )
        self.assertEqual( len(op_a1.args), 2 )

        self.assertEqual( op_a1.args[0].value,  2 )
        self.assertEqual( type(op_a1.args[0]),  LGNumWord )

        self.assertEqual( op_a1.args[1].value,  3 )
        self.assertEqual( type(op_a1.args[1]),  LGNumWord )

        # b = (+ (?) 3)
        self.assertEqual( type(op1.args[1]), LGOperation )
        op_b = op1.args[1]
        self.assertEqual( op_b.name, '+' )
        self.assertEqual( len(op_b.args), 2 )

        self.assertEqual( op_b.args[1].value,  3 )
        self.assertEqual( type(op_b.args[1]),  LGNumWord )

        # b = (+ (* 1 2) 3)
        #        ~~~~~~~
        self.assertEqual( type(op_b.args[0]), LGOperation )
        op_b1 = op_b.args[0]
        self.assertEqual( op_b1.name, '*' )
        self.assertEqual( len(op_b1.args), 2 )

        self.assertEqual( op_b1.args[0].value,  1 )
        self.assertEqual( type(op_b1.args[0]),  LGNumWord )

        self.assertEqual( op_b1.args[1].value,  2 )
        self.assertEqual( type(op_b1.args[1]),  LGNumWord )

        # c = (- 5 4)
        self.assertEqual( type(op1.args[2]), LGOperation )
        op_c = op1.args[2]
        self.assertEqual( op_c.name, '-' )
        self.assertEqual( len(op_c.args), 2 )

        self.assertEqual( op_c.args[0].value,  5 )
        self.assertEqual( type(op_b1.args[0]),  LGNumWord )

        self.assertEqual( op_c.args[1].value,  4 )
        self.assertEqual( type(op_b1.args[1]),  LGNumWord )


    def testGrpAddDecBin(self):
        # (1 + 2)

        source = LGList()
        param = LGGroup()
        param.append( LGNumWord(1) )
        param.append( LGBinOpe('+') )
        param.append( LGNumWord(2) )
        source.append( param )

        context = LGContext()
        context.makeFunction( '+', DummyFunction(2) )

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )


        self.assertEqual( type(ret.expressions[0]), LGOperation )
        op1 = ret.expressions[0]
        self.assertEqual( op1.name, '+' )
        self.assertEqual( len(op1.args), 2 )
        self.assertEqual( op1.args[0].value, 1 )
        self.assertEqual( type(op1.args[0]), LGNumWord )
        self.assertEqual( op1.args[1].value, 2 )
        self.assertEqual( type(op1.args[1]), LGNumWord )

    def testGrpMulSubBin(self):
        # (1 * 2)

        source = LGList()
        param = LGGroup()
        param.append( LGNumWord(1) )
        param.append( LGBinOpe('*') )
        param.append( LGNumWord(2) )
        source.append( param )

        context = LGContext()
        context.makeFunction( '*', DummyFunction(2) )

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )


        self.assertEqual( type(ret.expressions[0]), LGOperation )
        op1 = ret.expressions[0]
        self.assertEqual( op1.name, '*' )
        self.assertEqual( len(op1.args), 2 )
        self.assertEqual( op1.args[0].value, 1 )
        self.assertEqual( type(op1.args[0]), LGNumWord )
        self.assertEqual( op1.args[1].value, 2 )
        self.assertEqual( type(op1.args[1]), LGNumWord )

    def testGrpSingleNumValue(self):
        # (1)
        source = LGList()
        param = LGGroup()
        param.append( LGNumWord(1) )
        source.append( param )

        context = LGContext()

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )


        self.assertEqual( type(ret.expressions[0]), LGNumWord )
        self.assertEqual( ret.expressions[0].value, 1 )


    def testGrpSingleQuoValue(self):
        # ("hello)
        source = LGList()
        param = LGGroup()
        param.append( LGQuoWord('"hello') )
        source.append( param )

        context = LGContext()

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )


        self.assertEqual( type(ret.expressions[0]), LGQuoWord )
        self.assertEqual( ret.expressions[0].value, '"hello' )


    def testGrpSingleWordValue(self):
        # (pi)
        source = LGList()
        param = LGGroup()
        param.append( LGWord('pi') )
        source.append( param )

        context = LGContext()
        context.makeFunction( 'pi', DummyFunction(0) )

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )


        self.assertEqual( type(ret.expressions[0]), LGOperation )
        op1 = ret.expressions[0]
        self.assertEqual( op1.name, 'pi' )
        self.assertEqual( len(op1.args), 0 )


    def testGrpUpperMatch(self):
        # (pi)
        source = LGList()
        param = LGGroup()
        param.append( LGWord('PI') )
        source.append( param )

        context = LGContext()
        context.makeFunction( 'pi', DummyFunction(0) )

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )


        self.assertEqual( type(ret.expressions[0]), LGOperation )
        op1 = ret.expressions[0]
        self.assertEqual( op1.name, 'PI' )
        self.assertEqual( len(op1.args), 0 )


    def testUpperMatch(self):
        # pi
        source = LGList()
        source.append( LGWord('PI') )

        context = LGContext()
        context.makeFunction( 'pi', DummyFunction(0) )

        parser = LGProgramParser(context)
        ret = parser.parse( source )

        self.assertEqual( type(ret), LGProgram )


        self.assertEqual( type(ret.expressions[0]), LGOperation )
        op1 = ret.expressions[0]
        self.assertEqual( op1.name, 'PI' )
        self.assertEqual( len(op1.args), 0 )




