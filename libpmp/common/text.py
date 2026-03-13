"""Common utilities available in multiple modules."""


def pretty_truncate(text, length):
    """Return a version of @p text is no longer @p length."""
    # Matplotlib does not recognize unicode, so you can't say `u'\u2030'`
    # here.  However it does render "..." as a single character width, so you
    # can't just say it's three characters long.  Blech.
    ellipsis = "..."
    ellipsis_len = 1
    if len(text) <= length:
        return text
    return text[:length - ellipsis_len] + ellipsis
