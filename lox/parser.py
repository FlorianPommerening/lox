from lox.tokentype import TokenType

class Parser():
  def __init__(self, tokens):
    self._tokens = tokens
    self._current = 0

#  def _expression(self) -> Expr:
#    pass