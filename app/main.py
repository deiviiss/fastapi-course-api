"""
This is a simple API example with FastAPI
"""
# Standard library
from datetime import datetime
import time
from typing import Annotated
import zoneinfo

# Third-party packages
from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# First-party application modules
from app.db import create_all_tables
from app.routers import customers, invoices, plans, transactions

# Create the application
app = FastAPI(lifespan=create_all_tables)

# Security scheme
security = HTTPBasic()

# Include routers
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(invoices.router)
app.include_router(plans.router)

# Middlewares
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    """
    Log the request time
    """
    start_time = time.time() # se guarda el tiempo inicial

    response = await call_next(request) # se ejecuta la solicitud

    process_time = time.time() - start_time # se calcula el tiempo

    response.headers["X-Process-Time"] = str(process_time) # se agrega el header

    print(
        f"""
            Request: {request.method} {request.url}
            Response: {response.status_code}
            Process Time: {process_time:.4f} seconds
        """
    )

    return response


@app.get('/')
# credentials es una dependencia totalmente registrada, que significa?
# Annotated es una función que permite agregar metadatos a una variable
# Depends es una función que permite agregar dependencias a una variable
# HTTPBasicCredentials es una clase que permite agregar credenciales de autenticación
# security es una instancia de HTTPBasic
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    """
    API root endpoint
    """
    print(credentials)
    if credentials.username == "David Hilera" and credentials.password == "admin123":
        return {'message': f'Hello, {credentials.username}'}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

country_timezones = {
    "CO": "America/Bogota",
    "US": "America/New_York",
    "MX": "America/Mexico_City",
    "PE": "America/Lima"
}


@app.get('/time/{iso_code}')
async def get_country(iso_code: str):
    """
    Get the time zone of a country by ISO code
    """
    iso = iso_code.upper()

    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)

    return {
        "time": datetime.now(tz)
    }
