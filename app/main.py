from fastapi import FastAPI, Depends, HTTPException, Form, Response, status
from authlib.jose import jwt, JsonWebKey
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import HTMLResponse
from typing import Annotated


app = FastAPI()

security = HTTPBearer()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Read and return the HTML file content
    with open("templates/index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


# Read RSA keys from files
with open('../config/private_key.pem', 'rb') as f:
    private_key = f.read()

with open('../config/public_key.pem', 'rb') as f:
    public_key = f.read()


@app.post("/create-token", response_model=dict)
async def create_token(name: str = Form(...)):
    header = {"alg": "RS256", "typ":"JWT"}
    payload = {"roles": "NOTadmin", "sub": name}
    # Create a token with roles set to "NOTadmin"
    token = jwt.encode(header, payload, private_key)

    return {"token": token}


@app.get("/users/me", status_code=200)
async def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], response: Response):
    try:
        payload = jwt.decode(credentials.credentials, public_key)
        username: str = payload.get("sub")
        role: str = payload.get("roles")

        if username:
            response.status_code = status.HTTP_200_OK
            return payload

        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return HTTPException(status_code=401, detail="Unable to Verify Token")


    except Exception as e:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return HTTPException(status_code=401, detail="Unable to verity token. You are not authorized to access this resource!")




@app.get("/admin", status_code=200)
async def is_admin(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], response: Response):
    try:
        payload = jwt.decode(credentials.credentials, public_key)
        username: str = payload.get("sub")
        role: str = payload.get("roles")

        if role == "admin":
            response.status_code = status.HTTP_200_OK
            return {"message": "Welcome, Admin! You have successfully completed the BSides Sofia 2024 Challenge!"}

        elif role == "NOTadmin":
            response.status_code = status.HTTP_403_FORBIDDEN
            return HTTPException(status_code=403, detail=f"You are not authorized to access this resource as '{username}', you need to be 'admin'!")

        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return HTTPException(status_code=403, detail="You are NOTadmin, you need to be 'admin' to access this resource!")

    except Exception as e:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return HTTPException(status_code=401, detail="Unable to verity token. You are not authorized to access this resource!")


# Add Discovery endpoint
@app.get("/jwks")
def get_jwk():
    jwks = JsonWebKey.import_key(public_key).as_json()
    return jwks


# Enumerate hints using path parameters
@app.get("/hint/{hint_id}")
def get_hint(hint_id: int):
    hints = {
        1: "Hint 1: Did you already get a JWT? If so, send a request to the available endpoints, by using it as a Bearer token",
        2: "Hint 2: If you are not an admin, maybe you need to forge a token to become one",
        3: "Hint 3: Read about algorithm confusion in JWTs. I heard that PortSwigger are really good.",
        4: "Hint 4: Maybe try getting the public token with this tool: https://github.com/SecuraBV/jws2pubkey",
        5: "Hint 5: Don't dwell on it, we can convert a JWK to PEM, using this: https://8gwifi.org/jwkconvertfunctions.jsp",
        6: "Hint 6: JWT Editor (BApp Store) is your best friend!",
        7: "Hint 7: Use JWT Editor to create a symmetric key -> change the value of 'k' with the Base64 encoded public key (PEM)",
        8: "Hint 8: Change the value of alg to HS256 (from RS256) and change your role to admin, then sign it with your symmetric key"
    }

    # Check if the provided hint_number is valid
    if hint_id not in hints:
        return {"error": "Hint not found."}

    # Return the specified hint
    return {"hint": hints[hint_id]}