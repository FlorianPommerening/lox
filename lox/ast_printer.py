#!/usr/bin/env python

from lox.expr import *

class AstPrinter(Visitor):
    def print(self, expr: Expr):
        return expr.accept(self)

    def parenthesize(self, name: str, *exprs: list[str]):
        parts = [name] + [expr.accept(self) for expr in exprs]
        return "(" + " ".join(parts) + ")"

    def visit_binary_expr(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

if __name__ == "__main__":
    from lox.token import Token
    from lox.tokentype import TokenType

    expression = Binary(
        Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67)))
    print(AstPrinter().print(expression))
