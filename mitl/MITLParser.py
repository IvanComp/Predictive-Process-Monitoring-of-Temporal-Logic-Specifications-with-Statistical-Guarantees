# Generated from MITL.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,19,51,2,0,7,0,2,1,7,1,2,2,7,2,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,
        1,30,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,40,8,1,10,1,12,1,43,
        9,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,0,1,2,3,0,2,4,0,2,1,0,11,12,2,0,
        13,14,16,16,55,0,6,1,0,0,0,2,29,1,0,0,0,4,44,1,0,0,0,6,7,3,2,1,0,
        7,1,1,0,0,0,8,9,6,1,-1,0,9,10,5,15,0,0,10,30,3,2,1,8,11,30,5,1,0,
        0,12,13,5,2,0,0,13,14,3,2,1,0,14,15,5,3,0,0,15,30,1,0,0,0,16,30,
        7,0,0,0,17,18,5,8,0,0,18,19,3,4,2,0,19,20,3,2,1,3,20,30,1,0,0,0,
        21,22,5,9,0,0,22,23,3,4,2,0,23,24,3,2,1,2,24,30,1,0,0,0,25,26,5,
        10,0,0,26,27,3,4,2,0,27,28,3,2,1,1,28,30,1,0,0,0,29,8,1,0,0,0,29,
        11,1,0,0,0,29,12,1,0,0,0,29,16,1,0,0,0,29,17,1,0,0,0,29,21,1,0,0,
        0,29,25,1,0,0,0,30,41,1,0,0,0,31,32,10,9,0,0,32,33,7,1,0,0,33,40,
        3,2,1,10,34,35,10,4,0,0,35,36,5,7,0,0,36,37,3,4,2,0,37,38,3,2,1,
        5,38,40,1,0,0,0,39,31,1,0,0,0,39,34,1,0,0,0,40,43,1,0,0,0,41,39,
        1,0,0,0,41,42,1,0,0,0,42,3,1,0,0,0,43,41,1,0,0,0,44,45,5,5,0,0,45,
        46,5,17,0,0,46,47,5,4,0,0,47,48,5,17,0,0,48,49,5,6,0,0,49,5,1,0,
        0,0,3,29,39,41
    ]

class MITLParser ( Parser ):

    grammarFileName = "MITL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "'('", "')'", "','", "'['", 
                     "']'", "'U'", "'F'", "'G'", "'X'", "'True'", "'False'", 
                     "'&'", "'|'", "'!'", "'-->'" ]

    symbolicNames = [ "<INVALID>", "PARAMETERS", "LPAR", "RPAR", "COMMA", 
                      "LBRAT", "RBRAT", "U", "F", "G", "X", "TRUE", "FALSE", 
                      "AND", "OR", "NOT", "IMPL", "NUMBER", "COMMENT", "WS" ]

    RULE_prog = 0
    RULE_formula = 1
    RULE_interval = 2

    ruleNames =  [ "prog", "formula", "interval" ]

    EOF = Token.EOF
    PARAMETERS=1
    LPAR=2
    RPAR=3
    COMMA=4
    LBRAT=5
    RBRAT=6
    U=7
    F=8
    G=9
    X=10
    TRUE=11
    FALSE=12
    AND=13
    OR=14
    NOT=15
    IMPL=16
    NUMBER=17
    COMMENT=18
    WS=19

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def formula(self):
            return self.getTypedRuleContext(MITLParser.FormulaContext,0)


        def getRuleIndex(self):
            return MITLParser.RULE_prog

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProg" ):
                listener.enterProg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProg" ):
                listener.exitProg(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProg" ):
                return visitor.visitProg(self)
            else:
                return visitor.visitChildren(self)




    def prog(self):

        localctx = MITLParser.ProgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_prog)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 6
            self.formula(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FormulaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return MITLParser.RULE_formula

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class NotContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MITLParser.FormulaContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NOT(self):
            return self.getToken(MITLParser.NOT, 0)
        def formula(self):
            return self.getTypedRuleContext(MITLParser.FormulaContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNot" ):
                listener.enterNot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNot" ):
                listener.exitNot(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNot" ):
                return visitor.visitNot(self)
            else:
                return visitor.visitChildren(self)


    class AndOrImplContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MITLParser.FormulaContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def formula(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MITLParser.FormulaContext)
            else:
                return self.getTypedRuleContext(MITLParser.FormulaContext,i)

        def AND(self):
            return self.getToken(MITLParser.AND, 0)
        def OR(self):
            return self.getToken(MITLParser.OR, 0)
        def IMPL(self):
            return self.getToken(MITLParser.IMPL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAndOrImpl" ):
                listener.enterAndOrImpl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAndOrImpl" ):
                listener.exitAndOrImpl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndOrImpl" ):
                return visitor.visitAndOrImpl(self)
            else:
                return visitor.visitChildren(self)


    class UContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MITLParser.FormulaContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def formula(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MITLParser.FormulaContext)
            else:
                return self.getTypedRuleContext(MITLParser.FormulaContext,i)

        def U(self):
            return self.getToken(MITLParser.U, 0)
        def interval(self):
            return self.getTypedRuleContext(MITLParser.IntervalContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterU" ):
                listener.enterU(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitU" ):
                listener.exitU(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitU" ):
                return visitor.visitU(self)
            else:
                return visitor.visitChildren(self)


    class FContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MITLParser.FormulaContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def F(self):
            return self.getToken(MITLParser.F, 0)
        def interval(self):
            return self.getTypedRuleContext(MITLParser.IntervalContext,0)

        def formula(self):
            return self.getTypedRuleContext(MITLParser.FormulaContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterF" ):
                listener.enterF(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitF" ):
                listener.exitF(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitF" ):
                return visitor.visitF(self)
            else:
                return visitor.visitChildren(self)


    class ParensFormulaContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MITLParser.FormulaContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAR(self):
            return self.getToken(MITLParser.LPAR, 0)
        def formula(self):
            return self.getTypedRuleContext(MITLParser.FormulaContext,0)

        def RPAR(self):
            return self.getToken(MITLParser.RPAR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParensFormula" ):
                listener.enterParensFormula(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParensFormula" ):
                listener.exitParensFormula(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParensFormula" ):
                return visitor.visitParensFormula(self)
            else:
                return visitor.visitChildren(self)


    class TrueFalseContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MITLParser.FormulaContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def TRUE(self):
            return self.getToken(MITLParser.TRUE, 0)
        def FALSE(self):
            return self.getToken(MITLParser.FALSE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTrueFalse" ):
                listener.enterTrueFalse(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTrueFalse" ):
                listener.exitTrueFalse(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTrueFalse" ):
                return visitor.visitTrueFalse(self)
            else:
                return visitor.visitChildren(self)


    class GContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MITLParser.FormulaContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def G(self):
            return self.getToken(MITLParser.G, 0)
        def interval(self):
            return self.getTypedRuleContext(MITLParser.IntervalContext,0)

        def formula(self):
            return self.getTypedRuleContext(MITLParser.FormulaContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterG" ):
                listener.enterG(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitG" ):
                listener.exitG(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitG" ):
                return visitor.visitG(self)
            else:
                return visitor.visitChildren(self)


    class XContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MITLParser.FormulaContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def X(self):
            return self.getToken(MITLParser.X, 0)
        def interval(self):
            return self.getTypedRuleContext(MITLParser.IntervalContext,0)

        def formula(self):
            return self.getTypedRuleContext(MITLParser.FormulaContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterX" ):
                listener.enterX(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitX" ):
                listener.exitX(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitX" ):
                return visitor.visitX(self)
            else:
                return visitor.visitChildren(self)


    class AtomContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a MITLParser.FormulaContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def PARAMETERS(self):
            return self.getToken(MITLParser.PARAMETERS, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtom" ):
                listener.enterAtom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtom" ):
                listener.exitAtom(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtom" ):
                return visitor.visitAtom(self)
            else:
                return visitor.visitChildren(self)



    def formula(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = MITLParser.FormulaContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_formula, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 29
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [15]:
                localctx = MITLParser.NotContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 9
                self.match(MITLParser.NOT)
                self.state = 10
                self.formula(8)
                pass
            elif token in [1]:
                localctx = MITLParser.AtomContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 11
                self.match(MITLParser.PARAMETERS)
                pass
            elif token in [2]:
                localctx = MITLParser.ParensFormulaContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 12
                self.match(MITLParser.LPAR)
                self.state = 13
                self.formula(0)
                self.state = 14
                self.match(MITLParser.RPAR)
                pass
            elif token in [11, 12]:
                localctx = MITLParser.TrueFalseContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 16
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==11 or _la==12):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass
            elif token in [8]:
                localctx = MITLParser.FContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 17
                self.match(MITLParser.F)
                self.state = 18
                self.interval()
                self.state = 19
                self.formula(3)
                pass
            elif token in [9]:
                localctx = MITLParser.GContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 21
                self.match(MITLParser.G)
                self.state = 22
                self.interval()
                self.state = 23
                self.formula(2)
                pass
            elif token in [10]:
                localctx = MITLParser.XContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 25
                self.match(MITLParser.X)
                self.state = 26
                self.interval()
                self.state = 27
                self.formula(1)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 41
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 39
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = MITLParser.AndOrImplContext(self, MITLParser.FormulaContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 31
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 32
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 90112) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 33
                        self.formula(10)
                        pass

                    elif la_ == 2:
                        localctx = MITLParser.UContext(self, MITLParser.FormulaContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 34
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 35
                        self.match(MITLParser.U)
                        self.state = 36
                        self.interval()
                        self.state = 37
                        self.formula(5)
                        pass

             
                self.state = 43
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class IntervalContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRAT(self):
            return self.getToken(MITLParser.LBRAT, 0)

        def NUMBER(self, i:int=None):
            if i is None:
                return self.getTokens(MITLParser.NUMBER)
            else:
                return self.getToken(MITLParser.NUMBER, i)

        def COMMA(self):
            return self.getToken(MITLParser.COMMA, 0)

        def RBRAT(self):
            return self.getToken(MITLParser.RBRAT, 0)

        def getRuleIndex(self):
            return MITLParser.RULE_interval

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInterval" ):
                listener.enterInterval(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInterval" ):
                listener.exitInterval(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInterval" ):
                return visitor.visitInterval(self)
            else:
                return visitor.visitChildren(self)




    def interval(self):

        localctx = MITLParser.IntervalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_interval)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            self.match(MITLParser.LBRAT)
            self.state = 45
            self.match(MITLParser.NUMBER)
            self.state = 46
            self.match(MITLParser.COMMA)
            self.state = 47
            self.match(MITLParser.NUMBER)
            self.state = 48
            self.match(MITLParser.RBRAT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.formula_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def formula_sempred(self, localctx:FormulaContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 9)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 4)
         




