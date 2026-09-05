from app.api.deps import require_role
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import verify_password, get_password_hash, create_access_token

router = APIRouter()

# Mock DB for testing. Member 5 will replace this with actual DB queries later.
MOCK_USERS_DB = {
    "asha_worker_1": {
        "username": "asha_worker_1",
        "hashed_password": get_password_hash("secret123"),
        "role": "ASHA"
    },
    "admin_1": {
        "username": "admin_1",
        "hashed_password": get_password_hash("admin123"),
        "role": "ADMIN"
    }
}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticates a user and returns a JWT Bearer token."""
    user = MOCK_USERS_DB.get(form_data.username)
    
    # Check if user exists and password is correct
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate token with user's role embedded
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/dashboard/asha")
async def asha_dashboard(current_user: dict = Depends(require_role("ASHA"))):
    """A highly secure endpoint only accessible by ASHA workers."""
    return {
        "message": f"Welcome ASHA worker {current_user['username']}!", 
        "data": "Confidential community health stats load here."
    }
