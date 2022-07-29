from collections import namedtuple
import ssl
import smtplib

Credentials = namedtuple('Credentials', 'username password')


class EmailSender:
    def __init__(self, port, smtp_server, credentials:Credentials, ssl_enable:bool=False) -> None:
        self.port = port
        self.smtp_server = smtp_server
        self.credentials = credentials
        self.ssl_enable = ssl_enable
        self.connection = None


    def __enter__(self):
        if not self.ssl_enable:
            self.connection = smtplib.SMTP(self.smtp_server, self.port)
        else:
            ssl_context = ssl.create_default_context()
            self.connection = smtplib.SMTP_SSL(self.smtp_server, self.port, context=ssl_context)

        self.connection.login(self.credentials.username, self.credentials.password)
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


    def sendmail(self, sender:str, receiver:str, message:str) -> None:
        self.connection.sendmail(sender, receiver, message)
