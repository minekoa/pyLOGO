#-*- coding: shift_jis -*-

from logoParser import *
from logoScanner import *
from logoContext import *

class SumFunc(object):
    def requieredArgCount(self): return 2
    def evaluate(self, context, args):
        ret = 0
        for i in args: ret += i.value
        return LGNumWord( ret )

class PrintFunc(object):
    def requieredArgCount(self): return 1
    def evaluate(self, context, args):
        if ( type(args[0]) == LGQuoWord or
             type(args[0]) == LGNumWord ):
            print( args[0].thing().__str__() )
        if type(args[0]) == LGList:
            print( args[0].__str__()[1:-1] )

class MakeFunc(object):
    def requieredArgCount(self): return 2
    def evaluate(self, context, args):
        if type(args[0]) != LGQuoWord: raise LGInputError( args[0] )
        context.makeVariable( args[0].thing().value, args[1] )

if __name__ == '__main__':
    context = LGContext()
    context.makeFunction( 'sum', SumFunc() )
    context.makeFunction( 'print', PrintFunc() )
    context.makeFunction( 'make', MakeFunc() )

    dparser = LGDataParser()
    pparser = LGProgramParser( context )

    while True:
        source = raw_input( '>>>' )

        try:
            scanner = LGEzScanner( source )
            lst  = dparser.parse( scanner )
            tree = pparser.parse( lst )
            ret  = tree.evaluate( context )
            if ret != None:
                print( "You don't say what to do with %s" % ret )
        except LGRuntimeError, err:
            print( err )

