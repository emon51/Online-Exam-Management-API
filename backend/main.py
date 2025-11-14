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
    

@app.post("/login")
async def user_login(user: schemas.LoginModel, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.password != db_user.password:
        raise HTTPException(status_code=400, detail="Invalid password.")
        
    return {"message": f"Welcome {db_user.username}", "role": db_user.role}


@app.post("/add-question")
async def add_question(question: schemas.QuestionModel, db: Session = Depends(get_db)):
    db_question = models.Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return {"question": question.dict()}
    

@app.get("/questions")
async def questions(db: Session = Depends(get_db)):
    all_questions = db.query(models.Question).all()
    if all_questions:
        return all_questions
    else:
        raise HTTPException(status_code=404, detail="No questions found.")