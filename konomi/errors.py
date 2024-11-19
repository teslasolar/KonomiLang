class KonomiError(Exception):
    pass

class SyntaxError(KonomiError):
    pass

class RuntimeError(KonomiError):
    pass
