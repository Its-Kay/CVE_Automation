import pytest
import feedparser
from app.utils import is_actionable, clean_description
from typing import List, Dict, Tuple

actionable_keywords: List[str] = ["critical", "remote", "exploit", "linux"]


class TestIsActionable:
    @pytest.mark.parametrize("description, expected_actionable", [
        ("Critical vulnerability found", (True, ['critical'])),
        ("Minor issue, not a security problem", (False, [])),
        ("Lorem ipsum exploit, everything is on fire", (True, ['exploit'])),
        ("Linux ipsum dolar", (True, ['linux'])),
        ("Could be a problem", (False, [])),
        ("Insert Test Text Here", (False, []))
    ])
    def test_is_actionable(self, description: str, expected_actionable: Tuple[bool, List[str]]) -> None:
        assert is_actionable(description) == expected_actionable

    def test_is_actionable_with_actionable_description(self) -> None:
        description: str = "This is a critical issue affecting remote systems."
        actionable: bool
        keywords: List[str]
        actionable, keywords = is_actionable(description)
        assert actionable
        assert "critical" in keywords

    def test_is_actionable_with_non_actionable_description(self) -> None:
        description: str = "This string does not contain any actionable keywords."
        actionable, keywords = is_actionable(description)
        assert not actionable

    def test_is_actionable_with_description_list(self) -> None:
        description: List[str] = ["Linux problem", "Check this exploit", "This is not a problem"]
        actionable, keywords = is_actionable(description)
        assert actionable

    def test_is_actionable_with_list_of_feed_parser_dict(self) -> None:
        feedparser_dict1: feedparser.FeedParserDict = feedparser.FeedParserDict(value="This is a critical issue.")
        feedparser_dict2: feedparser.FeedParserDict = feedparser.FeedParserDict(value="This affects remote systems.")
        description: List[feedparser.FeedParserDict] = [feedparser_dict1, feedparser_dict2]
        actionable, keywords = is_actionable(description)
        assert actionable
        assert "critical" in keywords
        assert "remote" in keywords


class TestCleanDescription:
    def test_clean_description_with_html_string(self) -> None:
        html_description: str = "<p>This is <strong>important</strong> text.</p>"
        cleaned: str = clean_description(html_description)
        assert cleaned == "This is important text."

    def test_clean_description_with_list(self) -> None:
        list_description: List[str] = ["Part1", "<p>Part2</p>"]
        cleaned: str = clean_description(list_description)
        assert cleaned == "Part1 Part2"

    def test_clean_description_with_dictionary(self) -> None:
        dict_description: Dict[str, str] = {"value": "<div>Some <a href='http://example.com'>link</a></div>"}
        cleaned: str = clean_description(dict_description)
        assert cleaned == "Some link"

    def test_clean_description_with_whitespace(self) -> None:
        spaced_description: str = "This   is   spaced\nout  \t text."
        cleaned: str = clean_description(spaced_description)
        assert cleaned == "This is spaced out text."

    def test_clean_description_with_backslash_new_lines(self) -> None:
        spaced_description: str = "This   is   some looong text so we fall onto the next\n \t paragraph.\n\n"
        cleaned: str = clean_description(spaced_description)
        assert cleaned == "This is some looong text so we fall onto the next paragraph."
