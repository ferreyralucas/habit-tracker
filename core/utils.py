def deepgetattr(obj, attr: str, default=None):
    """
    Get a named attribute from an object; deepgetattr(x, 'a.b.c.d') is
    equivalent to x.a.b.c.d. When a default argument is given, it is
    returned when any attribute in the chain doesn't exist; without
    it, an exception is raised when a missing attribute is encountered.

    """
    for i in attr.split("."):
        obj = getattr(obj, i, default)
    return obj
