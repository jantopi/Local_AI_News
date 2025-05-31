```python
import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "gemma:12b-it-qat" # As specified in the setup instructions

def summarize_text(text: str, model: str = DEFAULT_MODEL, ollama_url: str = OLLAMA_API_URL) -> str | None:
    """
    Summarizes the given text using the specified Ollama model.

    Args:
        text: The text to summarize.
        model: The Ollama model to use (e.g., 'gemma:12b-it-qat').
        ollama_url: The URL of the Ollama API.

    Returns:
        The summarized text as a string, or None if an error occurs.
    """
    if not text or not isinstance(text, str):
        print("Error: Input text must be a non-empty string.")
        return None

    prompt = f"Summarize the following news article in 2-3 sentences: \n\n{text}"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False # Get the full response at once
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(ollama_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

        response_data = response.json()
        summary = response_data.get("response", "").strip()

        # Basic check if the summary is meaningful
        if not summary or len(summary) < 10: # Arbitrary minimum length for a summary
            print(f"Warning: Received a very short or empty summary from model {model} for text: {text[:100]}...")
            return None

        return summary
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama API at {ollama_url}: {e}")
        print("Please ensure Ollama is running and the model is available. See OLLAMA_SETUP.md.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON response from Ollama. Response: {response.text}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during AI processing: {e}")
        return None

if __name__ == '__main__':
    # Example Usage (requires Ollama server to be running with the model)
    sample_article_text = (
        "Tech Giant Alpha today announced the release of its groundbreaking new Quantum Leap processor, "
        "promising to revolutionize computing speeds and capabilities. The processor, developed over a "
        "decade of research, utilizes qubits that can maintain coherence for significantly longer periods "
        "than previous designs. Alpha's CEO stated, 'This is not just an incremental improvement; it's a "
        "paradigm shift that will unlock new possibilities in fields like medicine, materials science, and "
        "artificial intelligence.' Early benchmarks show performance gains of over 1000x on specific quantum "
        "algorithms compared to classical supercomputers. However, experts caution that widespread adoption "
        "is still years away, citing challenges in manufacturing and software development. The company plans "
        "to offer cloud access to the Quantum Leap processor for researchers and enterprise clients by the end of the year."
    )

    print(f"Attempting to summarize article (model: {DEFAULT_MODEL}):")
    print("---")
    print(f"Original Text (first 200 chars): {sample_article_text[:200]}...")
    print("---")

    summary = summarize_text(sample_article_text)

    if summary:
        print("Summary:")
        print(summary)
    else:
        print("Failed to generate summary. Make sure Ollama is running and the model is pulled.")
        print("You can run 'ollama serve' and 'ollama pull gemma:12b-it-qat' in your terminal.")

    # Example of a text too short (or problematic)
    print("\n---")
    print("Attempting to summarize a very short text:")
    short_text = "Hello world."
    summary_short = summarize_text(short_text)
    if summary_short:
        print("Summary of short text:")
        print(summary_short)
    else:
        print("Failed to summarize short text as expected (or model provided no meaningful summary).")

```
