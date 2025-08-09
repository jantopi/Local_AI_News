import streamlit as st
import sys
import os
import feedparser # Import the missing library

# Add project root to Python path to allow importing from news_fetcher and ai_processor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from news_fetcher.fetcher import fetch_news_from_rss
from ai_processor.processor import summarize_text, get_available_models

# --- App Configuration ---
MAX_ARTICLES_TO_DISPLAY = 20
SUMMARIZE_ARTICLES_DEFAULT = True
DEFAULT_PROMPT = "Summarize the following news article in 2-3 concise sentences, capturing the main point."

# --- Caching Configuration ---
CACHE_TTL_SECONDS = 600  # 10 minutes for news and models

# --- Cached Data Fetching Functions ---
@st.cache_data(ttl=CACHE_TTL_SECONDS)
def cached_fetch_news(feed_urls):
    """Cached function to fetch news from RSS feeds."""
    st.toast(f"Fetching news from {len(feed_urls)} sources...", icon="📰")
    return fetch_news_from_rss(feed_urls)

@st.cache_data(ttl=CACHE_TTL_SECONDS)
def cached_get_models():
    """Cached function to get available Ollama models."""
    return get_available_models()

@st.cache_data(ttl=CACHE_TTL_SECONDS * 6) # Cache summaries for an hour
def cached_summarize_text(text, model, prompt):
    """Cached function to generate AI summary."""
    if not text or len(text) < 100: # Don't summarize very short texts
        return None
    return summarize_text(text, model, prompt)

# --- Predefined News Sources ---
PREDEFINED_NEWS_SOURCES = {
    "CNN Top Stories": "http://rss.cnn.com/rss/cnn_topstories.rss",
    "BBC News": "http://feeds.bbci.co.uk/news/rss.xml",
    "Reuters Top News": "http://feeds.reuters.com/reuters/topNews",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "WIRED": "https://www.wired.com/feed/rss",
    "Ars Technica": "http://feeds.arstechnica.com/arstechnica/index",
}

# --- UI Helper Functions ---
def display_article(article, index, summarize=False, selected_model="default", summarization_prompt=""):
    """Displays a single article in a card-like format."""
    st.subheader(article.get('title', 'No Title'))

    # Metadata and link button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.caption(f"Published: {article.get('published_date', 'N/A')}")
    with col2:
        st.link_button("Read Full Article ↗️", article.get('link', '#'), use_container_width=True)

    # Summarization section
    if summarize:
        if 'summary_ai' in article:
            if article['summary_ai']:
                with st.expander("🤖 AI Summary", expanded=True):
                    st.markdown(article['summary_ai'])
                with st.expander("📄 Original Summary"):
                    st.markdown(article.get('summary', '_No original summary available._'))
            else:
                # This indicates summarization was attempted but failed (e.g., short text)
                with st.expander("📄 Original Summary", expanded=True):
                    st.markdown(article.get('summary', '_No original summary available._'))
                st.info("Article not summarized by AI (e.g., content too short).", icon="ℹ️")
        else:
            # This case happens if summarization is enabled but hasn't been run for this article yet
            st.info("AI summary is being generated...", icon="⏳")
    else:
        # If summarization is disabled, just show the original summary
        with st.expander("📄 Summary/Description", expanded=True):
            st.markdown(article.get('summary', '_No summary available._'))

# --- Main Application ---
def main():
    st.set_page_config(page_title="IntelliNews 2.0", layout="wide", initial_sidebar_state="expanded")

    # --- Sidebar ---
    st.sidebar.title("IntelliNews 2.0 🚀")
    st.sidebar.markdown("Your AI-powered news digest.")

    st.sidebar.header("📰 News Sources")

    # Initialize session state for feeds
    if 'selected_sources' not in st.session_state:
        st.session_state.selected_sources = list(PREDEFINED_NEWS_SOURCES.keys())[:3] # Default to first 3
    if 'custom_feeds' not in st.session_state:
        st.session_state.custom_feeds = []

    # Predefined sources multiselect
    st.session_state.selected_sources = st.sidebar.multiselect(
        "Choose from predefined sources:",
        options=list(PREDEFINED_NEWS_SOURCES.keys()),
        default=st.session_state.selected_sources,
        key="predefined_sources_multiselect"
    )

    # Custom RSS feed management
    st.sidebar.markdown("---")
    custom_feed_input = st.sidebar.text_input("Add a custom RSS feed URL:")
    if st.sidebar.button("Add Custom Feed") and custom_feed_input:
        if custom_feed_input not in st.session_state.custom_feeds:
            st.session_state.custom_feeds.append(custom_feed_input)
            st.sidebar.success("Custom feed added!")
        else:
            st.sidebar.warning("Custom feed already in list.")

    # Combine selected and custom feeds
    active_feeds = [PREDEFINED_NEWS_SOURCES[name] for name in st.session_state.selected_sources]
    active_feeds.extend(st.session_state.custom_feeds)

    # Display current custom feeds with a remove button
    for feed in st.session_state.custom_feeds[:]: # Iterate over a copy
        col1, col2 = st.sidebar.columns([4, 1])
        col1.caption(feed, help=feed)
        if col2.button("✖", key=f"remove_{feed}", help=f"Remove {feed}"):
            st.session_state.custom_feeds.remove(feed)
            st.rerun()

    st.sidebar.header("🤖 AI Settings")

    # AI Summarization Toggle
    summarize_enabled = st.sidebar.toggle(
        "Enable AI Summaries",
        value=SUMMARIZE_ARTICLES_DEFAULT,
        key="summarize_toggle"
    )

    if summarize_enabled:
        available_models = cached_get_models()
        if not available_models:
            st.sidebar.error("Ollama not detected or no models found. Please ensure Ollama is running.")
            st.session_state.selected_model = None
        else:
            # Model selection
            st.session_state.selected_model = st.sidebar.selectbox(
                "Choose an AI model:",
                options=available_models,
                index=available_models.index(st.session_state.get('selected_model', available_models[0])) if st.session_state.get('selected_model') in available_models else 0,
                key="model_selectbox"
            )

        # Custom prompt
        st.session_state.summarization_prompt = st.sidebar.text_area(
            "Custom summarization prompt:",
            value=st.session_state.get('summarization_prompt', DEFAULT_PROMPT),
            height=150,
            key="prompt_textarea"
        )

    # --- Main Page ---
    st.title("IntelliNews Digest")
    st.markdown("---")

    if not active_feeds:
        st.warning("No news sources selected. Please choose some sources from the sidebar.")
        return

    # Fetch and display news
    # Convert list to tuple for caching
    feed_tuple = tuple(active_feeds)
    articles = cached_fetch_news(feed_tuple)

    if not articles:
        st.error("No articles found from the configured sources. Check the URLs or try again later.")
        return

    # Sort articles by published date (best effort)
    try:
        articles.sort(key=lambda x: feedparser._parse_date(x.get('published_date')), reverse=True)
    except Exception:
        st.caption("Note: Could not reliably sort all articles by date.")

    st.info(f"Fetched {len(articles)} articles. Displaying the latest {min(len(articles), MAX_ARTICLES_TO_DISPLAY)}.")

    selected_model = st.session_state.get('selected_model')
    summarization_prompt = st.session_state.get('summarization_prompt', DEFAULT_PROMPT)

    # --- Tabbed Article Display ---

    # Create a reverse mapping from URL to source name for display
    url_to_source_name = {v: k for k, v in PREDEFINED_NEWS_SOURCES.items()}

    # Group articles by source
    articles_by_source = {}
    for article in articles:
        source_url = article['source_url']
        if source_url not in articles_by_source:
            articles_by_source[source_url] = []
        articles_by_source[source_url].append(article)

    # Create tabs for each source
    source_urls_with_articles = [url for url in active_feeds if url in articles_by_source]

    if not source_urls_with_articles:
        st.info("No articles found for the selected sources at the moment.")
        return

    tab_titles = [url_to_source_name.get(url, url) for url in source_urls_with_articles]
    tabs = st.tabs(tab_titles)

    for i, tab in enumerate(tabs):
        with tab:
            source_url = source_urls_with_articles[i]
            source_articles = articles_by_source[source_url]
            st.header(f"Latest from {url_to_source_name.get(source_url, source_url)}")

            for j, article_data in enumerate(source_articles[:MAX_ARTICLES_TO_DISPLAY]):
                if summarize_enabled and selected_model:
                    text_to_summarize = article_data.get('summary', article_data.get('title', ''))
                    ai_summary = cached_summarize_text(
                        text=text_to_summarize,
                        model=selected_model,
                        prompt=summarization_prompt
                    )
                    article_data['summary_ai'] = ai_summary

                # Using a container for a "card" like effect
                with st.container(border=True):
                    display_article(
                        article_data,
                        j, # Use j for index within the tab
                        summarize=summarize_enabled,
                        selected_model=selected_model,
                        summarization_prompt=summarization_prompt
                    )

    st.sidebar.markdown("---")
    st.sidebar.info("Developed for IntelliNews 2.0")

if __name__ == "__main__":
    main()
