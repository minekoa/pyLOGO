#-*- coding: shift_jis -*-

from math import *
from Tkinter import *
from logoElement import *

from logoElement import _asNum

class Coordinate(object):
    '''タートル座標'''
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    @classmethod
    def fromVector(cls, direction, distance):
        return Coordinate().moveVector(direction, distance)

    def __add__(self, other):
        return Coordinate( self.x + float(other.x),
                           self.y + float(other.y) )
    def __sub__(self, other):
        return Coordinate( self.x - float(other.x),
                           self.y - float(other.y) )

    def moveVector(self, direction, distance):
        self.y -= cos( radians(direction) ) * distance
        self.x += sin( radians(direction) ) * distance
        return self

    def clone(self): return Coordinate(self.x, self.y)
    def __str__(self): return '(%d,%d)' % (self.x, self.y)


class Subject(object):
    '''Observerパターン用'''
    def __init__(self): self.observers = []
    def addObserver(self, obs): self.observers.append(obs)
    def notifyObservers(self, aspect):
        for i in self.observers: i.update(aspect)


class Turtle( Subject ):
    def __init__(self, x=0.0, y=0.0):
        Subject.__init__(self)
        self.direction = 0 # タートルの向き
        self.isPenDown = True
        self.pos = Coordinate(x,y)
        self.oldpos = self.pos

    def oldX(self): return self.oldpos.x
    def oldY(self): return self.oldpos.y
    def x(self): return self.pos.x
    def y(self): return self.pos.y


    def forward( self, distance ):
        self.oldpos = self.pos.clone()
        self.pos.moveVector(self.direction, distance)
        self.notifyObservers('forward')

    def back(self, distance):
        self.oldpos = self.pos.clone()
        self.pos.moveVector(self.direction, -distance)
        self.notifyObservers('back')

    def right(self, angle):
        self.direction = (self.direction + angle) % 360
        self.notifyObservers('right')

    def left(self,angle):
        self.direction = (self.direction - angle) % 360
        self.notifyObservers('left')

    def home(self):
        self.direction = 0
        self.oldpos = self.pos.clone()
        self.pos = Coordinate(0.0, 0.0)
        self.notifyObservers('home')

    def penup(self): self.isPenDown = False
    def pendown(self): self.isPenDown = True


class ForwardFunc(object):
    def __init__(self, turtle): self.turtle = turtle
    def requieredArgCount(self): return 1
    def evaluate(self, context, args):
        self.turtle.forward( _asNum(args[0]) )

class BackFunc(object):
    def __init__(self, turtle): self.turtle = turtle
    def requieredArgCount(self): return 1
    def evaluate(self, context, args):
        self.turtle.back( _asNum(args[0]) )

class RightFunc(object):
    def __init__(self, turtle): self.turtle = turtle
    def requieredArgCount(self): return 1
    def evaluate(self, context, args):
        self.turtle.right( _asNum(args[0]) )

class LeftFunc(object):
    def __init__(self, turtle): self.turtle = turtle
    def requieredArgCount(self): return 1
    def evaluate(self, context, args):
        self.turtle.left( _asNum(args[0]) )

class HomeFunc(object):
    def __init__(self, turtle): self.turtle = turtle
    def requieredArgCount(self): return 0
    def evaluate(self, context, args):
        self.turtle.home()

class PenupFunc(object):
    def __init__(self, turtle): self.turtle = turtle
    def requieredArgCount(self): return 0
    def evaluate(self, context, args):
        self.turtle.penup()

class PendownFunc(object):
    def __init__(self, turtle): self.turtle = turtle
    def requieredArgCount(self): return 0
    def evaluate(self, context, args):
        self.turtle.pendown()


class TurtleScreen( Canvas ):
    def __init__(self, turtle, master=None, **args):
        Canvas.__init__(self, master, args)
        self.turtle = turtle
        self.turtle.addObserver(self)

        self.orgX = int(self['width']) / 2
        self.orgY = int(self['height']) / 2
        self.writeTurtle()

    def update(self, aspect):
        self.writeTurtle()
        if (aspect == 'forward' or aspect == 'back' or
            aspect == 'home'):
            if self.turtle.isPenDown:
                self.writeTrac()

    def writeTrac(self):
        if self.turtle.isPenDown == True:
            self.create_line( self.turtle.oldX() +self.orgX, self.turtle.oldY() +self.orgY,
                              self.turtle.x() +self.orgX, self.turtle.y() +self.orgY,
                              tag='trac' )
    def deleteTrac(self):
        self.delete('trac')

    def writeTurtle(self):
        dr = self.turtle.direction
        p1 = self.turtle.pos + Coordinate.fromVector( dr, 20 )
        p2 = self.turtle.pos + Coordinate.fromVector( dr-120, 10 )
        p3 = self.turtle.pos + Coordinate.fromVector( dr+120, 10 )

        self.delete('turtle')
        self.create_line( p1.x +self.orgX, p1.y +self.orgY,
                          p2.x +self.orgX, p2.y +self.orgY,
                          p3.x +self.orgX, p3.y +self.orgY,
                          p1.x +self.orgX, p1.y +self.orgY,
                          tag='turtle')

    def deleteTurtle(self):
        self.delete('turtle')


class ClearScreenFunc(object):
    def __init__(self, turtle, screen):
        self.turtle = turtle
        self.screen = screen
    def requieredArgCount(self): return 0
    def evaluate(self, context, args):
        self.turtle.home()
        self.screen.deleteTrac()


