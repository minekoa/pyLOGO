#-*- coding: shift_jis -*-

import unittest
from logoScanner import *
from logoParser import *

class LogoDataParserTest(unittest.TestCase):

    def testWordsParseInList(self):
        source  = 'print "hello 42 :hoge -1 1.0 -3.14'
        scanner = LGScanner( source )
        parser  = LGDataParser()

        ret = parser.parse(scanner)
        self.assertEqual( type(ret) ,LGList )

        self.assertEqual( ret[0].value,  'print' )
        self.assertEqual( type(ret[0]) , LGWord )

        self.assertEqual( ret[1].value,  '"hello' )
        self.assertEqual( type(ret[1]) , LGQuoWord )

        self.assertEqual( ret[2].value,  42 )
        self.assertEqual( type(ret[2]) , LGNumWord )

        self.assertEqual( ret[3].value,  ':hoge' )
        self.assertEqual( type(ret[3]) , LGDotWord )

        self.assertEqual( ret[4].value,  -1 )
        self.assertEqual( type(ret[4]) , LGNumWord )

        self.assertEqual( ret[5].value,  1.0 )
        self.assertEqual( type(ret[5]) , LGNumWord )

        self.assertEqual( ret[6].value,  -3.14 )
        self.assertEqual( type(ret[6]) , LGNumWord )

        try:
            ret[7]
            self.fail("don't raize Index Error")
        except IndexError:
            pass

    def testWordsParseInGroup(self):
        source  = '(print "hello 42 :hoge)'
        scanner = LGScanner( source )
        parser  = LGDataParser()

        ret = parser.parse(scanner)
        self.assertEqual( type(ret) ,LGList )

        self.assertEqual( type(ret[0]) , LGGroup )
        grp = ret[0]

        self.assertEqual( grp[0].value,  'print' )
        self.assertEqual( type(grp[0]) , LGWord )

        self.assertEqual( grp[1].value,  '"hello' )
        self.assertEqual( type(grp[1]) , LGQuoWord )

        self.assertEqual( grp[2].value,  42 )
        self.assertEqual( type(grp[2]) , LGNumWord )

        self.assertEqual( grp[3].value,  ':hoge' )
        self.assertEqual( type(grp[3]) , LGDotWord )

        try:
            ret[1]
            self.fail("don't raize Index Error")
        except IndexError:
            pass

        try:
            grp[4]
            self.fail("don't raize Index Error")
        except IndexError:
            pass


    def testListNest(self):
        source  = 'print ["hello [sum 42 36] :hoge]'
        scanner = LGScanner( source )
        parser  = LGDataParser()

        ret = parser.parse(scanner)
        self.assertEqual( type(ret) ,LGList )

        self.assertEqual( ret[0].value,  'print' )
        self.assertEqual( type(ret[0]) , LGWord )

        #--[
        self.assertEqual( type(ret[1]) , LGList )
        lst2 = ret[1]

        self.assertEqual( lst2[0].value,  '"hello' )
        self.assertEqual( type(lst2[0]) , LGQuoWord )

        #--[
        self.assertEqual( type(lst2[1]) , LGList )
        lst3 = lst2[1]

        self.assertEqual( lst3[0].value,  'sum' )
        self.assertEqual( type(lst3[0]) , LGWord )

        self.assertEqual( lst3[1].value,  42 )
        self.assertEqual( type(lst3[1]) , LGNumWord )

        self.assertEqual( lst3[2].value,  36 )
        self.assertEqual( type(lst3[2]) , LGNumWord )
        #--]
 
        self.assertEqual( lst2[2].value,  ':hoge' )
        self.assertEqual( type(lst2[2]) , LGDotWord )
        #--]

        try:
            ret[2]
            self.fail("don't raize Index Error")
        except IndexError:
            pass
        try:
            lst2[3]
            self.fail("don't raize Index Error")
        except IndexError:
            pass
        try:
            lst3[3]
            self.fail("don't raize Index Error")
        except IndexError:
            pass

    def testGroupNest(self):
        source  = 'print ("hello (sum 42 36) :hoge)'
        scanner = LGScanner( source )
        parser  = LGDataParser()

        ret = parser.parse(scanner)
        self.assertEqual( type(ret) ,LGList )

        self.assertEqual( ret[0].value,  'print' )
        self.assertEqual( type(ret[0]) , LGWord )

        #--[
        self.assertEqual( type(ret[1]) , LGGroup )
        grp1 = ret[1]

        self.assertEqual( grp1[0].value,  '"hello' )
        self.assertEqual( type(grp1[0]) , LGQuoWord )

        #--[
        self.assertEqual( type(grp1[1]) , LGGroup )
        grp2 = grp1[1]

        self.assertEqual( grp2[0].value,  'sum' )
        self.assertEqual( type(grp2[0]) , LGWord )

        self.assertEqual( grp2[1].value,  42 )
        self.assertEqual( type(grp2[1]) , LGNumWord )

        self.assertEqual( grp2[2].value,  36 )
        self.assertEqual( type(grp2[2]) , LGNumWord )
        #--]
 
        self.assertEqual( grp1[2].value,  ':hoge' )
        self.assertEqual( type(grp1[2]) , LGDotWord )
        #--]

        try:
            ret[2]
            self.fail("don't raize Index Error")
        except IndexError:
            pass
        try:
            grp1[3]
            self.fail("don't raize Index Error")
        except IndexError:
            pass
        try:
            grp2[3]
            self.fail("don't raize Index Error")
        except IndexError:
            pass


    def testGroupListNest(self):
        source  = 'print ("hello [sum 42 36] :hoge)'
        scanner = LGScanner( source )
        parser  = LGDataParser()

        ret = parser.parse(scanner)
        self.assertEqual( type(ret) ,LGList )

        self.assertEqual( ret[0].value,  'print' )
        self.assertEqual( type(ret[0]) , LGWord )

        #--[
        self.assertEqual( type(ret[1]) , LGGroup )
        grp = ret[1]

        self.assertEqual( grp[0].value,  '"hello' )
        self.assertEqual( type(grp[0]) , LGQuoWord )

        #--[
        self.assertEqual( type(grp[1]) , LGList )
        lst3 = grp[1]

        self.assertEqual( lst3[0].value,  'sum' )
        self.assertEqual( type(lst3[0]) , LGWord )

        self.assertEqual( lst3[1].value,  42 )
        self.assertEqual( type(lst3[1]) , LGNumWord )

        self.assertEqual( lst3[2].value,  36 )
        self.assertEqual( type(lst3[2]) , LGNumWord )
        #--]
 
        self.assertEqual( grp[2].value,  ':hoge' )
        self.assertEqual( type(grp[2]) , LGDotWord )
        #--]

        try:
            ret[2]
            self.fail("don't raize Index Error")
        except IndexError:
            pass
        try:
            grp[3]
            self.fail("don't raize Index Error")
        except IndexError:
            pass
        try:
            lst3[3]
            self.fail("don't raize Index Error")
        except IndexError:
            pass


    def testBinOpeScan(self):
        source  = '1 + 2 - 3 * 4 / 5 = 6 < 7 > 8'
        scanner = LGScanner( source )
        parser  = LGDataParser()

        ret = parser.parse(scanner)
        self.assertEqual( type(ret) ,LGList )

        self.assertEqual( ret[0].value,  1 )
        self.assertEqual( type(ret[0]) , LGNumWord )

        self.assertEqual( ret[1].value,  '+' )
        self.assertEqual( type(ret[1]) , LGBinOpe )

        self.assertEqual( ret[2].value,  2 )
        self.assertEqual( type(ret[2]) , LGNumWord )

        self.assertEqual( ret[3].value,  '-' )
        self.assertEqual( type(ret[3]) , LGBinOpe )

        self.assertEqual( ret[4].value,  3 )
        self.assertEqual( type(ret[4]) , LGNumWord )

        self.assertEqual( ret[5].value,  '*' )
        self.assertEqual( type(ret[5]) , LGBinOpe )

        self.assertEqual( ret[6].value,  4 )
        self.assertEqual( type(ret[6]) , LGNumWord )

        self.assertEqual( ret[7].value,  '/' )
        self.assertEqual( type(ret[7]) , LGBinOpe )

        self.assertEqual( ret[8].value,  5 )
        self.assertEqual( type(ret[8]) , LGNumWord )

        self.assertEqual( ret[9].value,  '=' )
        self.assertEqual( type(ret[9]) , LGBinOpe )

        self.assertEqual( ret[10].value,  6 )
        self.assertEqual( type(ret[10]) , LGNumWord )

        self.assertEqual( ret[11].value,  '<' )
        self.assertEqual( type(ret[11]) , LGBinOpe )

        self.assertEqual( ret[12].value,  7 )
        self.assertEqual( type(ret[12]) , LGNumWord )

        self.assertEqual( ret[13].value,  '>' )
        self.assertEqual( type(ret[13]) , LGBinOpe )

        self.assertEqual( ret[14].value,  8 )
        self.assertEqual( type(ret[14]) , LGNumWord )

        try:
            ret[15]
            self.fail("don't raize Index Error")
        except IndexError:
            pass

