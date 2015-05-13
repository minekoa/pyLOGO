#-*- coding: shift_jis -*-

from logoElement import *
from logoScanner import *

'''
LOGOプログラム ::= { コマンド }*
コマンド       ::= 手続き名 + { 入力 }*
入力           ::= "語 | リスト | オペレーション
オペレーション ::= 手続き名 + { 入力 }*
語 : { 英数字 | 特殊記号 }*
リスト : { { 語 | リスト }* }
'''

class LGDataParser(object):
    '''まずは リストにする'''

    def parse(self, scanner):
        self.scanner = scanner
        rootlist = LGList();

        try:
            self.list_(rootlist)
        except StopIteration:
            pass

        return rootlist

    def list_(self, currentlist):
        while True:
            self.scanner.advance()
            toktype = self.scanner.getTokenType()
            tokval  = self.scanner.getTokenValue()

            if toktype == LGTokenType.Word:
                currentlist.append( LGWord(tokval) )
            if toktype == LGTokenType.QWrd:
                currentlist.append( LGQuoWord(tokval) )
            if toktype == LGTokenType.NWrd:
                currentlist.append( LGNumWord(tokval) )
            if toktype == LGTokenType.DWrd:
                currentlist.append( LGDotWord(tokval) )
            if toktype == LGTokenType.BOpe:
                currentlist.append( LGBinOpe(tokval) )

            if toktype == LGTokenType.LOpn:
                currentlist.append( LGList() )
                self.list_( currentlist[-1] )
            if toktype == LGTokenType.LCls:
                return

            if toktype == LGTokenType.GOpn:
                currentlist.append( LGGroup() )
                self.group( currentlist[-1] )
            if toktype == LGTokenType.GCls:
                raise LGRuntimeError("unexpected ')'")

    def group(self, currentgroup):
        while True:
            self.scanner.advance()
            toktype = self.scanner.getTokenType()
            tokval  = self.scanner.getTokenValue()

            if toktype == LGTokenType.Word:
                currentgroup.append( LGWord(tokval) )
            if toktype == LGTokenType.QWrd:
                currentgroup.append( LGQuoWord(tokval) )
            if toktype == LGTokenType.NWrd:
                currentgroup.append( LGNumWord(tokval) )
            if toktype == LGTokenType.DWrd:
                currentgroup.append( LGDotWord(tokval) )
            if toktype == LGTokenType.BOpe:
                currentgroup.append( LGBinOpe(tokval) )

            if toktype == LGTokenType.LOpn:
                currentgroup.append( LGList() )
                self.list_( currentgroup[-1] )
            if toktype == LGTokenType.LCls:
                raise LGRuntimeError("unexpected ']'")

            if toktype == LGTokenType.GOpn:
                currentgroup.append( LGGroup() )
                self.group( currentgroup[-1] )
            if toktype == LGTokenType.GCls:
                return



class LGProgramParser(object):
    def __init__(self, context):
        self.context = context

    def initSource(self, list_):
        class Scanner(object):
            def __init__(self, list_):
                self.list_ = list_
                self.cnt   = -1
            def advance(self):
                self.cnt += 1
                if self.cnt >= len(self.list_.values):
                    raise StopIteration
            def getElement(self): return self.list_[self.cnt]
            def nextElement(self): return self.list_[self.cnt +1]


        self.scanner = Scanner( list_ )

    def parse(self, list_):
        self.initSource(list_)
        return self.program()

    def program(self):
        ''' LOGOプログラム ::= {式}*'''
        prg = LGProgram()
        try:
            while True:
                prg.appendExpression( self.expression() )
        except StopIteration:
            pass
        return prg


    def expression(self):
        '''式 ::= 項 | {項 加減二項オペレーション}*'''
        fstret = self.term()

        while True:
            try:
                elm = self.scanner.nextElement()
            except IndexError:
                return fstret

            if type(elm) == LGBinOpe and elm.opetype == '+-':
                fstret = self.addsubBinOperation(fstret)
            else:
                return fstret

    def term(self):
        '''項 ::= 因子 | {因子 乗除二項オペレーション}*'''
        fstret = self.factor()

        while True:
            try:
                elm = self.scanner.nextElement()
            except IndexError:
                return fstret

            if type(elm) == LGBinOpe and elm.opetype == '*/':
                fstret = self.muldivBinOperation(fstret)
            else:
                return fstret

    def addsubBinOperation(self, rval):
        '''加減二項オペレーション ::= 加減二項演算子 項'''
        # 手続き名
        self.scanner.advance()
        elm = self.scanner.getElement()
        if type(elm) != LGBinOpe or elm.opetype != '+-':
            raise LGRuntimeError("parse error (addition-substraction binary operation)")
        ope = LGOperation( elm.value )
        ope.appendArgument( rval )
        try:
            ope.appendArgument( self.term() )
        except StopIteration:
            raise LGRuntimeError('not enough inputs to %s' % ope.name )
        return ope


    def factor(self):
        '''因子 ::= "語 | 数値語 | :語 | リスト | オペレーション | グループ '''
        try:
            elm = self.scanner.nextElement()
        except IndexError:
            raise StopIteration

        if (type(elm) == LGQuoWord or
            type(elm) == LGNumWord or
            type(elm) == LGDotWord or
            type(elm) == LGList):
            self.scanner.advance()
            return self.scanner.getElement()
        if type(elm) == LGWord:
            return self.operation()
        if type(elm) == LGGroup:
            self.scanner.advance()
            return self.parseGroup( self.scanner.getElement() )
        raise LGRuntimeError('parse error (factor) %s' % type(elm) )


    def muldivBinOperation(self, rval):
        '''乗除二項オペレーション ::= 乗除二項演算子 因子'''
        # 手続き名
        self.scanner.advance()
        elm = self.scanner.getElement()
        if type(elm) != LGBinOpe or elm.opetype != '*/':
            raise LGRuntimeError("parse error (multi-division binary operation)")
        ope = LGOperation( elm.value )
        ope.appendArgument( rval )
        try:
            ope.appendArgument( self.factor() )
        except StopIteration:
            raise LGRuntimeError('not enough inputs to %s' % ope.name )
        return ope


    def operation(self):
        '''オペレーション ::= 手続き名 {式}* '''
        # 手続き名
        self.scanner.advance()
        elm = self.scanner.getElement()
        if type(elm) != LGWord:
            raise LGRuntimeError("parse error (operation)")
        ope = LGOperation( elm.value )

        # 式
        func = self.context.findFunction( ope.name )
        for i in range(0, func.requieredArgCount()):
            try:
                ope.appendArgument( self.expression() )
            except StopIteration:
                raise LGRuntimeError('not enough inputs to %s' % ope.name )
        return ope

    def parseGroup(self, grp):
        if type(grp) != LGGroup:
            raise LGRuntimeError("parse error (operation) %s" % type(grp))
        parser = LGProgramParser( self.context )
        parser.initSource(grp)
        return parser.group( len(grp.values) -1)

    def group(self, argc):
        '''グループ ::= グループオペレーション | 二項演算グルーピング | "語 | 数値語 | :語 | リスト'''
        elm = self.scanner.nextElement()
        if type(elm) == LGWord:
            return self.groupOperation(argc)
        if argc != 0:
            return self.groupingBinOperation()
        if (type(elm) == LGQuoWord or
            type(elm) == LGNumWord or
            type(elm) == LGDotWord or
            type(elm) == LGList):
            if argc != 0: raise LGRuntimeError("too much inside ()'s")
            self.scanner.advance()
            return self.scanner.getElement()
        raise LGRuntimeError('parse error (group) %s' % type(elm) )

    def groupOperation(self, argc):
        '''グループオペレーション ::=  手続き名 {式}*'''
        # 手続き名
        self.scanner.advance()
        elm = self.scanner.getElement()
        if type(elm) != LGWord:
            raise LGRuntimeError("parse error (operation)")
        ope = LGOperation( elm.value )

        # 式
        func = self.context.findFunction( ope.name )
        while True:
            try:
                ope.appendArgument( self.expression() )
            except StopIteration:
                break
#            except IndexError:
#                raise LGRuntimeError('not enough inputs to %s' % ope.name )

        return ope

    def groupingBinOperation(self):
        '''二項演算グルーピング ::=
        オペレーションを除く項 二項オペレーション {項 二項オペレーション}+ '''
        if type(self.scanner.nextElement()) == LGOperation:
            raise LGRuntimeError("parse error (grouping bin operator)")

        fstret = self.term()

        while True:
            try:
                elm = self.scanner.nextElement()
            except IndexError:
                if type(fstret) == LGOperation:	# * or / を想定
                    return fstret
                else:
                    raise LGRuntimeError("parse error (grouping bin operator)")

            if type(elm) == LGBinOpe and elm.opetype == '+-':
                fstret = self.addsubBinOperation(fstret)
            else:
                raise LGRuntimeError("too much inside ()'s")
