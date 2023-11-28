import pytest
import os
from requests_mock import mocker
from unittest.mock import Mock
from pathlib import Path
from app.writer import create_directory, write_to_markdown


def test_create_directory(tmp_path: Path) -> None:
    directory_name: Path = tmp_path / "test_directory"
    create_directory(directory_name)
    assert os.path.exists(directory_name)


def test_write_to_markdown(tmp_path: Path, mocker: Mock) -> None:
    mocker.patch('app.writer.clean_description', return_value="Cleaned Description")

    directory: Path = tmp_path / "test_markdown"
    filename: str = "test.md"
    total_cves: int = 10
    month_year: str= "January-2023"
    actionable_cves: int = 5
    cve_entries: list = [
        {
            'date': '2023-01-01',
            'title': 'Test CVE',
            'link': 'https://example.com',
            'cve_name': 'CVE-2023-0001',
            'cve_url': 'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0001',
            'severity': 'High',
            'keywords': ['keyword1', 'keyword2'],
            'description': '<p>Test Description</p>',
            'extra_details': 'Some extra details'
        }
    ]

    create_directory(directory)
    write_to_markdown(directory, filename, total_cves, month_year, actionable_cves, cve_entries)

    file_path: Path = directory / filename
    assert file_path.exists()

    with open(file_path, 'r') as file:
        content = file.read()
        assert "Test CVE" in content
        assert "Cleaned Description" in content
        assert "CVE-2023-0001" in content
        assert "keyword1, keyword2" in content
        assert "Some extra details" in content
