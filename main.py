# main.py

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# --- TU API KEY (de la imagen que enviaste) ---
API_KEY = "6b310e6a79ffa7fba871c9b0"

# --- 1. CREACIÓN DE LA APP ---
# Esta es la variable 'app' que Uvicorn busca
app = FastAPI(
    title="API Taller Finanzas",
    description="Backend que consume la ExchangeRate-API"
)

# --- 2. CONFIGURACIÓN DE CORS ---
# Permite que tu 'index.html' se comunique con este backend
origins = [
    "http://127.0.0.1:5500",  # Para Live Server de VS Code
    "http://localhost:5500",
    "null",  # Para cuando abres el 'index.html' como un archivo local
    "*"      # Permite todo (para depuración fácil)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- 3. ENDPOINT (LA RUTA DE TU API) ---
@app.get("/api/tasa-cambio")
async def obtener_tasa_de_cambio(moneda_base: str, moneda_destino: str):
    """
    Consume la API v6 de ExchangeRate-API y devuelve la tasa
    entre dos monedas específicas.
    """
    
    # --- URL v6 con tu API Key personal ---
    API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{moneda_base}"

    try:
        # Hacemos la llamada a la API externa
        async with httpx.AsyncClient() as client:
            response = await client.get(API_URL)
            # Lanza un error si la respuesta es 4xx o 5xx (ej. 404 si la moneda_base no existe)
            response.raise_for_status() 

            data = response.json()
            
            # Verificamos que la llamada a la API v6 fue exitosa
            if data.get("result") != "success":
                raise HTTPException(status_code=500, detail="La API externa no devolvió un resultado exitoso")

            # En v6, las tasas están en 'conversion_rates'
            if "conversion_rates" not in data or moneda_destino not in data["conversion_rates"]:
                raise HTTPException(status_code=404, detail="Moneda de destino no encontrada en la respuesta de la API")

            tasa = data["conversion_rates"][moneda_destino]

            # Esta es la respuesta que tu backend le da a tu frontend
            return {
                "moneda_base": moneda_base,
                "moneda_destino": moneda_destino,
                "tasa": tasa
            }

    except httpx.HTTPStatusError as exc:
        # Captura errores de la API externa (ej. "Moneda no encontrada")
        raise HTTPException(status_code=exc.response.status_code, detail=f"Error de la API externa: {exc.response.text}")
    except Exception as e:
        # Captura cualquier otro error
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")