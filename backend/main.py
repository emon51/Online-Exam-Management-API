from fastapi import FastAPI, Depends, HTTPException
import schemas 
from database import SessionLocal, Base, engine
from sqlalchemy.orm import Session
import models

app = FastAPI(title="Online Exam Management API.")

Base.metadata.create_all(bind=engine)

# To get DB session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
async def index():
    return {"message": "Welcome."}

@app.post('/signup')
async def signup(user: schemas.UserModel, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=403, detail="Already registered.")
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"user": user.dict()}

@app.get('/users')
async def users(db: Session=Depends(get_db)):
    all_users = db.query(models.User).all()
    if all_users:
        return all_users 
    else:
        raise HTTPException(status_code=404, detail="No users found.")