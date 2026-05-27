from sqlalchemy.orm import Session

from app.models.user import User

from app.utils.password import hash_password, verify_password

from app.utils.jwt_handler import create_access_token


def register_user(request, db: Session):
    existing_user = db.query(User).filter(User.email == request.email).first()

    if existing_user:
        return None

    user = User(
        username=request.username,
        email=request.email,
        password=hash_password(request.password),
        role=request.role,
    )

    db.add(user)
    db.commit()

    return user


def login_user(request, db: Session):

    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        return None

    if not verify_password(request.password, user.password):
        return None

    token = create_access_token({"user_id": user.id, "role": user.role})

    return {"access_token": token, "role": user.role}
