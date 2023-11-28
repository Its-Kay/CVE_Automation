### Purpose

This script is to automate searching through a series of CVE RSS feeds for potential vulnerabilities.
The script will check against a series of keywords; these keywords can include packages or frameworks used in your
projects, and check if those matched CVE's are above a certain severity threshold.
These CVE's will be written to a Markdown file and provide enough context as to why they are included plus provide enough
data to persue checking those CVE's.
The output will also document how many CVE's have been checked and how many need to be followed up with later (ergo, how many CVE's met the threshold).


### Configure

To configure the script to parse disparate RSS feeds, all with their own tags, etc. the script has a configuration dictionary. 
This dictionary will map RSS tags to kwargs which are used to write to the Markdown file.
To add a new RSS feed to be consumed, or to modify an existing one, go to `configurations/__init__.py` and update the `feed_configs` dictionary.

### Run

```bash
$ python main.py
```

#### Output
CVEs which are should be reviewed are exported to Markdown and written to a directory named by month.
The directory will be named after the month of when the CVEs were published.
The MD file will be named after date when the script was run.


### Tests

Run tests using pytest:

```bash
$ pytest
```

Run with coverage:

```bash
$ pytest --cov=app
```
or, with more detail, run coverage to generate a HTML file:

```bash
$ pytest --cov=app --cov-report html
```
