#!/usr/bin/env python
# coding: utf-8

# In[2]:


from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import END, StateGraph, MessagesState
from IPython.display import Image, display
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pinecone import Pinecone
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException


# In[3]:


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")


# In[4]:


model = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

# get the search results from the vector db
def get_results_from_vector_db(query: str, k: int = 1):
    embeddings = OpenAIEmbeddings(api_key=openai_api_key)
    index_name = "wiki-index"
    query_vector = embeddings.embed_query(query)
    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index(index_name)
    response = index.query(vector=query_vector, top_k=k, include_metadata=True, include_values=True)
    return response

# rag agent
def rag_agent(state: MessagesState):
    # get the user message as the query
    user_query = state['messages'][-1].content

    # fetch the result
    search_results = get_results_from_vector_db(query=user_query, k=1)

    ## the retriever ##
    # Process the retrieved results
    if not search_results.get("matches"):  # Handle empty results
        context = "No relevant documents were retrieved."
    else:
        # Extract the top results from the Pinecone response
        retrieved_docs = []
        for doc in search_results["matches"]:
            # Each document has a similarity score by default
            doc_text = f"Type: ID: {doc['id']}, Score: {doc['score']:.4f}, Content: {doc['metadata']['text']}"
            retrieved_docs.append(doc_text)
        
        context = "\n".join(retrieved_docs)

    # defining the prompt
    prompt = f"""
    Answer strictly based on the provided documents. If no relevant documents are retrieved,
    respond with: "I do not have enough information to answer this question.":
    Context: {context}

    Question: {user_query}
    Answer:
    """

    # generating the response using the LLM
    response = model(prompt)

    # update the state using the response
    state.update({"messages":AIMessage(content=response.content)})
    return state

workflow = StateGraph(MessagesState)
workflow.add_node("rag_agent", rag_agent)
workflow.set_entry_point("rag_agent")
workflow.add_edge("rag_agent", END)

graph = workflow.compile()

display(Image(graph.get_graph().draw_mermaid_png()))

def get_response_from_graph(user_query):
    """Generates a response based on user input."""
    try:
        # Create dynamic HumanMessage
        messages = [HumanMessage(content=user_query)]

        # Input dictionary for Langchain execution
        initial_input = {"messages": messages}
        thread = {"configurable": {"thread_id": "201"}}

        # Run the LangChain graph until the first interruption
        response_message = None
        for event in graph.stream(initial_input, thread, stream_mode="values"):
            response_message = event['messages'][-1].content  # Extracting the latest response

        # Return the generated message
        if response_message:
            return {"result": response_message}
        else:
            raise HTTPException(status_code=500, detail="No response generated from LangChain.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

