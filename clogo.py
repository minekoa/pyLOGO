#-*- coding: shift_jis -*-

from logoParser import *
from logoScanner import *
from logoContext import *

from logoPrimitiveFunctions import *


if __name__ == '__main__':

    context = LGContext()
    context.makeFunction( '+', SumFunc() )
    context.makeFunction( '-', DifferenceFunc() )
    context.makeFunction( '*', ProductFunc() )
    context.makeFunction( '/', QuotientFunc() )
    context.makeFunction( 'sum', SumFunc() )
    context.makeFunction( 'defference', DifferenceFunc() )
    context.makeFunction( 'product', ProductFunc() )
    context.makeFunction( 'quotient', QuotientFunc() )
    context.makeFunction( 'print', PrintFunc() )
    context.makeFunction( 'make', MakeFunc() )
    context.makeFunction( 'thing', ThingFunc() )
    context.makeFunction( 'run', RunFunc() )
    context.makeFunction( 'define', DefineFunc() )

    dparser = LGDataParser()
    pparser = LGProgramParser( context )

    while True:
        source = raw_input( '>>>' )

        try:
            scanner = LGScanner( source )
            lst = dparser.parse(scanner)
            tre = pparser.parse( lst )
            ret = tre.evaluate( context )
            if ret != None:
                print( "You don't say what to do with %s" % ret )
        except LGRuntimeError, err:
            print( err )


