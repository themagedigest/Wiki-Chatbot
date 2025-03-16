Wikipedia Chatbot using LangChain, FastAPI, and OpenAI
Project Overview
This project is an AI-powered Wikipedia Chatbot that allows users to ask natural language questions and receive intelligent answers. The chatbot is built using LangChain for query orchestration, Pinecone as a vector database for semantic search, OpenAI’s GPT model as the language model, FastAPI for backend integration, and Streamlit for an interactive UI.

Tech Stack & Workflow
1️⃣ LangChain for Graph Orchestration

Handles the logic for processing user queries and retrieving relevant Wikipedia information.
Uses retrieval-augmented generation (RAG) to improve responses by combining vector search with LLM capabilities.
2️⃣ Pinecone as the Vector Database

Stores Wikipedia embeddings for fast and efficient similarity search.
Enables semantic search to fetch relevant documents based on query meaning rather than exact words.
3️⃣ OpenAI GPT for Answer Generation

Uses OpenAI’s LLM to generate human-like responses based on the retrieved Wikipedia content.
Enhances answers by rephrasing and structuring the information for clarity.
4️⃣ FastAPI for Backend Integration

Provides a lightweight, high-performance REST API to handle user queries.
Exposes a /wiki_search/ endpoint to process user questions and return intelligent responses.
5️⃣ Streamlit for Chatbot UI

Creates an interactive chat-based UI where users can type questions and receive instant responses.
Maintains a conversation history for better user experience.
How It Works
🔹 User enters a question in the chatbot UI.
🔹 FastAPI sends the query to LangChain for processing.
🔹 Pinecone searches for the most relevant Wikipedia passages.
🔹 OpenAI LLM refines the response using the retrieved information.
🔹 Streamlit displays the answer in an intuitive chat format.

Key Features
✅ Fast & Accurate – Combines vector search with LLM intelligence.
✅ Conversational UI – Uses Streamlit for an engaging chatbot experience.
✅ Scalable Architecture – Built with modular components (FastAPI, Pinecone, OpenAI, LangChain).
✅ Real-time Responses – Ensures low latency for quick query resolution.
