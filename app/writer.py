import os
from pathlib import Path
from datetime import datetime
from app.utils import clean_description


def create_directory(directory_name: str) -> str:
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    return directory_name


def write_to_markdown(
        directory: Path, filename: str, total_cves: int, month_year: datetime, actionable_cves: int, cve_entries: list
):
    with open(os.path.join(directory, filename), 'w') as file:
        file.write("# Summary\n")
        file.write(f"* **Total CVEs checked:** {total_cves}\n")
        file.write(f"* **Date Range:** {month_year}\n")
        file.write(f"* **Actionable CVEs:** {actionable_cves}\n")
        for entry in cve_entries:
            cleaned_description = clean_description(entry['description'])
            file.write(f"* **Date:** {entry['date']}\n")
            file.write(f"* **Title:** {entry['title']}\n")
            if entry['link']:
                file.write(f"* **Link:** [{entry['link']}]({entry['link']})\n")
            file.write(f"* **CVE Name:** {entry['cve_name']}\n")
            file.write(f"* **CVE URL:** {entry['cve_url']}\n")
            if entry['severity']:
                file.write(f"* **Severity:** {entry['severity']}\n\n")
            file.write(f"* **Matched Keywords:** {', '.join(entry['keywords'])}\n")
            file.write(f"* **Description:** {cleaned_description}\n\n")
            file.write(f"* **Extra Details:** {entry['extra_details']}\n\n")
            # Add some spacing and delineation between the reports to make it easier to read.
            file.write("\n\n")
            file.write("----------------------------------------------------------------------------------------------")
            file.write("\n\n")
