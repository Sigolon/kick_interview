from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import FileResponse
from PIL import Image
from pydantic import BaseModel
import sqlite3
import pandas
import os 


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "This is fastapi for kick interview"}

@app.get("/database-info")
def get_database_info():
    conn = sqlite3.connect('data_base.db')
    cursor = conn.cursor()
    cursor.execute("SELECT sqlite_version();")
    version = cursor.fetchone()[0]
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    database_info = {
        "version": version,
        "tables": [table[0] for table in tables]
    }
    return database_info

@app.get("/table_info")
def get_table_info(table_name: str = Query(..., description="Filter player_info by horse_id")):
    conn = sqlite3.connect('data_base.db')
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    conn.close()
    table_info = {
        "table_name": table_name,
        "columns": [{"name": col[1], "type": col[2]} for col in columns]
    }
    return table_info

@app.get("/download/table/{table_name}")
def download_table_data(table_name: str = Path(..., description="Table name in the database")):
    conn = sqlite3.connect('data_base.db')
    query = f"SELECT * FROM {table_name}"
    df = pandas.read_sql_query(query, conn)
    conn.close()
    csv_file_path = f"db_table_csv/{table_name}.csv"
    df.to_csv(csv_file_path, index=False)
    file_response = FileResponse(csv_file_path, media_type="text/csv", filename=csv_file_path)
    return file_response

@app.get("/download/pg_to_pdf/{horse_id}")
def download_jpg_to_pdf(horse_id: str = Path(..., description="Horse ID")):
    jpg_file_path = f"house_image/{horse_id}.jpg"
    if not os.path.exists(jpg_file_path):
        raise HTTPException(status_code=404, detail="No JPG files found for the specified horse_id")
        
    pdf_file_path = f"horse_pdf/{horse_id}.pdf"
    with Image.open(jpg_file_path) as img:
        img.save(pdf_file_path, "PDF", resolution=100.0)

    file_response = FileResponse(pdf_file_path, media_type="application/pdf", filename=pdf_file_path)
    return file_response

@app.get("/player_info")
def get_player_info_by_horse_id(horse_id: str = Query(..., description="Filter player_info by horse_id")):
    conn = sqlite3.connect('data_base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM player_info WHERE horse_id = ?', (horse_id,))
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        result_dict = dict(zip(columns, row))
        results.append(result_dict)
    return results

@app.get("/player_info/horse_id/unique_horse_ids")
def get_unique_horse_ids():
    conn = sqlite3.connect('data_base.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT horse_id FROM player_info")
    unique_horse_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return {"unique_horse_ids": unique_horse_ids}

