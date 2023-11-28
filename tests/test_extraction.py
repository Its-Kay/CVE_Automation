import pytest
import requests_mock
from app.extraction import fetch_cve_severity, parse_cve_details, extract_cve_details
from unittest.mock import Mock


def test_fetch_cve_severity_success() -> None:
    cve_id: str = "CVE-2021-1234"
    expected_severity: str = "7.8 HIGH"

    with requests_mock.Mocker() as m:
        m.get(f"https://nvd.nist.gov/vuln/detail/{cve_id}",
              text=f'<a data-testid="vuln-cvss3-panel-score">{expected_severity}</a>')
        severity: str = fetch_cve_severity(cve_id)

    assert severity == expected_severity


def test_fetch_cve_severity_not_found() -> None:
    cve_id: str = "CVE-2021-1234"

    with requests_mock.Mocker() as m:
        m.get(f"https://nvd.nist.gov/vuln/detail/{cve_id}", status_code=404)
        severity: str = fetch_cve_severity(cve_id)

    assert severity == ""


def test_parse_cve_details() -> None:
    sample_html: str = '<a href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-1234">CVE-2021-1234</a><td>High</td>'
    cve_name: str
    cve_url: str
    severity: str
    cve_name, cve_url, severity = parse_cve_details(sample_html)

    assert cve_name == "CVE-2021-1234"
    assert cve_url == "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-1234"
    assert severity == "High"


def test_extract_cve_details_content_parse() -> None:
    entry: dict = {"content": [
        {"value": '<a href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-1234">CVE-2021-1234</a><td>High</td>'}
    ]}
    config: dict = {"content_parse": True}

    cve_name: str
    cve_url: str
    severity: str
    cve_name, cve_url, severity = extract_cve_details(entry, config)

    assert cve_name == "CVE-2021-1234"
    assert cve_url == "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-1234"
    assert severity == "High"


def test_extract_cve_details_without_content_parse(mocker: Mock) -> None:
    mocker.patch('app.extraction.fetch_cve_severity', return_value="")

    entry: dict = {"cveID": "CVE-2021-1234"}
    config: dict = {"content_parse": False, "cve_id_tag": "cveID"}

    expected_cve_id: str = ""
    expected_severity: str = ""

    cve_id: str
    severity: str
    cve_id, _, severity = extract_cve_details(entry, config)

    assert cve_id == expected_cve_id
    assert severity == expected_severity
