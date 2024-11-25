from errors import error
from tokentype import TokenType
from token import Token

KEYWORDS = {
    "and":    TokenType.AND,
    "class":  TokenType.CLASS,
    "else":   TokenType.ELSE,
    "false":  TokenType.FALSE,
    "for":    TokenType.FOR,
    "fun":    TokenType.FUN,
    "if":     TokenType.IF,
    "nil":    TokenType.NIL,
    "or":     TokenType.OR,
    "print":  TokenType.PRINT,
    "return": TokenType.RETURN,
    "super":  TokenType.SUPER,
    "this":   TokenType.THIS,
    "true":   TokenType.TRUE,
    "var":    TokenType.VAR,
    "while":  TokenType.WHILE,
}


class Scanner():
    def __init__(self, source: str):
       self._source = source
       self._tokens = []
       self._start = 0
       self._current = 0
       self._line = 1

    def scan_tokens(self):
        while not self._is_at_end():
            # We are at the beginning of the next lexeme.
            self._start = self._current
            self._scan_token()
        self._tokens.append(Token(TokenType.EOF, "", None, self._line))
        return self._tokens


    def _scan_token(self):
        c = self._advance()
        if c == '(': self._add_token(TokenType.LEFT_PAREN)
        elif c == '(': self._add_token(TokenType.LEFT_PAREN)
        elif c == ')': self._add_token(TokenType.RIGHT_PAREN)
        elif c == '{': self._add_token(TokenType.LEFT_BRACE)
        elif c == '}': self._add_token(TokenType.RIGHT_BRACE)
        elif c == ',': self._add_token(TokenType.COMMA)
        elif c == '.': self._add_token(TokenType.DOT)
        elif c == '-': self._add_token(TokenType.MINUS)
        elif c == '+': self._add_token(TokenType.PLUS)
        elif c == ';': self._add_token(TokenType.SEMICOLON)
        elif c == '*': self._add_token(TokenType.STAR)
        elif c == '!':
            if self._match('='):
                self._add_token(TokenType.BANG_EQUAL)
            else:
                self._add_token(TokenType.BANG)
        elif c == '=':
            if self._match('='):
                self._add_token(TokenType.EQUAL_EQUAL)
            else:
                self._add_token(TokenType.EQUAL)
        elif c == '<':
            if self._match('='):
                self._add_token(TokenType.LESS_EQUAL)
            else:
                self._add_token(TokenType.LESS)
        elif c == '>':
            if self._match('='):
                self._add_token(TokenType.GREATER_EQUAL)
            else:
                self._add_token(TokenType.GREATER)
        elif c == '/':
            if self._match('/'):
                # A comment goes until the end of the line.
                while self._peek() != '\n' and not self._is_at_end():
                    self._advance()
            else:
                self._add_token(TokenType.SLASH)
        elif c == ' ' or c == '\r' or c == '\t':
            # Ignore whitespace.
            pass
        elif c == '\n':
            self._line += 1
        elif c == '"': self._string()
        elif is_digit(c):
            self._number()
        elif is_alpha(c):
            self._identifier()
        else:
            error(self._line, f"unexpected character '{c}'.")


    def _advance(self):
        c = self._source[self._current]
        self._current += 1
        return c


    def _match(self, expected):
        if self._is_at_end():
            return False
        if self._source[self._current] != expected:
            return False
        self._current += 1
        return True


    def _peek(self):
        if self._is_at_end():
            return '\0'
        return self._source[self._current]


    def _peek_next(self):
        if self._current + 1 >= len(self._source):
            return '\0'
        return self._source[self._current + 1]


    def _add_token(self, token_type: TokenType, literal: object = None):
        text = self._source[self._start: self._current]
        self._tokens.append(Token(token_type, text, literal, self._line))


    def _is_at_end(self):
        return self._current >= len(self._source)


    def _string(self):
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == '\n':
                self._line += 1
            self._advance()
            if self._is_at_end():
                error(self._line, "Unterminated string.")
                return
        # The closing ".
        self._advance()

        # Trim the surrounding quotes.
        value = self._source[self._start + 1: self._current - 1]
        self._add_token(TokenType.STRING, value)


    def _number(self):
        while is_digit(self._peek()):
            self._advance()
        # Look for a fractional part.
        if self._peek() == '.' and is_digit(self._peek_next()) :
            # Consume the "."
            self._advance()
            while is_digit(self._peek()):
                self._advance()
        value = float(self._source[self._start: self._current])
        self._add_token(TokenType.NUMBER, value)


    def _identifier(self):
        while is_alpha_numeric(self._peek()):
            self._advance()
        text = self._source[self._start: self._current]
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)
        self._add_token(token_type)


def is_digit(c):
    return '0' <= c <= '9'


def is_alpha(c):
    return 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c == '_'


def is_alpha_numeric(c):
    return is_alpha(c) or is_digit(c)
