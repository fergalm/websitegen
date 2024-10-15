import traceback
import datetime
import inspect
import html


class ErrorHandler:
    """
    Catch errors and email the traceback to an administrator.

    Most functions are called on demand via the REST endpoint, and errors
    can be formatted as html and returned to the user immediately.

    For batch jobs, Azure doesn't automatically alert you when the job fails,
    you have to manually checks the logs, and who remembers to to that.

    This code wraps potentially failing code in a context handler which
    catches any exceptions, and sends an email about them.

    This class just catches the error and formats the email message. The
    actual business of authenticating and sending email is hadned off
    to an `email_client`. See emailer.py in this directory for some examples.

    Usage
    ------

    ::
        from emailer import DummyEmailer

        def foo():
            with ErrorHandler(DummyEmailer):
                do_something_that_might_fail()

    Notes
    --------
    An older implementation of this code created a error handling decorator.
    While this worked well inititally, it was too difficult to change the
    behaviour of the decorator dynamically, eg, for testing, or for changing
    the email recipient.s
    """

    def __init__(self, email_client, to_addr=None, subject=None):
        """

        Inputs
        ---------
        email_client
            Object responsible for actually sending the error email. See `emailer.py`

        Optional Inputs
        -----------------
        to_add
            (str or list). Email address, or list of addresses to send error report to
        subject
            (str) Subject line of email

        """

        self.to_addr = to_addr or ["fergal.mullally@gmail.com"]
        self.subject = subject or "An error has occurred"
        self.email_client = email_client

        if isinstance(self.to_addr, str):
            self.to_addr = [self.to_addr]

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            return True  # No exceptions raised

        self.email_error_report(exc_type, exc_value, exc_tb)
        return False

    def email_error_report(self, exc_type, exc_value, exc_tb):
        properties = {
            "to": self.to_addr,
            "subject": self.subject,
            "body": create_error_email_content(exc_type, exc_value, exc_tb),
        }

        self.email_client.send(properties)
        return properties


def create_error_email_content(exc_type, exc_value, exc_tb):
    try:
        frame = exc_tb.tb_next.tb_frame
    except AttributeError:
        frame = exc_tb.tb_frame

    file = html.escape(frame.f_globals["__file__"])
    func = html.escape(frame.f_code.co_name)
    lineno = frame.f_lineno
    inputargs = inspect.getargvalues(frame)
    etype = html.escape(str(exc_type))
    evalue = html.escape(str(exc_value))
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    arglist = parse_arglist(inputargs)
    kwarglist = parse_kwarglist(inputargs)

    msg = [
        "<P>A runtime error occurred in the WebsiteGen Package",
        f"while running the function '{func}' with arguments<BR>",
        f"{arglist}",
        "<BR> and keyword arguments</P>",
        f"{kwarglist}"
        f"(Note: the values of input arguments may have been modified within the function)",
        "<P></P>",
        f"<P>The exception of type {etype} says</P>",
        "<PRE>",
        f"{evalue}",
        "</PRE>",
        f"and occurred in line {lineno} of '{func}' in file {file}",
        f"at {now}",
        "",
        "<P>The traceback is:</P>",
        "<PRE>",
        f"{traceback.format_exc()}",
        "</PRE>",
    ]
    return "\n".join(msg)


def parse_arglist(inputargs) -> str:
    """Produce a html snippet listing input arguments to function and their values.

    Values are at the time the exception occurred, not the values that were
    input to the function
    """

    arglist = ["<UL>"]
    if inputargs.args is not None:
        for name in inputargs.args:
            arglist.append(f"<LI>{name} = {inputargs.locals[name]}")

    va = inputargs.varargs
    if va is not None:
        arglist.append(f"<LI>{va} = {inputargs.locals[va]}")
    arglist.append("</UL>")
    arglist = "\n".join(arglist)
    return arglist


def parse_kwarglist(inputargs) -> str:
    """Produce a html snippet listing input keyword arguments to function

    Values are at the time the exception occurred, not the values that were
    input to the function
    """
    kw = inputargs.keywords
    if kw is None:
        return "(no keyword arguments passed)"

    kwargs = inputargs.locals[kw]
    kwargslist = ["<UL>"]
    for name in kwargs:
        kwargslist.append(f"<LI>{name} = {kwargs[name]}")
    kwargslist.append("</UL>")
    kwargslist = "\n".join(kwargslist)
    return kwargslist
