#-*- coding: shift_jis -*-

import unittest
from logoElement import *
from logoContext import *

class LogoElementTest(unittest.TestCase):

    def testLGWord(self):
        target = LGWord( 'hogehoge' )
        self.assertEqual( target.value, 'hogehoge' )

        try:
            target.evaluate( None )
            self.fail('not-evalutable-exception')

        except LGRuntimeError, err:
            self.assertEqual( err.__str__(), 'not-evalutable-exception' )

        self.assertEqual( target.__str__(), 'hogehoge' )


    def testLGQuoWord(self):
        target = LGQuoWord( '"hogehoge' )
        self.assertEqual( target.value, '"hogehoge' )

        evalret = target.evaluate( None )
        self.assertEqual( type(evalret), LGQuoWord )
        self.assertEqual( evalret.value, '"hogehoge' )

#        thingret = target.thing()
#        self.assertEqual( type(thingret), LGWord )
#        self.assertEqual( thingret.value, 'hogehoge' )

        self.assertEqual( target.__str__(), '"hogehoge' )


    def testLGDotWord(self):
        target = LGDotWord( ':hogehoge' )
        self.assertEqual( target.value, ':hogehoge' )

        context = LGContext()
        context.makeVariable( 'hogehoge', LGWord('piyopiyo') )

        evalret = target.evaluate( context )
        self.assertEqual( type(evalret), LGWord )
        self.assertEqual( evalret.value, 'piyopiyo' )

        self.assertEqual( target.__str__(), ':hogehoge' )


    def testLGNumWord(self):
        target_si = LGNumWord( '42' )
        self.assertEqual( target_si.value, 42 )
        self.assertEqual( target_si.__str__(), '42' )

        target_sf = LGNumWord( '3.14' )
        self.assertEqual( target_sf.value, 3.14 )
        self.assertEqual( target_sf.__str__(), '3.14' )

        target_i = LGNumWord( 42 )
        self.assertEqual( target_i.value, 42 )
        self.assertEqual( target_i.__str__(), '42' )

        target_f = LGNumWord( 3.14 )
        self.assertEqual( target_f.value, 3.14 )
        self.assertEqual( target_f.__str__(), '3.14' )


if __name__ == '__main__':
    unittest.main()
