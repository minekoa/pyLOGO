import unittest
from logoContext import *
from logoElement import *

class LogoContestTest(unittest.TestCase):

    def testGlobalVariableMakeAndFind(self):
        root = LGContext()
        child = LGContext(root)

        child.makeVariable( 'bar', LGWord('g_v') )
        self.assertEqual( child.variables.has_key('bar'), False )
        self.assertEqual( root.variables['bar'].value, 'g_v' )
        self.assertEqual( child.findVariable('bar').value, 'g_v' )

    def testLocalVariableMakeAndFind(self):
        root = LGContext()
        child = LGContext(root)

        child.makeLocalVariable( 'foo', LGWord('l_v') )

        self.assertEqual( child.variables['foo'].value, 'l_v' )
        self.assertEqual( root.variables.has_key('foo'), False )
        self.assertEqual( child.findVariable('foo').value, 'l_v' )

    def testFunctionMakeAndFind(self):
        root = LGContext()
        child = LGContext(root)

        dmyfunc1 = 'dmy1'
        dmyfunc2 = 'dmy2'
        root.makeFunction( 'func1', dmyfunc1 )
        child.makeFunction( 'func2', dmyfunc2 )

        self.assertEqual( root.functions['func1'], dmyfunc1 )
        self.assertEqual( root.functions['func2'], dmyfunc2 )

        self.assertEqual( root.findFunction('func1'), dmyfunc1 )
        self.assertEqual( child.findFunction('func1'), dmyfunc1 )

if __name__ == '__main__':
    unittest.main()
