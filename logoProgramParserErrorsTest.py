#-*- coding: shift_jis -*-

import unittest
from logoScanner import *
from logoParser import *
from logoContext import *

class DummyFunction(object):
    def __init__(self, argc):
        self.argc = argc
    def requieredArgCount(self): return self.argc

class LogoProgramParserErrorsTest(unittest.TestCase):

    def testNotEnoughInputsInOperation(self):
        source= LGList()
        source.append( LGWord('sum') )
        source.append( LGNumWord(1) )

        context = LGContext()
        context.makeFunction( 'sum', DummyFunction(2) )

        parser = LGProgramParser(context)

        try:
            ret = parser.parse( source )
            self.fail( 'not raise exception' )
        except LGRuntimeError, err:
            self.assertEqual( err.__str__(), 'not enough inputs to sum' )


    def testNotEnoughInputsInBinOperation(self):
        source= LGList()
        source.append( LGNumWord(1) )
        source.append( LGWord('+') )

        context = LGContext()
        context.makeFunction( '+', DummyFunction(2) )

        parser = LGProgramParser(context)

        try:
            ret = parser.parse( source )
            self.fail( 'not raise exception' )
        except LGRuntimeError, err:
            self.assertEqual( err.__str__(), 'not enough inputs to +' )

    def testToMuchInside(self):
        source= LGList()
        grp   = LGGroup()
        grp.append( LGNumWord(1) )
        grp.append( LGNumWord(2) )
        grp.append( LGNumWord(3) )
        grp.append( LGNumWord(4) )
        source.append( grp )

        context = LGContext()

        parser = LGProgramParser(context)

        try:
            ret = parser.parse( source )
            self.fail( 'not raise exception' )
        except LGRuntimeError, err:
            self.assertEqual( err.__str__(), "too much inside ()'s")


    def testIDontKnowHowTo(self):
        source= LGList()
        source.append( LGWord('hoge') )

        context = LGContext()

        parser = LGProgramParser(context)

        try:
            ret = parser.parse( source )
            self.fail( 'not raise exception' )
        except LGRuntimeError, err:
            self.assertEqual( err.__str__(), "I don't know how  to hoge")


    def testIDontKnowHowToUpperLower(self):
        source= LGList()
        source.append( LGWord('HoGe') )

        context = LGContext()

        parser = LGProgramParser(context)

        try:
            ret = parser.parse( source )
            self.fail( 'not raise exception' )
        except LGRuntimeError, err:
            self.assertEqual( err.__str__(), "I don't know how  to HoGe")


    def testIDontKnowHowToInGrp(self):
        # これはパーズエラーにならなくても良いかもしれない
        # （実行時エラーにすべきか？）→未定義で
        source= LGList()
        grp   = LGGroup()
        grp.append( LGWord('hoge') )
        source.append( grp )

        context = LGContext()

        parser = LGProgramParser(context)

        try:
            ret = parser.parse( source )
            self.fail( 'not raise exception' )
        except LGRuntimeError, err:
            self.assertEqual( err.__str__(), "I don't know how  to hoge")
