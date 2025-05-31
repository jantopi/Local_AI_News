```python
import streamlit as st
import sys
import os

# Add project root to Python path to allow importing from news_fetcher and ai_processor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from news_fetcher.fetcher import fetch_news_from_rss
from ai_processor.processor import summarize_text

# --- Configuration ---
DEFAULT_RSS_FEEDS = [
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://feeds.bbci.co.uk/news/rss.xml",
    "http://feeds.reuters.com/reuters/topNews",
    "https://www.aljazeera.com/xml/rss/all.xml",
    # "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en" # Google News RSS, often requires consent/cookie handling
]
MAX_ARTICLES_TO_DISPLAY = 20
SUMMARIZE_ARTICLES_DEFAULT = True # Whether to attempt summarization by default

# --- Helper Functions ---
def display_article(article, index, summarize=False):
    """Displays a single article in the Streamlit app."""
    st.subheader(f"{index + 1}. {article.get('title', 'No Title')}")

    col1, col2 = st.columns([3,1])
    with col1:
        st.caption(f"Published: {article.get('published_date', 'N/A')} | Source: {article.get('source_url', 'N/A')}")
    with col2:
        st.link_button("Read Full Article", article.get('link', '#'), use_container_width=True)

    if summarize and 'summary_ai' in article and article['summary_ai']:
        with st.expander("AI Summary", expanded=False):
            st.markdown(article['summary_ai'])
        with st.expander("Original Summary/Description", expanded=False):
            st.markdown(article.get('summary', 'No original summary available.'))
    elif 'summary' in article and article['summary']:
        with st.expander("Summary/Description", expanded=True):
            st.markdown(article.get('summary'))
    else:
        st.markdown("_No summary available for this article._")

    st.divider()

# --- Main Application ---
def main():
    st.set_page_config(page_title="IntelliNews Local", layout="wide", initial_sidebar_state="expanded")

    st.sidebar.title("IntelliNews Settings")
    st.sidebar.markdown("Configure your news feed.")

    # RSS Feed Management
    st.sidebar.subheader("News Sources (RSS Feeds)")
    if 'rss_feeds' not in st.session_state:
        st.session_state.rss_feeds = DEFAULT_RSS_FEEDS[:] # Use a copy

    new_feed = st.sidebar.text_input("Add RSS Feed URL:", key="new_feed_input")
    if st.sidebar.button("Add Feed", key="add_feed_button") and new_feed:
        if new_feed not in st.session_state.rss_feeds:
            st.session_state.rss_feeds.append(new_feed)
            st.sidebar.success(f"Added feed: {new_feed}")
        else:
            st.sidebar.warning("Feed already exists.")
        # Clear input by re-assigning a new key or using st.empty() for more complex scenarios
        # For simplicity here, we rely on Streamlit's rerun behavior.

    # Display and allow removal of feeds
    feeds_to_remove = []
    for feed_url in st.session_state.rss_feeds:
        col1, col2 = st.sidebar.columns([4,1])
        col1.caption(feed_url, help=feed_url)
        if col2.button("X", key=f"remove_{feed_url}", help=f"Remove {feed_url}"):
            feeds_to_remove.append(feed_url)

    if feeds_to_remove:
        for feed_url in feeds_to_remove:
            st.session_state.rss_feeds.remove(feed_url)
        st.rerun() # Rerun to update the list immediately

    # AI Settings
    st.sidebar.subheader("AI Processing")
    summarize_enabled = st.sidebar.checkbox("Enable AI Summaries", value=SUMMARIZE_ARTICLES_DEFAULT, key="summarize_toggle")

    # --- Page Title ---
    st.title("IntelliNews Local Digest 📰")
    st.markdown("Your local news feed, powered by AI.")
    st.markdown("---")

    # --- Fetch and Display News ---
    if not st.session_state.rss_feeds:
        st.warning("No RSS feeds configured. Please add some feeds in the sidebar to see news.")
        return

    with st.spinner("Fetching news articles..."):
        articles = fetch_news_from_rss(st.session_state.rss_feeds)

    if not articles:
        st.error("No articles found from the configured RSS feeds. Check the URLs or try different feeds.")
        return

    st.info(f"Fetched {len(articles)} articles. Displaying the latest {min(len(articles), MAX_ARTICLES_TO_DISPLAY)}.")

    processed_articles = []
    if articles:
        # Sort articles by published date if possible (best effort)
        # Note: feedparser tries to normalize dates, but quality varies.
        try:
            articles.sort(key=lambda x: feedparser._parse_date(x.get('published_date')), reverse=True)
        except Exception:
            st.caption("Note: Could not reliably sort all articles by date.")


        for i, article_data in enumerate(articles[:MAX_ARTICLES_TO_DISPLAY]):
            if summarize_enabled:
                with st.spinner(f"Generating AI summary for article {i+1}/{min(len(articles), MAX_ARTICLES_TO_DISPLAY)}..."):
                    # Use the original summary/description as input for AI summarization if available
                    text_to_summarize = article_data.get('summary', article_data.get('title', ''))
                    if text_to_summarize and len(text_to_summarize) > 50: # Only summarize if there's enough content
                        ai_summary = summarize_text(text_to_summarize)
                        article_data['summary_ai'] = ai_summary
                    else:
                        article_data['summary_ai'] = None # Not enough content or no content to summarize
            processed_articles.append(article_data)
            display_article(article_data, i, summarize=summarize_enabled)

    st.sidebar.markdown("---")
    st.sidebar.markdown("Developed with Ollama & Gemma.")

if __name__ == "__main__":
    main()

```
