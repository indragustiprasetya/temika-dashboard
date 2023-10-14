import pymongo
import json
import os

# Constants for config keys
def load_config():
    # Get the absolute path to config.json
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of this script
    config_path = os.path.join(current_dir, '../config.json')

    with open(config_path) as config:
        read_config = json.load(config)
        db_name = read_config['db_name']
        employee_collection = read_config['collections']['employee']
        user_collection = read_config['collections']['internal_user']
        address = read_config['db_address']
        port = int(read_config['db_port'])
        return db_name, employee_collection, user_collection, address, port

def connect_employee():
    db_name, employee_collection, user_collection, address, port = load_config()

    client = pymongo.MongoClient(host=address, port=port)
    dbname = client[db_name]
    employee_coll = dbname[employee_collection]
    user_coll = dbname[user_collection]

    return dbname, employee_coll, user_coll  # Return both the database and collection objects
