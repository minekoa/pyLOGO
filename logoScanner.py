#-*- coding: shift_jis -*-
import re
from logoError import *


class LGTokenType(object):

    Word  = "Word"          # 語
    QWrd  = "QuoWord"       # quote (") + 語
    DWrd  = "DotWord"       # dot(:) + 語
    NWrd  = "NumWord"       # 語(数字のみで構成された語)
    LOpn  = "ListOpen"      # List 開くカッコ
    LCls  = "ListClose"     # List 閉じるカッコ
    GOpn  = "GroupingOpen"  # グルーピング 開くカッコ
    GCls  = "GroupingClose" # グルーピング 閉じるカッコ
    BOpe  = "BinaryOperator"# 二項演算子

    def __init__(self):
        self.wordptn  = re.compile( r"[a-zA-Z0-9_\.]+$" );
        self.qwrdptn  = re.compile( r"\"[a-zA-Z0-9_\.\+\-]+$" );
        self.dwrdptn  = re.compile( r"\:[a-zA-Z0-9_\.]+$" );
        self.nwrdptn  = re.compile( r"[+-]?[0-9]+\.?[0-9]*$" );
        self.lopnptn  = re.compile( r"\[" );
        self.lclsptn  = re.compile( r"\]" );
        self.gopnptn  = re.compile( r"\(" );
        self.gclsptn  = re.compile( r"\)" );
        self.bopeptn  = re.compile( r"[+\-\/\*\<\>\=]" )

    def typeOf(self, token):
        if self.nwrdptn.match( token ): return LGTokenType.NWrd
        if self.qwrdptn.match( token ): return LGTokenType.QWrd
        if self.dwrdptn.match( token ): return LGTokenType.DWrd
        if self.bopeptn.match( token ): return LGTokenType.BOpe
        if self.wordptn.match( token ): return LGTokenType.Word
        if self.lopnptn.match( token ): return LGTokenType.LOpn
        if self.lclsptn.match( token ): return LGTokenType.LCls
        if self.gopnptn.match( token ): return LGTokenType.GOpn
        if self.gclsptn.match( token ): return LGTokenType.GCls
        raise LGRuntimeError( 'unknown token type "%s"' % token )

class LGScanner(object):
    def __init__(self, source):
        self.typeJudger = LGTokenType()

        self.separatorPtn = re.compile( r"[ \t\(\)\[\]]" )
        self.brankPtn     = re.compile( r"[ \t]" )

        self.source     = source
        self.tokenValue = None
        self.tokenType  = None
        self.cursor     = 0

    def skipBrank(self):
        try:
            while True:
                if not self.brankPtn.match( self.source[self.cursor] ):
                   break
                self.cursor += 1
        except IndexError:
            raise StopIteration

    def advance(self):
        if self.cursor >= len(self.source):
            raise StopIteration;

        self.skipBrank()
        headCursor = self.cursor

        if self.separatorPtn.match( self.source[headCursor] ):
            self.tokenValue = self.source[headCursor]
            self.tokenType  = self.typeJudger.typeOf( self.tokenValue )
            self.cursor += 1
            return

        while True:
            self.cursor += 1
            try:
                if self.separatorPtn.match( self.source[self.cursor] ): break
            except IndexError:
                break


        self.tokenValue = self.source[headCursor : self.cursor]
        self.tokenType  = self.typeJudger.typeOf( self.tokenValue )


    def getTokenType(self): return self.tokenType
    def getTokenValue(self): return self.tokenValue


class LGEzScanner(object):
    def __init__(self, source):
        toktype = LGTokenType()
        self.tokenGenarator = ((i, toktype.typeOf(i)) for i in source.split())
        self.tokenValue = None
        self.tokenType  = None

    def advance(self):
        self.tokenValue, self.tokenType = self.tokenGenarator.next()

    def getTokenType(self): return self.tokenType
    def getTokenValue(self): return self.tokenValue



    