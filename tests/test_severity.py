import pytest
from app.severity import evaluate_severity


def test_evaluate_severity() -> None:
	assert evaluate_severity("5.5 MEDIUM") == False
	assert evaluate_severity("9.0 CRITICAL") == True
	assert evaluate_severity("Low") == False
	assert evaluate_severity("High") == True
	assert evaluate_severity("Critical") == True
	assert evaluate_severity("5.5 11.00") == False


def test_evaluate_severity_with_none() -> None:
	assert evaluate_severity(None) == False


def test_evaluate_severity_with_empty_description() -> None:
	assert evaluate_severity("") == False
