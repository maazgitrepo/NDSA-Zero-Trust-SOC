from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import requests

security = HTTPBearer()

KEYCLOAK_URL = "http://192.168.2.211:8081"
REALM = "ndsa"

ISSUER = f"{KEYCLOAK_URL}/realms/{REALM}"
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"

jwks = requests.get(JWKS_URL).json()


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            jwks,
            algorithms=["RS256"],
            issuer=ISSUER,
            options={
                "verify_aud": False,
                "verify_exp": True
            }
        )

        return payload

    except Exception as e:
        print("TOKEN ERROR:", repr(e))

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

def require_role(role: str):
    def role_checker(user=Depends(verify_token)):
        roles = user.get("realm_access", {}).get("roles", [])

        if role not in roles:
            raise HTTPException(
                status_code=403,
                detail=f"{role} role required"
            )

        return user

    return role_checker


admin_required = require_role("admin")
analyst_required = require_role("analyst")
viewer_required = require_role("viewer")
