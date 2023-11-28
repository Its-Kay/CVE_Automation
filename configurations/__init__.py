feed_configs = {
    "https://cloud.google.com/feeds/google-cloud-security-bulletins.xml": {
        "date": "updated",
        "title": "title",
        "link": "link",
        "description": "content",
        "extra_details": None,
        "content_parse": True  # Indicates that the content needs to be parsed for CVE details
    },
    "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json": {
        "date": "dateAdded",
        "title": "vulnerabilityName",
        "link": None,  # No link tag in this feed
        "description": "shortDescription",
        "extra_details": ["requiredAction", "knownRansomwareCampaignUse", "notes"],
        "cve_id_tag": "cveID",  # Tag for CVE ID
        "content_parse": False
    }
}