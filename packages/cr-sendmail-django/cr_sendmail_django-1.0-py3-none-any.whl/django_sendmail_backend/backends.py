"""
Shim for compatibility with ``django_sendmail_backend``.
"""

from cr_sendmail.backends import SendmailBackend


class EmailBackend(SendmailBackend):
    pass
