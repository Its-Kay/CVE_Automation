import requests
from typing import Optional, Union, Dict, Any, Tuple
from bs4 import BeautifulSoup, Tag, NavigableString
from app.constants import base_url


def fetch_cve_severity(cve_id: str) -> str:
    full_url: str = base_url + cve_id

    response: requests.Response = requests.get(full_url)
    if response.status_code == 200:
        soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
        severity_span: Optional[Union[Tag, NavigableString]] = soup.find('a', {'data-testid': 'vuln-cvss3-panel-score'})
        if severity_span:
            return severity_span.text
    return ""


def parse_cve_details(content_html: Union[str, bytes]) -> Tuple[str, str, str]:
    # Needed to parse out the content blob from the GCloud Sec Bulletin <content> tag
    soup: BeautifulSoup = BeautifulSoup(content_html, 'html.parser')
    cve_name: str = ""
    cve_url: str = ""
    severity: str = ""

    cve_link = soup.find('a', href=lambda href: href and "cve.mitre.org" in href)
    if cve_link:
        cve_url = cve_link['href']
        cve_name = cve_link.get_text()

    severity_td = soup.find('td', string=lambda text: text and text.lower() in ["low", "medium", "high", "critical"])
    if severity_td:
        severity = severity_td.get_text()

    return cve_name, cve_url, severity


def extract_cve_details(entry: Dict[str, Any], config: Dict[str, Any]) -> Tuple[str, str, str]:
    if config.get("content_parse"):
        content_html: str = entry['content'][0]['value'] if 'content' in entry else ""
        return parse_cve_details(content_html)
    else:
        cve_id: str = getattr(entry, config.get("cve_id_tag", ""), "")
        severity: str = fetch_cve_severity(cve_id) if cve_id else ""
        return cve_id, "", severity
