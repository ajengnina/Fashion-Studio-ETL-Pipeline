# tests/test_load.py
import pandas as pd
import pytest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load

def test_save_to_csv(tmp_path):
    df = pd.DataFrame({
        "title": ["Hoodie"],
        "price": [160000.0],
        "rating": [4.7],
        "colors": ["3 Colors"],
        "size": ["Size: M"],
        "gender": ["Gender: Men"],
        "timestamp": ["2025-05-19 15:00:00"]
    })

    path = tmp_path / "product.csv"
    load.load_to_csv(df, path)
    loaded = pd.read_csv(path)

    assert not loaded.empty
    assert list(loaded.columns) == list(df.columns)


@patch("utils.load.Credentials.from_service_account_file")
@patch("utils.load.gspread.authorize")
def test_load_to_gsheet(mock_authorize, mock_credentials):
    df = pd.DataFrame({
        "col1": [1, 2],
        "col2": ["a", "b"]
    })

    mock_creds_instance = MagicMock()
    mock_credentials.return_value = mock_creds_instance

    mock_client = MagicMock()
    mock_authorize.return_value = mock_client

    mock_spreadsheet = MagicMock()
    mock_client.open_by_url.return_value = mock_spreadsheet

    mock_worksheet = MagicMock()
    mock_spreadsheet.sheet1 = mock_worksheet

    load.load_to_gsheet(df, "fashion-studio.json", "https://docs.google.com/spreadsheets/d/1bYSconAsDjXMf9Qhp1KgRlk7wGw9I1jNzxPd_GeFdbQ/edit?gid=0#gid=0")

    mock_credentials.assert_called_once_with("fashion-studio.json", scopes=['https://www.googleapis.com/auth/spreadsheets'])
    mock_authorize.assert_called_once_with(mock_creds_instance)
    mock_client.open_by_url.assert_called_once_with("https://docs.google.com/spreadsheets/d/1bYSconAsDjXMf9Qhp1KgRlk7wGw9I1jNzxPd_GeFdbQ/edit?gid=0#gid=0")
    mock_worksheet.clear.assert_called_once()
    mock_worksheet.update.assert_called_once_with([df.columns.tolist()] + df.values.tolist())


@patch("utils.load.create_engine")
@patch("utils.load.pd.DataFrame.to_sql")
def test_load_to_postgresql(mock_to_sql, mock_create_engine):
    df = pd.DataFrame({
        "col1": [1, 2],
        "col2": ["a", "b"]
    })

    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine

    load.load_to_postgresql(df, "postgresql://ajengnina12:123456@localhost:5432/fashion_db", "fashion_products")

    mock_create_engine.assert_called_once_with("postgresql://ajengnina12:123456@localhost:5432/fashion_db")
    mock_to_sql.assert_called_once_with("fashion_products", con=mock_engine, index=False, if_exists='append')

