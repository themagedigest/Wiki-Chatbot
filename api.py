from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from wiki_graph import get_response_from_graph

app = FastAPI()

# Define request model
class QueryRequest(BaseModel):
    user_query: str

@app.post("/wiki_search/")
async def generate_message(request: QueryRequest):
    try:
        # Call the function from wiki_graph.py
        response = get_response_from_graph(request.user_query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
