import pymongo
from pymongo import *
import test


class AnimalShelter(object):
    def __init__(self, user, pwd):
        self.client = MongoClient('mongodb://%s:%s@localhost:27017' % (user, pwd))
        self.database = self.client['AAC']

    # method to get the collection
    def get_collection(self, data):
        return self.database.animals

    # method to create a document with the key/value pair passed
    def create(self, data):
        self.database.animals.insert_one(data)

    # method to read documents from a collection with the key/value pair passed
    def read(self, data):
        print("Reading Data...")
        collection = self.database.animals.find(data)
        return collection

    # method to update a document with the key/value pair passed
    def update(self, data):
        newkey = input("Enter new key: ")
        newvalue = input("Enter new value: ")
        newdata = {newkey: newvalue}
        newpair = {"$set": newdata}
        self.database.animals.update_one(data, newpair)

    # method to delete a document with the key/value pair passed
    def delete(self, data):
        self.get_collection(data).delete_one(data)

    # method to start the CRUD selection

    def crud(self):

        choice = input("Would you like to (c)reate, (r)ead, (u)pdate, or (d)elete a document? Press (q) to quit: ")
        if choice == 'c' or choice == 'C':
            key = input("Enter key: ")
            value = input("Enter value: ")
            data = {key: value}
            self.create(data)
            self.crud()
        elif choice == 'r' or choice == 'R':
            key = input("Enter key: ")
            value = input("Enter value: ")
            data = {key: value}
            coll = self.read(data)
            self.print_docs(data)
            return coll

        elif choice == 'u' or choice == 'U':
            key = input("Enter key: ")
            value = input("Enter value: ")
            data = {key: value}
            self.update(data)
            self.crud()
        elif choice == 'd' or choice == 'D':
            key = input("Enter key: ")
            value = input("Enter value: ")
            data = {key: value}
            self.delete(data)
            self.crud()
        # loop until user enters 'q' or 'Q'
        elif choice == 'q' or choice == 'Q':
            print("exiting...")
            exit()
        else:
            print("Unrecognized Input...")
            self.crud()

    def get_collection_size(self, data):
        size = self.database.animals.count_documents(data)
        return size

    def print_docs(self, data):
        collection = self.database.animals.find(data)
        for x in collection:
            print(x)


def main():
    # call CRUD function loop
    AnimalShelter()


if __name__ == '__main__':
    main()
