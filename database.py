from pymongo import MongoClient
try:
    # Replace 'your_connection_string' with your MongoDB connection string
    # The connection string typically looks like: mongodb://username:password@host:port/database
    connection_string = 'mongodb://localhost:27017'

    # Establish a connection to MongoDB
    client = MongoClient(connection_string)

    # Access a specific database
    db = client['anox']  # Replace 'your_database_name' with your database name

    # Access a specific collection within the database
    collection = db['halal']  # Replace 'your_collection_name' with your collection name

    if client is not None and db is not None:
            print("Connection to MongoDB established successfully!")
            # You can proceed with further operations on the database
    else:
            print("Connection failed.")

except Exception as e:
    print(e)
    print("Connection failed.")


def insert_period(period,incomes,expenses,comments):
    try:
        # Insert a document into the collection
        collection.insert_one(
            {
                "period": period,
                "incomes": incomes,
                "expenses": expenses,
                "comments": comments
            }
        )
        print("Data inserted successfully!")
    except Exception as e:
        print(e)
        print("Data insertion failed.")


def fetch_all_periods():
    try:
        # Fetch all documents in the collection
        cursor = collection.find({})
        for document in cursor:
            print(document)
        
    except Exception as e:
        print(e)
        print("Data fetching failed.")
    # return the period list
    return  collection.distinct("period")
def get_period(period):
    try:
        # Fetch all documents in the collection
        cursor = collection.find({"period":period})
        for document in cursor:
            print(document)
    except Exception as e:
        print(e)
        print("Data fetching failed.")
    # return the data for the period
    return  collection.find_one({"period":period})
