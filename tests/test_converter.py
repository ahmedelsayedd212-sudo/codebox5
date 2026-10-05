from utils.converter import (
    km_to_miles,
    miles_to_km,
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    kg_to_pounds,
    pounds_to_kg
)


def test_km_to_miles():
    assert round(km_to_miles(10), 2) == 6.21


def test_miles_to_km():
    assert round(miles_to_km(10), 2) == 16.09


def test_celsius_to_fahrenheit():
    assert celsius_to_fahrenheit(0) == 32


def test_fahrenheit_to_celsius():
    assert fahrenheit_to_celsius(32) == 0


def test_kg_to_pounds():
    assert round(kg_to_pounds(10), 2) == 22.05


def test_pounds_to_kg():
    assert round(pounds_to_kg(10), 2) == 4.54