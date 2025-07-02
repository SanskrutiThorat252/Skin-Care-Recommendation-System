import pandas as pd
from sqlalchemy import create_engine

# Path to your CSV
csv_path = 'C:\\Users\\vanka\\AppData\\Local\\Programs\\Python\\Python310\\Scripts\\Skinflask\\Skinpro.csv'

# Load CSV into DataFrame
df = pd.read_csv(csv_path)

# Database connection info
username = "postgres"
password = "root"
host = "localhost"
port = 5432
database = "product_skincare"

# Create connection using SQLAlchemy
engine = create_engine(f'postgresql+psycopg2://{"postgres"}:{"root"}@{"localhost"}:{5432}/{"product_skincare"}')

# Insert into table (replace 'skincare_products' with your actual table name)
df.to_sql('skincare_products', con=engine, if_exists='replace', index=False)

print("✅ Data imported successfully into PostgreSQL.")








# C:/Users/aci/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0/LocalCache/local-packages/Python312/Scripts/Skinflask/product_skincare.csv