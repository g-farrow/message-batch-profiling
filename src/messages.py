from uuid import uuid4
from faker import Faker
from json import loads

fake = Faker()


class Message:

    def __init__(self):
        self.id = uuid4().hex
        self.name = fake.name()
        self.address = fake.address()
        self.dict = {'id': self.id, 'name': self.name, 'address': self.address}
        self.str = loads(self.dict)
