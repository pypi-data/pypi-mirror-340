"""
Django email backend that invokes the system ``sendmail`` binary.
"""

import logging
from subprocess import PIPE
from subprocess import Popen

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address


LOGGER = logging.getLogger("cr-sendmail-django")


class SendmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages) -> int:
        """
        Sends one or more EmailMessage objects and returns the number of
        email messages sent.
        """
        if not email_messages:
            return 0
        num = 0
        for m in email_messages:
            if self._send(m):
                num += 1
        return num

    def _send(self, email_message) -> bool:
        encoding = email_message.encoding or settings.DEFAULT_CHARSET
        recipients = [
            sanitize_address(addr, encoding)
            for addr in email_message.recipients()
        ]
        if not recipients:
            LOGGER.warning("Email message has no recipients!")
            return False
        sendmail = getattr(settings, "SENDMAIL_BINARY", "/usr/sbin/sendmail")
        try:
            # Invoke sendmail by passing all recipients (To, Cc, Bcc) as args.
            m = email_message.message()
            args = [sendmail] + recipients
            LOGGER.debug("Message:\n---\n%s", m)
            LOGGER.info("Subprocess: %s", args)
            p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate(input=m.as_bytes(linesep="\r\n"))
            LOGGER.debug("stdout: %r", stdout)
            LOGGER.debug("stderr: %r", stderr)
        # Handle python errors.
        except Exception as err:
            LOGGER.exception("Error invoking sendmail.")
            if not self.fail_silently:
                raise err
            return False
        # Handle subprocess failure.
        if p.returncode != 0:
            if not self.fail_silently:
                error = stderr if stderr else stdout
                raise Exception(f"Sendmail failed with error: {error!r}")
            return False
        return True
