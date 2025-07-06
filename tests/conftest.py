import sys
import os
import pytest
import csv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

@pytest.fixture
def sample_csv(tmp_path):
    """фикстура, создающая временный .csv файл для тестов"""
    file_path = tmp_path / "test.csv"
    data = [
        ["name", "brand", "price", "rating"],
        ["iphone 15 pro", "apple", "999", "4.9"],
        ["galaxy s23 ultra", "samsung", "1199", "4.8"],
        ["redmi note 12", "xiaomi", "199", "4.6"],
        ["poco x5 pro", "xiaomi", "299", "4.4"],
    ]
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)
    return file_path