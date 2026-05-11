# Skepti Scan

A RAG-based fact-checking API built with FastAPI to verify claims against external sources.

## Requirements

- Python 3.14 or later

#### Install python using Miniconda:

1) Download and install Miniconda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
2) Create a new environment using the following command:
```bash
$ conda create -n skepti-app python=3.14
```
3) Activate the environment:
```bash
$ conda activate skepti-app
```

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

### Run the Host API

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.
