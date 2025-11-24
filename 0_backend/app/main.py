from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.routers import campus_info, student_record
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("BE_PORT", 8000))
CE_APP = str(os.environ.get("CE_APP", ""))
CE_SUBDOMAIN = str(os.environ.get("CE_SUBDOMAIN", ""))
CE_DOMAIN = str(os.environ.get("CE_DOMAIN", ""))

app = FastAPI(title="University Assistant Backend")

app.include_router(campus_info.router, prefix="/campus", tags=["Campus Info"])
app.include_router(student_record.router, prefix="/student", tags=["Student Record"])

@app.get("/health")
def health():
    return {"status": "ok"}

def custom_openapi() -> Dict[str, Any]:
    """Generate a customized OpenAPI schema for the FastAPI application.

    This function creates and returns a customized OpenAPI schema that includes specific configurations:

    - It defines two server URLs, one with HTTP (unsecure) and one with HTTPS (secure).
    - The secure URL is dynamically set based on environment variables `CE_APP`, `CE_SUBDOMAIN`, and `CE_DOMAIN`.
    - Custom servers are defined to support both unsecure and secure environments.

    Additionally, the function ensures that anyOf, allOf, oneOf constructs in the OpenAPI schema are removed, which might be unnecessary or unsupported by some clients.

    Returns:
        Dict[str, Any]: The customized OpenAPI schema for the FastAPI application.
    """
    if app.openapi_schema:
        return app.openapi_schema

    custom_servers = [
        {
            "url": "http://{url}",
            "description": "Unsecure Server",
            "variables": {
                "url": {
                    "default": f"localhost:{PORT}",
                    "description": "The unsecure url of the backend",
                }
            },
        },
        {
            "url": "https://{url}",
            "description": "Secure Server",
            "variables": {
                "url": {
                    "default": f"{CE_APP}.{CE_SUBDOMAIN}.{CE_DOMAIN}",
                    "description": "The secure url of the backend",
                }
            },
        },
    ]

    if CE_APP != "":
        custom_servers.reverse()

    openapi_schema = get_openapi(
        openapi_version="3.0.2",
        title="rag-backend",
        version="1.0.0",
        description="RAG Backend",
        routes=app.routes,
        servers=custom_servers,
    )

    # Delete anyOf, allOf, oneOf which Assistant does not accept
    schemas = openapi_schema["components"]["schemas"]
    for schema in schemas:
        if "properties" in schemas[schema].keys():
            for property in schemas[schema]["properties"]:
                for key in ["anyOf", "allOf", "oneOf"]:
                    if key in schemas[schema]["properties"][property].keys():
                        del schemas[schema]["properties"][property][key]
                for item in schemas[schema]["properties"][property]:
                    if isinstance(schemas[schema]["properties"][property][item], dict):
                        for key in ["anyOf", "allOf", "oneOf"]:
                            if (
                                key
                                in schemas[schema]["properties"][property][item].keys()
                            ):
                                del schemas[schema]["properties"][property][item][key]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

