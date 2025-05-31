```markdown
# IntelliNews Local - AI-Powered News Aggregator

IntelliNews Local is a Python application that fetches news articles from RSS feeds, uses a local AI model (Ollama with Gemma) to generate summaries, and displays them in a web interface built with Streamlit.

## Features

-   Fetches news from configurable RSS feeds.
-   Utilizes Ollama and a Gemma model (e.g., `gemma:12b-it-qat`) for AI-powered text summarization.
-   Interactive web UI using Streamlit to display news and summaries.
-   Allows adding and removing RSS feed sources directly from the UI.
-   Toggle AI summarization on or off.
-   Basic unit tests for core components.

## Project Structure

```
.
├── ai_processor/
│   ├── __init__.py
│   └── processor.py      # Handles AI summarization via Ollama
├── news_fetcher/
│   ├── __init__.py
│   └── fetcher.py        # Fetches and parses RSS feeds
├── tests/
│   ├── __init__.py
│   ├── test_ai_processor.py # Unit tests for AI processor
│   └── test_fetcher.py   # Unit tests for news fetcher
├── ui/
│   ├── __init__.py
│   └── app.py            # Streamlit web application
├── OLLAMA_SETUP.md       # Instructions for setting up Ollama and Gemma model
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Prerequisites

1.  **Python 3.8+**: Ensure you have Python installed.
2.  **Ollama and Gemma Model**: You need to have Ollama installed and the desired Gemma model downloaded.
    -   Follow the instructions in [OLLAMA_SETUP.md](./OLLAMA_SETUP.md) to install Ollama and pull the `gemma:12b-it-qat` model (or another Gemma variant if you prefer, but you'll need to update `DEFAULT_MODEL` in `ai_processor/processor.py` and potentially `ui/app.py`).

## Setup and Installation

1.  **Clone the repository (if applicable):**
    ```bash
    # git clone <repository_url>
    # cd <repository_directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Ensure Ollama is running and serving the model.**
    -   You can typically start Ollama by running `ollama serve` in a separate terminal if it's not already running in the background.
    -   Verify the model is available: `ollama list` (should show `gemma:12b-it-qat` or your chosen model).

2.  **Run the Streamlit application:**
    Navigate to the project's root directory and execute:
    ```bash
    streamlit run ui/app.py
    ```
    This will start the web server, and your default web browser should open to the application's URL (usually `http://localhost:8501`).

## Running Tests

To run the unit tests, ensure `pytest` is installed (it's in `requirements.txt`).
Navigate to the project's root directory and run:

```bash
python -m pytest
```
or simply:
```bash
pytest
```

## How It Works

1.  **News Fetching**: The `news_fetcher.fetcher` module uses the `feedparser` library to retrieve articles from the RSS feed URLs specified in the Streamlit UI.
2.  **AI Summarization**: If AI summaries are enabled in the UI, the `ai_processor.processor` module sends the content of each article (usually the original summary or description) to the locally running Ollama API. The Gemma model generates a concise summary.
3.  **User Interface**: The `ui.app` (Streamlit application) provides controls to manage RSS feeds, toggle AI summarization, and displays the fetched articles along with their AI-generated summaries (if available).

## Customization

-   **RSS Feeds**: You can add or remove RSS feeds directly in the web UI. The initial list of feeds is defined in `ui/app.py` (`DEFAULT_RSS_FEEDS`).
-   **AI Model**: The default AI model is `gemma:12b-it-qat`. You can change this in `ai_processor/processor.py` (variable `DEFAULT_MODEL`). Ensure the chosen model is downloaded via Ollama.
-   **Summarization Prompt**: The prompt used for summarization can be adjusted in `ai_processor/processor.py` within the `summarize_text` function.

## Contributing

Feel free to fork this project, make improvements, and submit pull requests. If you encounter issues or have suggestions, please open an issue in the repository.
```
