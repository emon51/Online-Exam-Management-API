from fastapi import FastAPI, Depends, HTTPException, Request, UploadFile
import schemas 
from database import SessionLocal, Base, engine
from sqlalchemy.orm import Session
import models
import openpyxl
import json
from io import BytesIO
from typing import List, Optional


#==================================================================================================================

app = FastAPI(title="Online Exam Management API.")

#================================================================================================================== 

Base.metadata.create_all(bind=engine)
#==================================================================================================================

# To get DB session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#=================================================================================================================
# Helper functions.

def parse_excel(file_obj):
    wb = openpyxl.load_workbook(file_obj)
    sheet = wb.active

    rows = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        rows.append({
            "title": row[0],
            "type": row[1],
            "complexity": row[2],
            "options": row[3],
            "correct_answers": row[4],
            "max_score": row[5]
        })

    return rows
#==================================================================================================================

@app.get('/', tags=["Testing"], description="Test inital setup")
async def index():
    return {"message": "Welcome."}
#==================================================================================================================

@app.post('/signup', tags=["Account"], description="Users registration")
async def signup(user: schemas.UserModel, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=403, detail="Already registered.")
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    return db_user 
#==================================================================================================================

@app.get('/users',  tags=["Account"], description="List of users")
async def users(db: Session=Depends(get_db)):
    all_users = db.query(models.User).all()
    if all_users:
        return all_users 
    else:
        raise HTTPException(status_code=404, detail="No users found.")
    
#==================================================================================================================

@app.post("/login", tags=["Account"], description="Users login")
async def user_login(user: schemas.LoginModel, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.password != db_user.password:
        raise HTTPException(status_code=400, detail="Invalid password.")
        
    return {"message": f"Welcome {db_user.username}", "user_id": db_user.id, "role": db_user.role}

    
#==================================================================================================================

@app.get("/questions/list", tags=["Question Bank"], description="List of questions")
async def questions(db: Session = Depends(get_db)):
    all_questions = db.query(models.Question).all()
    if all_questions:
        return all_questions
    else:
        raise HTTPException(status_code=404, detail="No questions found.")
    

#==================================================================================================================

@app.post("/questions/upload-xlsx", tags=["Question Bank"], description="Upload excel file of questions")
async def upload_questions(file: UploadFile, db: Session = Depends(get_db)):
    content = await file.read()
    data = parse_excel(BytesIO(content))
    for q in data:
        db_question = models.Question(
            title=q["title"],
            type=q["type"],
            complexity=q["complexity"],
            options=json.loads(q["options"]) if q["options"] else None,
            correct_answers=json.loads(q["correct_answers"]) if q["correct_answers"] else None,
            max_score=q["max_score"]
        )
        db.add(db_question)

    db.commit()

    return {"message": "Questions uploaded successfully."}

#==================================================================================================================


@app.post("/exams/create", tags=["Exam"], description="Create an Exam")
async def create_exam(exm: schemas.ExamCreate, db: Session = Depends(get_db)):
    exam = models.Exam(**exm.dict())
    db.add(exam)
    db.commit()
    return {"message": "Exam created successfully."}


#==================================================================================================================

@app.get("/exams/list", tags=["Exam"], description="Exams list")
async def exam_list(db: Session = Depends(get_db)):
    all_exams = db.query(models.Exam).all()
    if all_exams:
        return all_exams
    else:
        raise HTTPException(status_code=404, detail="No exams found.")

#==================================================================================================================

# add questions to exam.
@app.post("/exams/{exam_id}/add-questions", tags=["Question Bank"], description="Add questiosn to an Exam")
def add_questions_to_exam(exam_id: str, question_ids: List[str], db: Session = Depends(get_db)):
    exam = db.query(models.Exam).filter(models.Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    for qid in question_ids:
        link = models.ExamQuestion(exam_id=exam_id, question_id=qid)
        db.add(link)
    db.commit()
    return {"message": "Questions added to the exam."}

#==================================================================================================================


@app.get("/exams/exam-question-list", tags=["Exam"], description="List of Exams with questions")
async def exam_question_list(db: Session = Depends(get_db)):
    all_records = db.query(models.ExamQuestionBank).all()
    if all_records:
        return all_records
    else:
        raise HTTPException(status_code=404, detail="Not found.")

#==================================================================================================================

# Publish exam.
@app.post("/exams/{exam_id}/publish", tags=["Exam"], description="Published an Exam")
async def publish_exam(exam_id: str, request: Request, db: Session = Depends(get_db)):
    
    exam = db.query(models.Exam).filter(models.Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found.")
    exam.published = True
    db.commit()
    return {"message": "Published."}

#==================================================================================================================


# Get a specific exam's questions.
@app.get("/exams/{exam_id}/questions/", tags=["Question Bank"], description="List of questions of an Exam")
async def get_exam_questions(exam_id: str, student_id: str, db: Session = Depends(get_db)):
    records = db.query(models.ExamQuestionBank).filter(models.ExamQuestionBank.exam_id == exam_id).all()
    all_question_ids = [record.question_id for record in records]
    all_questions = db.query(models.Question).filter(models.Question.id.in_(all_question_ids)).all() if all_question_ids else []
    return all_questions

#==================================================================================================================

# Submit exam.
<<<<<<< HEAD
@app.post("/exams/{exam_id}/submit/{student_id}", tags=["Exam"], description="Submit Exam by students")
=======
@app.post("/exams/{exam_id}/submit/{student_id}")
>>>>>>> 662012ee1fb9fad131fb8863b22ecc6f9ac14c03
async def submit_exam(exam_id: str, student_id: str, payload: schemas.SubmittedPayload, db: Session = Depends(get_db)):
    # Get all questions belonging to this exam.
    qids = [q.question_id for q in db.query(models.ExamQuestionBank).filter_by(exam_id=exam_id).all()]
    questions = db.query(models.Question).filter(models.Question.id.in_(qids)).all()

    score = 0
    stored = {}

    for q in questions:
        qid = str(q.id)
        ans = payload.answers.get(qid)
        stored[qid] = ans
        
        if not q.correct_answers:
            continue

        # Multi-select.
        if isinstance(q.correct_answers, list):
            if isinstance(ans, list) and set(ans) == set(q.correct_answers):
                score += q.max_score

        # Single answer
        else:
            if ans == q.correct_answers:
                score += q.max_score

    # Save submission
    sub = models.Submission(
        exam_id=exam_id,
        student_id=student_id,
        answers=stored,
        score=score,
        submitted=True
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)

    return {"score": score, "submission_id": sub.id}

#==================================================================================================================
# Get results for students.

@app.get("/results/student/{student_id}", tags=["Results"], description="Get results by students")
async def student_results(student_id: str, db: Session = Depends(get_db)):
    results = (db.query(models.Submission).filter(models.Submission.student_id == student_id).all())

    if not results:
        raise HTTPException(status_code=404, detail="No results found.")

    output = []
    for r in results:
        exam = db.query(models.Exam).filter(models.Exam.id == r.exam_id).first()

        output.append({
            "submission_id": r.id,
            "exam_id": r.exam_id,
            "exam_title": exam.title,
            "score": r.score,
            "answers": r.answers,
            "submitted": r.submitted
        })

    return {"student_id": student_id, "results": output}

#==================================================================================================================
# Get results for admin.
@app.get("/results/exam/{exam_id}", tags=["Results"], description="Get an Exam's result by Admins")
async def exam_results(exam_id: str, db: Session = Depends(get_db)):
    results = (db.query(models.Submission).filter(models.Submission.exam_id == exam_id).all())

    if not results:
        raise HTTPException(status_code=404, detail="No submissions found for this exam.")

    output = []
    for r in results:
        student = db.query(models.User).filter(models.User.id == r.student_id).first()

        output.append({
            "submission_id": r.id,
            "student_id": r.student_id,
            "student_name": student.username,
            "score": r.score,
            "answers": r.answers,
            "submitted": r.submitted
        })

    return {"exam_id": exam_id, "results": output}

#==================================================================================================================

