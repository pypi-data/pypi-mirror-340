# A tool for spitting out .eml files from a template and a CSV file

Built for UNSW tutors, because we don't get to use SMTP with Outlook, since we can't add OAuth applications.

It can also do SMTP for when you have the luxury.

```
Usage: class-email [OPTIONS] DATAFILE TEMPLATE SUBJECT

  Creates .eml files for each row in DATAFILE. The email body is generated
  from TEMPLATE, which is a Jinja2 template. Each email's subject will be
  SUBJECT. Can optionally be opened in your preferred email program or sent
  via SMTP.

Options:
  --filter <INTEGER FILENAME>...  A column number followed by the name of a
                                  file containing values that that column
                                  needs to match. Values should be separated
                                  by newlines.
  --sender TEXT                   If specified, the From header is added to
                                  .eml files - useful if you have multiple
                                  sending addresses configured in your email
                                  client. If specified in SMTP mode, will
                                  override the sender address (which defaults
                                  to the SMTP username).
  --cc TEXT                       If specified, the CC header is added, to CC
                                  additional email addresses to all emails.
  --reply-to TEXT                 If specified, the Reply-To header is added,
                                  to indicate to receiving email clients where
                                  replies should be directed.
  --email-column INTEGER          The column to use as the email address.
                                  First column is column 0. Defaults to 0.
  --skip-rows INTEGER             Number of rows to skip (e.g. headers).
                                  Defaults to 0.
  --outdir DIRECTORY              A directory where .eml files should be
                                  output to. Defaults to ./out.
  --smtp                          Sends emails via SMTP using the environment
                                  variables `SMTP_HOST`, `SMTP_USER`,
                                  `SMTP_PASS`, `SMTP_PORT`.
  --yes                           Automatically answers 'yes' when prompted to
                                  open files or send emails.
  --no                            Automatically answers 'no' when prompted to
                                  open files or send emails.
  --help                          Show this message and exit.
```