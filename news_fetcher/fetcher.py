```python
import feedparser

def fetch_news_from_rss(rss_feed_urls: list[str]) -> list[dict]:
    """
    Fetches news articles from a list of RSS feed URLs.

    Args:
        rss_feed_urls: A list of URLs for RSS feeds.

    Returns:
        A list of dictionaries, where each dictionary represents a news article
        and contains keys like 'title', 'link', 'summary', and 'published_date'.
        Returns an empty list if fetching fails or no articles are found.
    """
    articles = []
    if not isinstance(rss_feed_urls, list):
        print("Error: rss_feed_urls must be a list.")
        return articles

    for url in rss_feed_urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                article = {
                    'title': entry.get('title', 'N/A'),
                    'link': entry.get('link', '#'),
                    'summary': entry.get('summary', entry.get('description', 'N/A')), # Also check 'description'
                    'published_date': entry.get('published', entry.get('updated', 'N/A')), # Also check 'updated'
                    'source_url': url
                }
                articles.append(article)
        except Exception as e:
            print(f"Error fetching or parsing RSS feed {url}: {e}")
    return articles

if __name__ == '__main__':
    # Example usage:
    sample_rss_feeds = [
        "http://rss.cnn.com/rss/cnn_topstories.rss",  # CNN Top Stories
        "http://feeds.bbci.co.uk/news/rss.xml",       # BBC News
        # Add more RSS feeds here
    ]

    print(f"Fetching news from: {sample_rss_feeds}")
    news_articles = fetch_news_from_rss(sample_rss_feeds)

    if news_articles:
        print(f"Successfully fetched {len(news_articles)} articles.")
        for i, article in enumerate(news_articles[:3]): # Print details of first 3 articles
            print(f"\n--- Article {i+1} ---")
            print(f"Title: {article['title']}")
            print(f"Link: {article['link']}")
            print(f"Published Date: {article['published_date']}")
            print(f"Source: {article['source_url']}")
            print(f"Summary: {article['summary'][:200]}...") # Print first 200 chars of summary
    else:
        print("No articles fetched. Check URLs or network connection.")

```
