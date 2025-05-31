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

1.  **Python 3.8+**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/).
2.  **Ollama and Gemma Model**: You need to have Ollama installed and the desired Gemma model downloaded.
    -   Follow the instructions in [OLLAMA_SETUP.md](./OLLAMA_SETUP.md) to install Ollama and pull the `gemma:12b-it-qat` model.
    -   If you prefer another Gemma variant, you'll need to update `DEFAULT_MODEL` in `ai_processor/processor.py`.

## Setup and Installation

### 1. Download the Project

To get started, you'll need to download the project files to your local machine. The recommended way to do this is by using Git.

**Prerequisite: Install Git**
If you don't have Git installed, download and install it from [git-scm.com](https://git-scm.com/). Git is a version control system that helps manage and track changes to code.

**Cloning the Repository**
Open your command line interface (like Terminal on macOS/Linux, or Command Prompt/PowerShell/Git Bash on Windows). Navigate to the directory where you want to store the project. Then, run the following command:

```bash
git clone <repository_url>
```
Replace `<repository_url>` with the actual URL of this project's repository. This command will create a new folder named after the repository, containing all the project files.

Navigate into the newly created project directory:
```bash
cd <repository_directory_name>
```
Replace `<repository_directory_name>` with the name of the folder created by `git clone` (e.g., `IntelliNews-Local`).

### 2. Create a Virtual Environment (Recommended)

A virtual environment isolates your project's dependencies from other Python projects.

In the project's root directory (`<repository_directory_name>`), run:
```bash
python -m venv venv
```
This creates a `venv` folder. To activate it:

-   **macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```
-   **Windows:**
    ```bash
    venv\Scripts\activate
    ```
You should see `(venv)` prefixed to your terminal prompt.

### 3. Install Dependencies

With the virtual environment activated, install the required Python packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1.  **Ensure Ollama is Running and Serving the Model.**
    -   Ollama typically runs as a background service after installation.
    -   If you need to start it manually (less common), you might use a command like `ollama serve` in a separate terminal.
    -   Verify the model is available by running:
        ```bash
        ollama list
        ```
        You should see `gemma:12b-it-qat` (or your chosen model) in the output. If not, pull it using `ollama pull gemma:12b-it-qat`.

2.  **Run the Streamlit Application.**
    Navigate to the project's root directory in your terminal (if you're not already there and your virtual environment is active). Execute:
    ```bash
    streamlit run ui/app.py
    ```
    This will start the web server. Your default web browser should open to the application's URL (usually `http://localhost:8501`).

## Running Tests

To run the unit tests, ensure `pytest` is installed (it's included in `requirements.txt`).

Navigate to the project's root directory and run:
```bash
python -m pytest
```
or simply:
```bash
pytest
```
This will discover and run all tests in the `tests` directory.

## How It Works

1.  **News Fetching**: The `news_fetcher.fetcher` module uses the `feedparser` library to retrieve articles from the RSS feed URLs specified in the Streamlit UI.
2.  **AI Summarization**: If AI summaries are enabled in the UI, the `ai_processor.processor` module sends the content of each article (usually the original summary or description found in the RSS feed) to the locally running Ollama API. The Gemma model then generates a concise summary.
3.  **User Interface**: The `ui/app.py` script, using Streamlit, provides an interactive web interface. Users can manage RSS feeds, toggle AI summarization, and view the fetched articles along with their AI-generated summaries (if available).

## Customization

-   **RSS Feeds**:
    -   Add or remove RSS feeds directly in the web UI's sidebar.
    -   The initial default list of feeds is defined in `ui/app.py` (look for the `DEFAULT_RSS_FEEDS` variable).
-   **AI Model**:
    -   The default AI model is `gemma:12b-it-qat`. This can be changed by modifying the `DEFAULT_MODEL` variable in `ai_processor/processor.py`.
    -   Ensure any model you specify is downloaded via Ollama (`ollama pull <your_model_name>`).
-   **Summarization Prompt**:
    -   The prompt sent to the AI for summarization can be adjusted in `ai_processor/processor.py` within the `summarize_text` function (the `prompt` variable).

## Contributing

Contributions are welcome! Feel free to fork this project, make improvements, and submit pull requests. If you encounter issues or have suggestions for new features, please open an issue in the repository.
