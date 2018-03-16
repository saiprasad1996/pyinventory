import os, json

#  For mailing
# From and to mails are same
EMAIL = ""
MAIL_PASSWORD = ""
MAIL_HOST = ""
MAIL_PORT = 000  # This should be a number

# Database Configuration

DB_NAME = "pyinventory"
DB_PASSWORD = ""
DB_USER = "root"
DB_HOST = "localhost"
DB_PORT = 3306

STOCK_LIMIT = 5
COMPUTER_ID = "C1"

current_dir = os.path.dirname(__file__)
# print(current_dir)
config_file = os.path.join(current_dir, "config.json")

config = ""
try:
    with open(config_file) as f:
        config = f.read()

    config = json.loads(config)

    # From and to mails are same
    EMAIL = config["email"]
    MAIL_PASSWORD = config["mail_password"]
    MAIL_HOST = config["mail_host"]
    MAIL_PORT = int(config["mail_port"])  # This should be a number

    # Database Configuration

    DB_NAME = config["db_name"]
    DB_PASSWORD = config["db_password"]
    DB_USER = config["db_user"]
    DB_HOST = config["db_host"]
    DB_PORT = int(config["db_port"])

    STOCK_LIMIT = int(config["stock_limit"])
    COMPUTER_ID = config["computer_id"]

except:
    print("An exception occured while reading the file")

