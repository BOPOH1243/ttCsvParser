import pytest
import os
import csv
from csv_processor import CSVProcessor

def test_filter_gt(sample_csv):
    processor = CSVProcessor(sample_csv)
    filtered = processor.filter_data("price>500")
    assert len(filtered) == 2
    assert filtered[0]["name"] == "iphone 15 pro"
    assert filtered[1]["name"] == "galaxy s23 ultra"

def test_filter_add_new_operator(sample_csv):
    '''не знаю зачем я это добавляю, но пусть будет'''
    processor = CSVProcessor(sample_csv)
    processor.OPERATORS['<=']=lambda a, b: a <= b
    filtered = processor.filter_data("price<=299")
    assert len(filtered) == 2
    assert filtered[0]["name"] == "redmi note 12"
    assert filtered[1]["name"] == "poco x5 pro"

def test_filter_eq(sample_csv):
    processor = CSVProcessor(sample_csv)
    filtered = processor.filter_data("brand=xiaomi")
    assert len(filtered) == 2
    assert all(row["brand"] == "xiaomi" for row in filtered)

def test_aggregate_avg(sample_csv):
    processor = CSVProcessor(sample_csv)
    result = processor.aggregate_data(processor.data, "avg", "price")
    assert result == (999 + 1199 + 199 + 299) / 4

def test_aggregate_min(sample_csv):
    processor = CSVProcessor(sample_csv)
    filtered = processor.filter_data("brand=xiaomi")
    result = processor.aggregate_data(filtered, "min", "rating")
    assert result == 4.4