import uvicorn
import os

if __name__ == "__main__":
    # For development
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,  # Changed port to avoid conflicts
        reload=True,
        workers=1
    )