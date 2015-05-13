#-*- coding: shift_jis -*-

import unittest
from logoElementTest import *
from logoContextTest import *
from logoScannerTest import *
from logoEzScannerTest import *
from logoDataParserTest import *
from logoProgramParserTest import *
from logoProgramParserErrorsTest import *
from logoEvaluateTest import *
from logoPrimitiveFunctionsTest import *

suite = unittest.TestSuite()

suite.addTest(unittest.makeSuite(LogoElementTest))
suite.addTest(unittest.makeSuite(LogoContestTest))
suite.addTest(unittest.makeSuite(LogoScannerTest))
suite.addTest(unittest.makeSuite(LogoEzScannerTest))
suite.addTest(unittest.makeSuite(LogoDataParserTest))
suite.addTest(unittest.makeSuite(LogoProgramParserTest))
suite.addTest(unittest.makeSuite(LogoProgramParserErrorsTest))
suite.addTest(unittest.makeSuite(LogoEvaluateTest))
suite.addTest(unittest.makeSuite(LogoPrimitiveFunctionsTest))

unittest.TextTestRunner(verbosity=2).run(suite)

