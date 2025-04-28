from sqlalchemy import create_engine, MetaData, text, Integer, String
from sqlalchemy.schema import Column, Table
from sqlalchemy.exc import SQLAlchemyError
from fastapi import FastAPI
from pydantic import BaseModel
import os
from urllib.parse import quote_plus

app = FastAPI()

# Get MySQL connection parameters from environment variables
mysql_user = os.environ.get("MYSQL_USER", "evaluser")
mysql_password = os.environ.get("MYSQL_PASSWORD", "evalmysql@..")
mysql_host = os.environ.get("MYSQL_HOST", "mysql")
mysql_port = os.environ.get("MYSQL_PORT", "3307")
mysql_database = os.environ.get("MYSQL_DATABASE", "datasc")

# URL encode the password to handle special characters
encoded_password = quote_plus(mysql_password)
print(f"Connection info - User: {mysql_user}, Host: {mysql_host}, Port: {mysql_port}, DB: {mysql_database}")
print(f"Original password: {mysql_password}")
print(f"Encoded password: {encoded_password}")

# Build the connection string with URL-encoded password
conn_string = f"mysql://{mysql_user}:{encoded_password}@{mysql_host}:{mysql_port}/{mysql_database}"

print(f"Connection string (masked): {conn_string.replace(encoded_password, '********')}")

mysql_engine = create_engine(conn_string)

metadata = MetaData()

class TableSchema(BaseModel):
    table_name: str
    columns: dict

@app.get("/")
async def root():
    return {"status": "FastAPI is running"}

@app.get("/tables")
async def get_tables():
    try:
        with mysql_engine.connect() as connection:
            results = connection.execute(text('SHOW TABLES;'))
            dict_res = {}
            dict_res['database'] = [str(result[0]) for result in results.fetchall()]
            return dict_res
    except SQLAlchemyError as e:
        return {"error": str(e)}

@app.put("/table")
async def create_table(schema: TableSchema):
    columns = [Column(col_name, eval(col_type)) for col_name, col_type in schema.columns.items()]
    table = Table(schema.table_name, metadata, *columns)
    try:
        metadata.create_all(mysql_engine, tables=[table], checkfirst=False)
        return f"{schema.table_name} successfully created"
    except SQLAlchemyError as e:
        return dict({"error_msg": str(e)})