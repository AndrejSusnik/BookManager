import json


class BookInfo:
    def __init__(self, title="", author="", publisher="", year_of_publishing="", description=""):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.year_of_publishing = year_of_publishing
        self.description = description

    def toJSON(self):
        return self.__dict__
