from email.message import EmailMessage
import smtplib


class Gmail:
    """Send emails from a Gmail account

    As of 2022, Gmail won't let you authenticate programtically unless you
    * Set up 2FA
    * Create an [App password](https://towardsdatascience.com/automate-sending-emails-with-gmail-in-python-449cc0c3c317)

    This app password is what is expected to initialise the object.
    If you use your normal password you will an `SMTPAuthenticationError`
    """

    def __init__(self, user, pwd, host="smtp.gmail.com", port=465):
        """
        Parameters
        ---------------
        * user
            * The "From" email address
        * pwd
            * The app password (see above)

        Optional Inputs
        --------------------
        host, port
            Leave these values at their defaults unless you have a
            very good reason to change them.
        """
        self.user = user
        self.pwd = pwd
        self.host = host
        self.port = port

    def send(self, msg: dict) -> None:
        """
        Send an email message.

        Parameters
        ------------
        * msg
            The input message. Contains the keys
            * to
                * The intended recipient
            * subject
                * The subject line
            * body
                * The text of the email to send

        Attachments aren't supported yet, but wouldn't be hard to implement
        """

        emsg = EmailMessage()
        emsg["From"] = msg.get("from", self.user)
        emsg["To"] = msg["to"]
        emsg["Subject"] = msg["subject"]
        emsg.set_content(msg["body"])

        with smtplib.SMTP_SSL(host=self.host, port=self.port) as smtp:
            smtp.login(self.user, self.pwd)
            smtp.send_message(emsg)


class DummyEmail:
    def __init__(self):
        pass

    def send(self, msg: dict):
        print(f"FROM: {msg.get('from', '<NotSet>')}")
        print(f"TO: {msg['to']}")
        print(f"SUBJECT: {msg['subject']}")
        print(f"\n: {msg['body']}")


def test_email():
    msg = EmailMessage()
    msg["To"] = "Bob"
    msg["Subject"] = "Eve"
    msg.set_content("She can NEVER know")
    DummyEmail().send(msg)
