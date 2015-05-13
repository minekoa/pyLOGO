#-*- coding:shift_jis -*-
from logoError import *

class LGContext(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}
        self.functions = {}

    def makeVariable(self, name, value):
        '''変数に値を代入する。
        無いときはグローバルスコープに変数を作る'''
        if self.variables.has_key(name):
            self.variables[name] = value
        elif self.parent == None:
            self.variables[name] = value
        else:
            self.parent.makeVariable(name, value)

    def makeLocalVariable(self, name, value):
        '''変数に値を代入する。
        無いときはローカルスコープに変数を作る'''
        self.variables[name] = value

    def makeFunction(self, name, func):
        if self.parent == None:
            self.functions[name] = func
        else:
            self.parent.makeFunction(name, func)

    def findVariable(self, name):
        if self.variables.has_key(name.lower()):
            return self.variables[name.lower()]
        elif self.parent == None:
            raise LGRuntimeError( '%s has no value' % name )
        else:
            return self.parent.findVariable(name)

    def findFunction(self, name):
        if self.functions.has_key(name.lower()):
            return self.functions[name.lower()]
        elif self.parent == None:
            raise LGRuntimeError( "I don't know how  to %s" % name )
        else:
            return self.parent.findFunction(name)


    def stdPrint(self, msg):
        print msg
