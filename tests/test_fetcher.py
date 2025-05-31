import pytest
from news_fetcher.fetcher import fetch_news_from_rss
from unittest.mock import patch, MagicMock

# A sample feed entry structure that feedparser might return
SAMPLE_FEED_ENTRY = {
    'title': 'Test Title',
    'link': 'http://example.com/test',
    'summary': 'Test summary.',
    'published': 'Tue, 23 Jul 2024 10:00:00 +0000',
    'source_url': 'http://example.com/rss'
}

SAMPLE_PARSED_FEED = {
    'bozo': 0, # 0 means not malformed
    'entries': [SAMPLE_FEED_ENTRY],
    'feed': {},
    'headers': {}
}

MALFORMED_PARSED_FEED = {
    'bozo': 1, # 1 means malformed
    'entries': [], # Typically no entries if feed is malformed
    'feed': {},
    'headers': {}
}

def test_fetch_news_empty_list():
    """Test fetching news with an empty list of RSS feeds."""
    articles = fetch_news_from_rss([])
    assert articles == []

def test_fetch_news_invalid_input():
    """Test fetching news with invalid input (not a list)."""
    articles = fetch_news_from_rss("not_a_list")
    assert articles == [] # Expecting the function to handle this gracefully

@patch('feedparser.parse')
def test_fetch_news_successful_mocked(mock_parse):
    """Test fetching news from a single valid RSS feed using a mock."""
    mock_parse.return_value = SAMPLE_PARSED_FEED

    rss_feeds = ["http://example.com/rss"]
    articles = fetch_news_from_rss(rss_feeds)

    assert len(articles) == 1
    article = articles[0]
    assert article['title'] == SAMPLE_FEED_ENTRY['title']
    assert article['link'] == SAMPLE_FEED_ENTRY['link']
    assert article['summary'] == SAMPLE_FEED_ENTRY['summary']
    assert article['published_date'] == SAMPLE_FEED_ENTRY['published']
    assert article['source_url'] == rss_feeds[0]
    mock_parse.assert_called_once_with("http://example.com/rss")

@patch('feedparser.parse')
def test_fetch_news_multiple_feeds_mocked(mock_parse):
    """Test fetching news from multiple RSS feeds, one valid, one error."""
    # Configure side_effect to return different values for different calls
    # The first call will be successful, the second will simulate an exception
    mock_parse.side_effect = [
        SAMPLE_PARSED_FEED,
        Exception("Simulated RSS parsing error")
    ]

    rss_feeds = ["http://valid.example.com/rss", "http://error.example.com/rss"]
    articles = fetch_news_from_rss(rss_feeds)

    assert len(articles) == 1 # Only one article from the valid feed
    article = articles[0]
    assert article['title'] == SAMPLE_FEED_ENTRY['title']
    assert article['source_url'] == "http://valid.example.com/rss"

    assert mock_parse.call_count == 2
    mock_parse.assert_any_call("http://valid.example.com/rss")
    mock_parse.assert_any_call("http://error.example.com/rss")

@patch('feedparser.parse')
def test_fetch_news_malformed_feed_mocked(mock_parse):
    """Test fetching news from a malformed RSS feed using a mock."""
    mock_parse.return_value = MALFORMED_PARSED_FEED # feedparser indicates malformed

    rss_feeds = ["http://malformed.example.com/rss"]
    # Depending on how strictly feedparser handles 'bozo', it might still return entries.
    # The current implementation of fetch_news_from_rss doesn't check feed.bozo.
    # This test assumes it might still try to process entries if they exist, or return empty if not.
    # If MALFORMED_PARSED_FEED has no entries, articles will be empty.
    articles = fetch_news_from_rss(rss_feeds)
    assert len(articles) == 0 # No entries in MALFORMED_PARSED_FEED

@patch('feedparser.parse')
def test_fetch_news_entry_missing_fields(mock_parse):
    """Test when a feed entry is missing some fields."""
    incomplete_entry = {
        'link': 'http://example.com/incomplete',
        # 'title' is missing
        # 'summary' is missing
        # 'published' is missing
    }
    parsed_feed_incomplete = {
        'entries': [incomplete_entry],
        'feed': {},
        'headers': {}
    }
    mock_parse.return_value = parsed_feed_incomplete

    articles = fetch_news_from_rss(["http://incomplete.example.com/rss"])
    assert len(articles) == 1
    article = articles[0]
    assert article['title'] == 'N/A' # Default value
    assert article['link'] == 'http://example.com/incomplete'
    assert article['summary'] == 'N/A' # Default value
    assert article['published_date'] == 'N/A' # Default value

# To run these tests, navigate to the project root and run:
# python -m pytest
```
