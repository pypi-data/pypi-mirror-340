import os
import pandas as pd


def convert_csv_to_str(csv_path: str):
    csv_path = os.path.join(os.path.dirname(__file__), csv_path)
    try:
        df = pd.read_csv(csv_path)
        headers = df.columns.tolist()
        data_rows = df.values.tolist()
        list_of_lists_with_headers = [headers] + data_rows
        data = str(list_of_lists_with_headers)
        return data
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None