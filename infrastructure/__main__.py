if __name__ == "__main__":
    import uvicorn
    import os

    is_debug = os.getenv("DEBUG") == "True"

    uvicorn.run(
        "infrastructure.run:app", host="0.0.0.0", port=5000, debug=is_debug, access_log=True, reload=is_debug,
    )
