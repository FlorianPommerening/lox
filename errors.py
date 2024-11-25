_had_error = False


def error(line: int, message: str):
    report(line, "", message)


def report(line: str, where: str, message: str):
    print(f"[line {line} Error{where}: {message}]")
    global _had_error
    _had_error = True


def had_error():
    global _had_error
    return _had_error


def reset_error():
    global _had_error
    _had_error = False
