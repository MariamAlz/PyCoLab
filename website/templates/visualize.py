from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String
import pandas as pd
import matplotlib.pyplot as plt

# Create an engine to connect to your database
engine = create_engine('sqlite:///database.db')

# Create a metadata object
metadata_obj = MetaData()

print(metadata_obj.tables[""])