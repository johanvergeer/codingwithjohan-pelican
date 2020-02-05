from typing import List
import imaplib

from typing_extensions import Protocol


class EmailReceiver(Protocol):
    def login(self, user: str, password: str): ...

    def select(self, mailbox='INBOX', readonly=False): ...

    def uid(self, command, *args): ...


class EmailClient:
    def __init__(self, email_receiver: EmailReceiver):
        self.server = email_receiver

    def receive(self, username: str, password: str) -> List[str]:
        self.server.login(username, password)
        self.server.select('INBOX')

        result, data = self.server.uid('search', None)

        # Process result and data


receiver: EmailReceiver = imaplib.IMAP4_SSL("localhost", 993)
client = EmailClient(receiver)
results = client.receive("codingwithjohan@gmail.com", "mysupersecretpasswd")

