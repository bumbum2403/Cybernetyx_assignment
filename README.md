# FastAPI ChromaDB Server
==========================

A lightweight FastAPI server utilizing ChromaDB's persistent client for ingesting and querying documents.


## Table of Contents
-----------------

1. [Overview](#overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API Endpoints](#api-endpoints)
7. [Contributing](#contributing)
8. [License](#license)


## Overview
--------

This FastAPI server provides non-blocking API endpoints for ingesting and querying documents using ChromaDB's persistent client. It leverages sentence-transformers/all-MiniLM-L6-v2 from Hugging Face for efficient embeddings.


## Features
--------

*   Support for PDF, DOC, DOCX, and TXT document formats
*   Non-blocking API endpoints using asyncio
*   Efficient concurrency handling
*   ChromaDB persistent client for document ingestion and querying
*   sentence-transformers/all-MiniLM-L6-v2 for embeddings


## Requirements
------------

*   Python 3.12+
*   FastAPI
*   ChromaDB
*   sentence-transformers
*   Hugging Face Transformers


## Installation
------------

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn app.main:app --reload
