import os
import platform
import smtplib
import subprocess
from csv import reader
from pathlib import Path
from typing import Literal, Optional, TextIO, TypedDict

import click
from jinja2 import DictLoader, Environment, select_autoescape
from tqdm import tqdm


class EmailToSend(TypedDict):
    to: str
    file: Path
    content: str


@click.command(
    help="Creates .eml files for each row in DATAFILE. The email body is generated from TEMPLATE, which is a Jinja2 template. Each email's subject will be SUBJECT. Can optionally be opened in your preferred email program or sent via SMTP."
)
@click.option(
    "--filter",
    help="A column number followed by the name of a file containing values that that column needs to match. Values should be separated by newlines.",
    type=(int, click.File("r")),
)
@click.option(
    "--sender",
    help="If specified, the From header is added to .eml files - useful if you have multiple sending addresses configured in your email client. If specified in SMTP mode, will override the sender address (which defaults to the SMTP username).",
)
@click.option(
    "--cc",
    help="If specified, the CC header is added, to CC additional email addresses to all emails.",
)
@click.option(
    "--reply-to",
    help="If specified, the Reply-To header is added, to indicate to receiving email clients where replies should be directed.",
)
@click.option(
    "--email-column",
    type=int,
    default=0,
    help="The column to use as the email address. First column is column 0. Defaults to 0.",
)
@click.option(
    "--skip-rows",
    default=0,
    help="Number of rows to skip (e.g. headers). Defaults to 0.",
)
@click.option(
    "--outdir",
    type=click.Path(file_okay=False, writable=True, resolve_path=True, path_type=Path),
    default="./out",
    help="A directory where .eml files should be output to. Defaults to ./out.",
)
@click.option(
    "--smtp",
    is_flag=True,
    help="Sends emails via SMTP using the environment variables `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS`, `SMTP_PORT`.",
)
@click.option(
    "--yes",
    "prompt_response",
    flag_value="yes",
    help="Automatically answers 'yes' when prompted to open files or send emails.",
)
@click.option(
    "--no",
    "prompt_response",
    flag_value="no",
    help="Automatically answers 'no' when prompted to open files or send emails.",
)
@click.argument("datafile", type=click.File("r", errors="surrogateescape"))
@click.argument(
    "template",
    type=click.File("r"),
)
@click.argument("subject")
def main(
    prompt_response: Optional[Literal["yes", "no"]],
    skip_rows: int,
    filter: Optional[tuple[int, TextIO]],
    email_column: int,
    sender: Optional[str],
    cc: Optional[str],
    reply_to: Optional[str],
    smtp: bool,
    outdir: Path,
    datafile: TextIO,
    template: TextIO,
    subject: str,
):
    if filter:
        filter_column, filter_file = filter
        allowed_values = [
            line.strip() for line in filter_file.readlines() if line.strip()
        ]
    else:
        filter_column = None
        allowed_values = None

    csv = reader(datafile)
    data = []
    for i, row in enumerate(csv):
        if i < skip_rows or (
            filter_column is not None
            and allowed_values is not None
            and row[filter_column].strip() not in allowed_values
        ):
            continue
        data.append(row)

    loader = DictLoader({"template.html": template.read()})
    env = Environment(loader=loader, autoescape=select_autoescape())
    t = env.get_template("template.html")

    if not outdir.exists():
        outdir.mkdir(parents=True)

    emails: list[EmailToSend] = []
    for row in data:
        to_addr = row[email_column]

        target = to_addr.split("@")[0]
        file = outdir / f"{target}.eml"

        content = ""
        if sender:
            content += f"From: <{sender}>\r\n"
        content += f"To: {to_addr}\r\n"
        if cc:
            content += f"CC: <{cc}>\r\n"
        if reply_to:
            content += f"Reply-To: <{reply_to}>\r\n"
        content += f"Subject: {subject}\r\n"
        if not smtp:
            content += "X-Unsent: 1\r\n"
        content += "Content-Type: text/html\r\n"
        content += "\r\n\r\n"

        content += t.render(data=row)
        with open(file, "w", errors="surrogateescape") as f:
            f.write(content)

        emails.append({"to": to_addr, "file": file, "content": content})

    click.echo(
        f"{len(data)} .eml files have been output to ./{outdir.relative_to(Path().resolve())}."
    )
    prompt = (
        "Do you want to open the email files in your preferred email client?"
        if not smtp
        else "Do you want to send the emails using your configured SMTP settings?"
    )
    if prompt_response != "no" and (prompt_response == "yes" or click.confirm(prompt)):
        if not smtp:
            for email in emails:
                fn = email["file"].resolve()
                if platform.system() == "Darwin":  # macOS
                    subprocess.call(("open", str(fn)))
                elif platform.system() == "Windows":  # Windows
                    os.startfile(str(fn))  # type: ignore
                else:  # Linux
                    subprocess.call(("xdg-open", str(fn)))
        else:
            hostname = os.getenv("SMTP_HOST", "")
            username = os.getenv("SMTP_USER", "")
            password = os.getenv("SMTP_PASS", "")
            try:
                port = int(os.getenv("SMTP_PORT", "a"))
            except ValueError:
                port = None
            encryption = os.getenv("SMTP_ENCRYPTION", "starttls").lower()
            if hostname == "":
                raise click.ClickException("Missing `SMTP_HOST` environment variable.")
            if username == "":
                raise click.ClickException("Missing `SMTP_USER` environment variable.")
            if password == "":
                raise click.ClickException("Missing `SMTP_PASS` environment variable.")
            if port is None:
                raise click.ClickException(
                    "Missing or invalid `SMTP_PORT` environment variable."
                )
            if encryption not in ["starttls", "none", "ssl"]:
                raise click.ClickException(
                    "Invalid `SMTP_HOST` environment variable. Allowed values: starttls (default), none, ssl"
                )

            if encryption == "ssl":
                smtp_client = smtplib.SMTP_SSL(hostname, port)
            else:
                smtp_client = smtplib.SMTP(hostname, port)
                smtp_client.starttls()

            smtp_client.login(username, password)

            for email in tqdm(emails):
                smtp_client.sendmail(
                    sender or username,
                    email["to"],
                    email["content"],
                )

            smtp_client.quit()
