import os
import sys
import json

if os.path.isfile("xf.db"):
    check = str(input("Do you want to delete and recreate the existing database? (Y/N): ")).lower()
    if check == "y":
        print("Deleting existing database...")
        os.remove("xf.db")
    else:
        print("Aborting database setup...")
        sys.exit(0)

print("Importing models and creating database...")
from models import *
db.create_all()

default_user = User(email="admin@admin.com", password="admin")
db.session.add(default_user)

print("Committing to new database...")
db.session.commit()
print("Done!")
