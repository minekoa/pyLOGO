#-*- coding: shift_jis -*-

class LGRuntimeError(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message

class LGInputError(Exception):
    def __init__(self, ngInput):
        self.ngInput = ngInput
    def __str__(self):
        return "doesn't like %s as input" % self.ngInput

