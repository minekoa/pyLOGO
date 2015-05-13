#-*- coding:shift_jis -*-

from Tkinter import *
from ScrolledText import *
from turtleGraphics import *

from logoParser import *
from logoScanner import *
from logoContext import *

from logoPrimitiveFunctions import *

class PrintGuiFunc( PrintFunc ):
    def __init__(self, window):
        self.window = window
    def print_(self, message ):
        self.window.print_(message)


class LogoWindow( Frame ):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('glogo ver.0.1.0')
        self.turtle = Turtle()

        self.createScreen()
        self.createConsole()
        self.createCommandLine()

        self.buildContext()

    def buildContext(self):
        self.context = LGContext()
        # basic primitive
        self.context.makeFunction( '+', SumFunc() )
        self.context.makeFunction( '-', DifferenceFunc() )
        self.context.makeFunction( '*', ProductFunc() )
        self.context.makeFunction( '/', QuotientFunc() )
        self.context.makeFunction( 'sum', SumFunc() )
        self.context.makeFunction( 'defference', DifferenceFunc() )
        self.context.makeFunction( 'product', ProductFunc() )
        self.context.makeFunction( 'quotient', QuotientFunc() )
        self.context.makeFunction( 'reminder', ReminderFunc() )
        self.context.makeFunction( 'int', IntFunc() )
        self.context.makeFunction( 'round', RoundFunc() )

        self.context.makeFunction( 'print', PrintGuiFunc(self) )
        self.context.makeFunction( 'make', MakeFunc() )
        self.context.makeFunction( 'localmake', LocalmakeFunc() )
        self.context.makeFunction( 'thing', ThingFunc() )
        self.context.makeFunction( 'run', RunFunc() )
        self.context.makeFunction( 'define', DefineFunc() )
        self.context.makeFunction( 'repeat', RepeatFunc() )

        # math
        self.context.makeFunction( 'pi', PiFunc() )
        self.context.makeFunction( 'sqrt', SqrtFunc() )
        self.context.makeFunction( 'sin', SinFunc() )
        self.context.makeFunction( 'cos', CosFunc() )
        self.context.makeFunction( 'tan', TanFunc() )
        self.context.makeFunction( 'arctan', ArctanFunc() )

        # turtle graphics
        self.context.makeFunction( 'fd', ForwardFunc(self.turtle) )
        self.context.makeFunction( 'bk', BackFunc(self.turtle) )
        self.context.makeFunction( 'rt', RightFunc(self.turtle) )
        self.context.makeFunction( 'lt', LeftFunc(self.turtle) )
        self.context.makeFunction( 'pd', PendownFunc(self.turtle) )
        self.context.makeFunction( 'pu', PenupFunc(self.turtle) )
        self.context.makeFunction( 'cs', ClearScreenFunc(self.turtle, self.screen) )
        self.context.makeFunction( 'forward', ForwardFunc(self.turtle) )
        self.context.makeFunction( 'back', BackFunc(self.turtle) )
        self.context.makeFunction( 'right', RightFunc(self.turtle) )
        self.context.makeFunction( 'left', LeftFunc(self.turtle) )
        self.context.makeFunction( 'pendown', PendownFunc(self.turtle) )
        self.context.makeFunction( 'penup', PenupFunc(self.turtle) )
        self.context.makeFunction( 'clearscreen',ClearScreenFunc(self.turtle, self.screen) )
        self.context.makeFunction( 'home', HomeFunc(self.turtle) )

        self.dparser = LGDataParser()
        self.pparser = LGProgramParser( self.context )



    def createScreen(self):
        self.screen = TurtleScreen( self.turtle,
                                    self,
                                    relief=RAISED,
                                    bg='white',
                                    width=400,
                                    height=400)
        self.screen.pack(side=TOP, fill=X)

    def createConsole(self):
        self.console = ScrolledText( self,
                                     width=40,
                                     height=5 )
        self.console.pack(side=TOP, fill=X)

    def createCommandLine(self):
        mainfrm = Frame(self)
        self.source = StringVar()
        self.cmdline = Entry( mainfrm, width=60,
                              textvariable=self.source )
        self.cmdline.pack(side=LEFT, fill=X)
        self.cmdline.bind('<Return>', lambda x: self.runCommand() )

        Button( mainfrm,
                command=self.runCommand , text='run' ).pack(side=LEFT,fill=X)
        mainfrm.pack(side=TOP, fill=X)

    def runCommand(self):
        try:
            self.console.insert(END, ">>> %s\n" % self.source.get())
            self.run(self.source.get())
        except LGRuntimeError, err:
            self.console.insert(END, "%s\n" % err)
        self.cmdline.delete(0, END)
        self.console.see(END)

    def run(self, source):
        scanner = LGScanner( source )
        lst  = self.dparser.parse( scanner )
        tree = self.pparser.parse( lst )
        ret  = tree.evaluate( self.context )
        if ret != None:
            self.print_( "You don't say what to do with %s" % ret )

    def print_(self, message):
        self.console.insert(END, "%s\n" % message )



if __name__ == '__main__':
    window = LogoWindow()
    window.pack()
    window.mainloop()
