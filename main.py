import feedparser
from datetime import datetime
import calendar
from typing import Dict, Any

from app.extraction import extract_cve_details
from app.writer import create_directory, write_to_markdown
from app.severity import evaluate_severity
from app.utils import is_actionable
from configurations import feed_configs


def main() -> None:
    total_cves: int = 0
    actionable_cves: int = 0
    cve_details: list = []

    for feed_url, config in feed_configs.items():
        feed: feedparser.FeedParserDict = feedparser.parse(feed_url)
        for entry in feed.entries:
            total_cves += 1
            date_tag: str = config["date"]
            title_tag: str = config["title"]
            link_tag: str = config.get("link", "")
            description_tag: str = config["description"]
            extra_details_tag: str = config["extra_details"]

            if config.get("content_parse"):
                cve_name, cve_url, severity = extract_cve_details(entry, config)
            else:
                cve_name, cve_url, severity = extract_cve_details(entry, config)

            if not evaluate_severity(severity):
                continue  # Skip to the next CVE if severity doesn't meet criteria

            date: Any = getattr(entry, date_tag, None)
            date_str: str = ""
            month_year: str = ""
            month_year_day: str = ""
            if date:
                formatted_date: datetime = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")
                date_str = formatted_date.strftime("%Y-%m-%d")
                month_year = formatted_date.strftime("%B-%Y")
                my_date: datetime = datetime.today()
                day_name: str = calendar.day_name[my_date.weekday()]
                month_year_day = day_name + "-" + formatted_date.strftime("%d-%B-%Y")

            title: str = getattr(entry, title_tag, "No Title")
            link: str = getattr(entry, link_tag, "")
            description: str = getattr(entry, description_tag, "")
            extra_details: str = getattr(entry, extra_details_tag, "")

            actionable: bool
            keywords: list
            actionable, keywords = is_actionable(description)
            if actionable:
                actionable_cves += 1
                cve_details.append({
                    'date': date_str,
                    'title': title,
                    'link': link,
                    'cve_name': cve_name,
                    'cve_url': cve_url,
                    'severity': severity,
                    'keywords': keywords,
                    'description': description,
                    'extra_details': extra_details
                })

    directory_name: str = f"CVEs-{month_year}"
    directory = create_directory(directory_name)
    filename: str = f"CVE_Report_{month_year_day}.md"
    write_to_markdown(directory, filename, total_cves, month_year, actionable_cves, cve_details)

    print(f"Report generated: {filename} in directory {directory_name}")


if __name__ == "__main__":
    main()
