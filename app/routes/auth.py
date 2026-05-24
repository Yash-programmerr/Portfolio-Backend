from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.auth import verify_password, create_access_token, get_current_admin
from app.middleware.rate_limit import limiter
from app.schemas.auth import LoginRequest, TokenResponse, MeResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


async def _issue_token(email: str, password: str) -> TokenResponse:
    db = get_db()
    user = await db.users.find_one({"email": email.lower()})
    if not user or not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=str(user["_id"]), extra={"email": user["email"]})
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
async def login(request: Request, payload: LoginRequest):
    """JSON login used by the admin dashboard frontend.
    Rate-limited to 10 attempts per minute per IP (brute-force protection)."""
    return await _issue_token(payload.email, payload.password)


@router.post("/token", response_model=TokenResponse, include_in_schema=False)
@limiter.limit("10/minute")
async def login_form(request: Request, form: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 form login used by Swagger UI's Authorize modal.
    `username` field accepts the admin email."""
    return await _issue_token(form.username, form.password)


@router.get("/me", response_model=MeResponse)
async def me(user: dict = Depends(get_current_admin)):
    return MeResponse(id=str(user["_id"]), email=user["email"])
