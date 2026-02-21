import logging
import os
import pandas as pd # Pandas insert ke liye zaroori hai
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String # Imports add kiye

# 1. Database Connection Setup
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")
DB_HOST = "db"  
DB_PORT = "5432"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# 2. Table Definition & Creation
users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('age', Integer)
)
metadata.create_all(engine)

# 3. Logging Setup
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 4. Pydantic Model
class UserRecord(BaseModel):
    name: str
    age: int = Field(gt=0, lt=120)

    @field_validator('name')
    @classmethod
    def name_must_be_capital(cls, v: str) -> str:
        if not v[0].isupper():
            raise ValueError('First Letter of Name should be capital')
        return v

# 5. THE MISSING FUNCTION: Data Load karne ke liye
def load_to_postgres(valid_data_list):
    try:
        if valid_data_list:
            # List of dicts ko DataFrame mein badlo
            df_to_save = pd.DataFrame(valid_data_list)
            # Database mein push karo
            df_to_save.to_sql('users', engine, if_exists='append', index=False)
            logging.info(f"SUCCESS: {len(valid_data_list)} records inserted into DB.")
            return True
        return False
    except Exception as e:
        logging.error(f"DATABASE ERROR: {str(e)}")
        return False