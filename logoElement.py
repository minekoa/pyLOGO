#-*- coding:shift_jis -*-

from logoError import *

def _asNum( value ):
    '''Logoエレメントを Python数値に変換する'''
    if type(value) == LGNumWord:
        ivalue = int(value.value)
        fvalue = float(value.value)
        return ivalue if ivalue == fvalue else fvalue

    if type(value) == LGQuoWord:
        try:
            return int(value.value[1:])
        except ValueError:
            try:
                return float(value.value[1:])
            except ValueError:
                pass
    raise LGInputError(value)


def _asSymbol( value ):
    '''Logoエレメントを Python文字列（Logoシンボル用）に変換する'''
    if type(value) == LGQuoWord:
        return value.value[1:].lower()
    if type(value) == LGWord:
        return value.value.lower()
    raise LGInputError(value)



class LGWord( object ):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        raise LGRuntimeError( 'not-evalutable-exception' )

    def __str__(self):
        return self.value

class LGQuoWord( object ):
    ''' "語 '''
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        return self

    def __str__(self):
        return self.value

class LGDotWord( object ):
    ''' :語 '''
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        return context.findVariable( self.value[1:].lower() )

    def __str__(self):
        return self.value

class LGNumWord( object ):
    def __init__(self, value):
        ''' 引数 value は 文字列でも 数値でも OK! '''
        self.vstr  = str(value)
        try:
            ivalue = int(value)
            fvalue = float(value)
            self.value = ivalue if ivalue == fvalue else fvalue
        except ValueError:
            self.value = float(value)

    def evaluate(self, context):
        return self

    def __str__(self):
        return self.vstr

class LGBinOpe( object ):
    def __init__(self, value):
        self.value = value
        self.opetype = self.opetype( value )

    def evaluate(self, context):
        raise LGRuntimeError( 'not-evalutable-exception' )

    def __str__(self):
        return self.value

    def opetype(self, value):
        '''演算子種別'''
        if (value == '<' or
            value == '>' or
            value == '='):
            return '<>='
        if (self.value == '*' or
            self.value == '/'):
            return '*/'
        if (self.value == '+' or
            self.value == '-'):
            return '+-'

class LGList( object ):
    def __init__(self):
        self.values = []
        self.quoteCnt = 1

    def append(self, value):
        self.values.append( value )

    def __getitem__(self, key):
        return self.values.__getitem__(key)

    def evaluate(self, context):
        return self

    def run(self, context):
        import logoParser
        parser = logoParser.LGProgramParser( context )
        tree = parser.parse( self )
        return tree.evaluate( context)

    def __str__(self):
        return '[%s]' % ' '.join(i.__str__() for i in self.values)

class LGGroup( object ):
    def __init__(self):
        self.values = []

    def append(self, value):
        self.values.append( value )

    def __getitem__(self, key):
        return self.values.__getitem__(key)

    def evaluate(self, context):
        raise LGRuntimeError( 'not-evalutable-exception' )

    def __str__(self):
        return '(%s)' % ' '.join(i.__str__() for i in self.values)







class LGOperation( object ):
    def __init__(self, name ):
        self.name = name
        self.args = []

    def appendArgument(self, argument):
        self.args.append(argument)

    def evaluate(self, context):
        func = context.findFunction( self.name )
        try:
            return func.evaluate(context,
                                 [i.evaluate(context) for i in self.args])
            return ret
        except LGInputError, err: 
            raise LGRuntimeError( '%s %s' % (self.name, err) )

    def __str__(self):
        return '{%s %s}' % (self.name,
                            ' '.join(i.__str__() for i in self.args))

class LGProgram( object ):
    def __init__(self):
        self.expressions = []

    def appendExpression(self, exp):
        self.expressions.append( exp )

    def evaluate(self, context):
        retVal = None
        for expression in self.expressions:
            retVal = expression.evaluate( context )
        return retVal

    def __str__(self):
        return 'a Logo Program'


