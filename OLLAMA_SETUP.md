# Ollama and Gemma Setup Instructions

This document provides instructions on how to install Ollama and download the Gemma model for use with this project.

## 1. Install Ollama

Follow the official Ollama installation instructions for your operating system:

- **Linux & macOS:** Visit [https://ollama.com](https://ollama.com) and follow the download and installation steps. Typically, this involves a command like:
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```
- **Windows:** Download the Windows installer from [https://ollama.com](https://ollama.com) and run it.

Verify the installation by opening a terminal or command prompt and running:
```bash
ollama --version
```

## 2. Download the Gemma Model

Once Ollama is installed and running, you need to download the Gemma model. We are using `gemma:12b-it-qat` for this project, but you can choose other variants if needed.

Open your terminal or command prompt and run:
```bash
ollama pull gemma:12b-it-qat
```
This command will download the specified Gemma model. The download size can be significant, so ensure you have a stable internet connection and sufficient disk space.

## 3. Ensure Ollama is Serving Models

By default, Ollama runs a server in the background. You can check its status or start it manually if needed.

To serve models (if not already running):
```bash
ollama serve
```
This command usually isn't necessary as Ollama typically starts automatically after installation and when you pull a model.

## 4. (Optional) Verify Model Availability

You can list the models Ollama has downloaded by running:
```bash
ollama list
```
You should see `gemma:12b-it-qat` in the list.

## Next Steps

Once Ollama is installed and the Gemma model is downloaded and available, the application will be able to connect to Ollama (usually at `http://localhost:11434`) to use the model for AI processing tasks.
