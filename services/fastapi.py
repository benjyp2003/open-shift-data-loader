from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .dal import Dal

app = FastAPI()

# Initialize DAL instance
dal = Dal()

class QueryRequest(BaseModel):
    query: str

@app.post("/input_query")
async def input_query(request: QueryRequest):
    """
    Endpoint to process a query and return a response.
    """
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        # Use DAL to execute the query
        cursor = dal.execute(request.query, commit=False, dictionary=True)

        results = dal.fetch_all(request.query)
        response = {
            "query": request.query,
            "response": "Query executed successfully",
            "results": results
        }

        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify DAL connection.
    """
    try:
        # Test DAL connection
        dal.get_connection()
        return {"status": "healthy", "message": "Database connection successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
