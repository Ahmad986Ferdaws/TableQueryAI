# app/dataload.py

import pandas as pd
import os

UPLOAD_FOLDER = "uploads/"

dataframes = {}

def load_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    ext = filename.split(".")[-1]
    if ext == "csv":
        df = pd.read_csv(path)
    elif ext in ["xls", "xlsx"]:
        df = pd.read_excel(path)
    else:
        raise ValueError("Unsupported file type.")
    dataframes[filename] = df
    return df

def get_df(filename):
    return dataframes.get(filename)
