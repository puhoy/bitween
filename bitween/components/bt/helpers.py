import chardet


def decode_string(s, encoding="utf8"):
    """
    from deluges core/torrentmanager.py

    Decodes a string and return unicode. If it cannot decode using
    `:param:encoding` then it will try latin1, and if that fails,
    try to detect the string encoding. If that fails, decode with
    ignore.

    :param s: string to decode
    :type s: string
    :keyword encoding: the encoding to use in the decoding
    :type encoding: string
    :returns: s converted to unicode
    :rtype: unicode

    """
    if not s:
        return u''
    elif isinstance(s, unicode):
        return s

    encodings = [lambda: ("utf8", 'strict'),
                 lambda: ("iso-8859-1", 'strict'),
                 lambda: (chardet.detect(s)["encoding"], 'strict'),
                 lambda: (encoding, 'ignore')]

    if not encoding is "utf8":
        encodings.insert(0, lambda: (encoding, 'strict'))

    for l in encodings:
        try:
            return s.decode(*l())
        except UnicodeDecodeError:
            pass
    return u''


def utf8_encoded(s, encoding="utf8"):
    """
    from deluges core/torrentmanager.py

    Returns a utf8 encoded string of s

    :param s: (unicode) string to (re-)encode
    :type s: basestring
    :keyword encoding: the encoding to use in the decoding
    :type encoding: string
    :returns: a utf8 encoded string of s
    :rtype: str

    """
    if isinstance(s, str):
        s = decode_string(s, encoding).encode("utf8")
    elif isinstance(s, unicode):
        s = s.encode("utf8")
    return s