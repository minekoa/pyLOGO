#-*- coding: shift_jis -*-

from logoError import *
from logoElement import *
from logoContext import *
import math

from logoElement import _asNum
from logoElement import _asSymbol

class SumFunc(object):
    def requieredArgCount(self): return 2
    def evaluate(self, context, args):
        ret = 0
        for i in args:
            ret += _asNum(i)
        return LGNumWord( ret )

class DifferenceFunc(object):
    def requieredArgCount(self): return 2
    def evaluate(self, context, args):
        ret = _asNum(args[0])
        for i in args[1:]:
            ret -= _asNum(i)
        return LGNumWord( ret )

class ProductFunc(object):
    def requieredArgCount(self): return 2
    def evaluate(self, context, args):
        ret = _asNum(args[0])
        for i in args[1:]:
            ret *= _asNum(i)
        return LGNumWord( ret )

class QuotientFunc(object):
    def requieredArgCount(self): return 2
    def evaluate(self, context, args):
        ret = _asNum(args[0])
        for i in args[1:]:
            ret /= _asNum(i)
        return LGNumWord( ret )

class ReminderFunc(object):
    def requieredArgCount(self): return 2
    def evaluate(self, context, args):
        return LGNumWord( _asNum(args[0]) % _asNum(args[1]) )

class IntFunc(object):
    def requieredArgCount(self): return 1
    def evaluate(self, context, args):
        return LGNumWord( int(_asNum(arg[0])) )

class RoundFunc(object):
    def requieredArgCount(self): return 1
    def evaluate(self, context, args):
        return LGNumWord( round(_asNum(arg[0])) )

class PiFunc(object):
    def requieredArgCount(self): return 0
    def evaluate(self, context, args):
        return LGNumWord(math.pi)

class SqrtFunc(object):
    def requieredArgCount(self): return 1
    def evaluate(self, context, args):
        return LGNumWord( math.sqrt(_asNum(args[0])) )

class SinFunc(object):
    def requieredArgCount(self): return 1
    def evaluate(self, context, args):
        return LGNumWord( math.sin(_asNum(args[0])) )

class CosFunc(object):
    def requieredArgCount(self): return 1
    def evaluate(self, context, args):
        return LGNumWord( math.cos(_asNum(args[0])) )

class TanFunc(object):
    def requieredArgCount(self): return 1
    def evaluate(self, context, args):
        return LGNumWord( math.tan(_asNum(args[0])) )

class ArctanFunc(object):
    def requieredArgCount(self): return 1
    def evaluate(self, context, args):
        return LGNumWord( math.atan(_asNum(args[0])) )

class PrintFunc(object):
    def requieredArgCount(self): return 1
    def evaluate(self, context, args):
        if type(args[0]) == LGQuoWord:
            self.print_( args[0].value[1:] )
        if type(args[0]) == LGNumWord:
            self.print_( args[0].__str__() )
        if type(args[0]) == LGList:
            self.print_( args[0].__str__()[1:-1] )

    def print_(self, msg):
        '''出力先の切り替え用'''
        print( msg )

class MakeFunc(object):
    def requieredArgCount(self): return 2
    def evaluate(self, context, args):
        if type(args[0]) != LGQuoWord: raise LGInputError( args[0] )
        context.makeVariable( _asSymbol(args[0]), args[1] )

class LocalmakeFunc(object):
    def requieredArgCount(self): return 2
    def evaluate(self, context, args):
        if type(args[0]) != LGQuoWord: raise LGInputError( args[0] )
        context.makeLocalVariable( _asSymbol(args[0]), args[1] )

class ThingFunc(object):
    def requieredArgCount(self): return 1
    def evaluate(self, context, args):
        if type(args[0]) != LGQuoWord: raise LGInputError( args[0] )
        return context.findVariable( _asSymbol(args[0]) )

class RunFunc(object):
    def requieredArgCount(self): return 1
    def evaluate(self, context, args):
        if type(args[0]) != LGList: raise LGInputError( args[0] )
        return args[0].run(context)

class RepeatFunc(object):
    def requieredArgCount(self): return 2
    def evaluate(self, context, args):
        if type(args[1]) != LGList: raise LGInputError( args[1] )

        ret = None
        for i in range (0, _asNum(args[0])):
            ret = args[1].run( context )
        return ret



class LogoFunction(object):
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def requieredArgCount(self): return len(self.args)

    def evaluate(self, context, args):
        newContext = LGContext( context )
        for i in range(0, self.requieredArgCount()):
            newContext.makeLocalVariable( self.args[i].value, args[i] )

        ret = None
        for line in self.body:
            ret = line.run(newContext)
        return ret
#        return self.body.run(newContext)



class DefineFunc(object):
    def requieredArgCount(self): return 2
    def evaluate(self, context, args):
        '''
        define "opeFoo [[arg1 arg2]
                        [make "hoge sum thing "arg1  256]
                        [output prduct thing "hoge arg2]]
        '''
        if type(args[0]) != LGQuoWord: raise LGInputError( args[0] )
        if type(args[1]) != LGList:  raise LGInputError( args[1] )
        body = LGList()
        for i in args[1][1:]:
            body.append(i)
        func = LogoFunction( args[1][0].values, body)
        context.makeFunction(_asSymbol(args[0]), func)

if __name__ == '__main__':
    print dir()
    raw_input('pause')

