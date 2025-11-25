# Import DB and export CSVs for handling

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd

load_dotenv()
link_db = os.getenv ("SUPABASE_DB_URL")
engine = create_engine(link_db)

df1 = pd.read_sql("SELECT * FROM investments.list_orders", engine)
df1.to_csv("demo_database_creation/exported_views/investments.list_orders.csv", encoding='utf-8-sig')

df2 = pd.read_sql("SELECT * FROM investments.table_for_geographies", engine)
df2.to_csv("demo_database_creation/exported_views/investments.table_for_geographies.csv", encoding='utf-8-sig')

df3 = pd.read_sql("SELECT * FROM investments.table_for_alocations", engine)
df3.to_csv("demo_database_creation/exported_views/investments.table_for_alocations.csv", encoding='utf-8-sig')