# Langchain Project

This project utilizes the Langchain library to index and query PDF documents using the OpenAI model. 
It allows for loading PDF documents, splitting them into chunks, generating embeddings using the OpenAI model, indexing these embeddings with FAISS, and answering user queries based on the indexed documents.

## Running Instructions

1. Clone this repository to your machine.
2. Install the required libraries using `pip install -r requirements.txt`.
3. Rename the `.env.template` file to `.env`.
4. In the `.env` file, fill in the `OPENAI_API_KEY` with the API key provided by OpenAI.
5. Run the main project script.

## Notes

- Ensure you have a valid API key from OpenAI.
- This project has been tested with Langchain version 0.0.312.

## Warning

- If the input document is too long, the chatbot may produce inaccurate or incomplete responses.

## Project Status

This project is actively being developed and will be continued in the future.
