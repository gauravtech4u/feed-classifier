from pymongo import Connection

connection = Connection( '127.0.0.1', 27017 )

db = connection.test_database