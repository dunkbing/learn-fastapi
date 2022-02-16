import uvicorn

if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(levelname)s - %(message)s"
    uvicorn.run("api.main:app", host="0.0.0.0", port=8080,
                reload=True, log_level="info", log_config=log_config)
