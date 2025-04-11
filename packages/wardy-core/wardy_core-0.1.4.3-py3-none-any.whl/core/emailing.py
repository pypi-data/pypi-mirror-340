"""Email processing."""
from __future__ import annotations

import logging
import mimetypes
import smtplib
import ssl
from collections import ChainMap
from dataclasses import dataclass, field, fields
from datetime import datetime, timezone
from email.message import EmailMessage
from functools import partial
from pathlib import Path
from typing import Any

import dacite

logger = logging.getLogger(__name__)


@dataclass
class EmailArgs:
    """Arguments for email routine."""

    from_mail: str = ""
    to_mail: str | list[str] = ""
    subject: str = "No Subject"
    body: str = ""
    html: str = ""
    files: set[str | Path] = field(default_factory=set)
    smtphost: str | None = None
    smtpport: int = 25
    smtpuser: str | None = None
    smtppass: str | None = None
    use_ssl: bool = False

    def add_file(self, filename: str | Path) -> None:
        """Add a file to the set of paths.

        Args:
            filename (Union[str, Path]): file name to add to sending list
        """
        self.files.add(Path(filename))

    @property
    def to_mail_as_str(self) -> str:
        """Return supplied to-mail as a str for sending.

        Raises:
            TypeError: Invalid type for to_mail

        Returns:
            str: comma-separated to emails
        """
        if isinstance(self.to_mail, str):
            return self.to_mail
        if isinstance(self.to_mail, list):
            return ",".join(self.to_mail)
        raise TypeError(
            f"parameter to_emails is of unsupported type {type(self.to_mail)}"
        )


def build_email_args(*args) -> EmailArgs:
    """Build email arg object from a collection of mappings.

    Args:
        args: most to least important mappings with email fields

    Returns:
        EmailArgs: Filled in email arguments
    """
    mapping = ChainMap(*args)

    logger.debug("making email args from input %s", mapping)
    args_dict = {
        dc_field.name: mapping.get(dc_field.name)
        for dc_field in fields(EmailArgs)
        if mapping.get(dc_field.name) is not None
    }
    logger.debug("Got args into %s", args_dict)
    return dacite.from_dict(
        data_class=EmailArgs, data=args_dict, config=dacite.Config(strict=True)
    )


def email(email_args: EmailArgs) -> None:
    """Email file(s) to address(es).

    Args:
        email_args (EmailArgs): Contains all to/from/content info
    """
    logger.info("Emailing ...")
    msg = EmailMessage()

    msg["To"] = email_args.to_mail_as_str
    msg["From"] = email_args.from_mail
    msg["Subject"] = email_args.subject
    # Eg, Date: Wed, 27 Jan 2016 20:41:27 -0500
    msg["Date"] = datetime.now(timezone.utc).astimezone().strftime("%a, %d %b %Y %X %z")

    if email_args.body:
        msg.set_content(email_args.body)
    else:
        msg.set_content("Please see attachment")

    if email_args.html:
        msg.add_alternative(email_args.html, subtype="html")

    _attach_files(msg, email_args.files)

    _send_email(email_args, msg)


def _attach_files(msg: EmailMessage, files_to_add: set[str | Path]) -> None:
    attach: str | Path
    for attach in files_to_add:
        if not isinstance(attach, Path):
            attach = Path(attach)
        ctype, encoding = mimetypes.guess_type(attach.name)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)

        msg.add_attachment(
            attach.read_bytes(),
            maintype=maintype,
            subtype=subtype,
            filename=attach.name,
        )
        logger.debug("Attached %s as %s/%s", attach, maintype, subtype)


def _send_email(email_args: EmailArgs, msg: EmailMessage) -> None:
    logger.debug("host %s\tport %d", email_args.smtphost, email_args.smtpport)
    smtp: Any  # actually is SMTP class
    if email_args.use_ssl:
        smtp = partial(smtplib.SMTP_SSL, context=ssl.create_default_context())
    else:
        smtp = smtplib.SMTP

    with smtp(host=email_args.smtphost, port=email_args.smtpport) as server:
        logger.info("emailing %s using %s", email_args.to_mail, email_args.smtphost)
        if logger.isEnabledFor(logging.DEBUG):
            server.set_debuglevel(2)
        if email_args.smtpuser is not None and email_args.smtppass is not None:
            logger.debug(
                "smtpuser %s\tsmtppass %s", email_args.smtpuser, email_args.smtppass
            )
            server.login(email_args.smtpuser, email_args.smtppass)
        server.send_message(msg)
        logger.info("emailed %s using %s", msg["To"], email_args.smtphost)
