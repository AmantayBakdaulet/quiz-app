from fastapi import Header, HTTPException


def get_user_id(x_user_id: str = Header(...)):
    if not x_user_id:
        raise HTTPException(status_code=400, detail="x-user-id header missing")
    return x_user_id
