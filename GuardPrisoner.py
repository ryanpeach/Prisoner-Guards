import sys
sys.path.insert(0,"E:\\OneDrive\\Documents\\School\\Masters of Science\\Knowledge-Based AI")
from CoreLibrary import *

PL = "PL"
PR = "PR"
GL = "GL"
GR = "GR"
BL = "BL"
S1 = "LastState"
S2 = "CurrState"

def Less(num1,num2):
        if isinstance(num1, int) and isinstance(num2, int):
                return num1 < num2
        else:
                raise TypeError, num1, num2
def Eq(num1,num2):
        if isinstance(num1, int) and isinstance(num2, int):
                return num1 == num2
        else:
                raise TypeError, num1, num2
def Real(num):
        if isinstance(num, int):
                return num >= 0
        else:
                raise TypeError, num
def Moved(state1,state2,num):
        L = state1[PL]+state1[GL]-state2[PL]-state2[GL]
        R = state1[PR]+state1[GR]-state2[PR]-state2[GR]
        return abs(L)==abs(R) and abs(L) == num and state1[BL] != state2[BL]
class MoveLR(Operator):
        def __init__(self):
                self.NAME = "MoveLR"
                Post2 = Sentence(Moved,(S1,S2,2)).disj(Moved,(S1,S2,1))
                self.Post = Sentence(BL).neg().conj(Post2)
                self.Pre  = Sentence(BL)

        def _func(self, frame):
                for n,m in [(1,0),(2,0),(1,1),(0,2),(0,1)]:
                        newFrame = frame.copy()
                        newFrame[PL] = frame[PL]-n
                        newFrame[GL] = frame[GL]-m
                        newFrame[PR] = frame[PR]+n
                        newFrame[GR] = frame[GR]+m
                        newFrame[BL] = not newFrame[BL]
                        newFrame[S1] = frame
                        newFrame[S2] = newFrame
                        newFrame.NAME = ""
                        yield newFrame

class MoveRL(Operator):
        def __init__(self):
                self.NAME = "MoveRL"
                Post2 = Sentence(Moved,(S1,S2,2)).disj(Moved,(S1,S2,1))
                self.Post = Sentence(BL).conj(Post2)
                self.Pre  = Sentence(BL).neg()

        def _func(self, frame):
                for n,m in [(1,0),(2,0),(1,1),(0,2),(0,1)]:
                        newFrame = frame.copy()
                        newFrame[PR] = frame[PR]-n
                        newFrame[GR] = frame[GR]-m
                        newFrame[PL] = frame[PL]+n
                        newFrame[GL] = frame[GL]+m
                        newFrame[BL] = not newFrame[BL]
                        newFrame[S1] = frame
                        newFrame[S2] = newFrame
                        newFrame.NAME = ""
                        yield newFrame

Init = Frame("Init", {PL: 3, PR:0, GL: 3, GR: 0, BL: True})
Goal = Frame("", {PL: 0, PR:3, GL: 0, GR: 3, BL: False})

Rule1 = Sentence(Less,(PR,GR)).disj(Eq,(PR,GR)).disj(Eq,(GR,0))
Rule2 = Sentence(Less,(PL,GL)).disj(Eq,(PL,GL)).disj(Eq,(GL,0))
Rule3 = Sentence(Real,PR).conj(Real,PL).conj(Real,GR).conj(Real,GL)
Rules = [Rule1, Rule2, Rule3]

Operators = [MoveLR(), MoveRL()]

graph = Graph(Init)
tst = Tester(graph, Rules)
gen = Generator(graph, Operators)
print generate_and_test(gen, tst, graph, Goal,20)
