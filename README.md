# Exam-Mangement-System
A simple Exam Management System built with FastAPI and SQLite. Teachers can create exams and questions, and students can submit answers and receive scores.
No authentication is currently implemented.

# Features
## Admin
- Create exams
- Upload question's Excel file
- Assign questions to exams
- Publish exams
- View all students

## Student
- View exam and questions
- Submit answers
- View scores after submission answers


# Tables and relationship among them
```
    USERS {
        id string "PK"
        username string
        email string
        password string
        role string
    }

    QUESTIONS {
        id string "PK"
        title string
        type string
        complexity string
        options json "nullable"
        correct_answers json "nullable"
        max_score int
    }

    EXAMS {
        id string "PK"
        title string
        start_time string
        end_time string
        duration int
        published boolean
    }

    EXAM_QUESTIONS {
        id string "PK"
        exam_id string "FK -> EXAMS.id  (1 exam has many questions)"
        question_id string "FK -> QUESTIONS.id  (1 question used in many exams)"
    }

    SUBMISSIONS {
        id string "PK"
        exam_id string "FK -> EXAMS.id  (1 exam has many submissions)"
        student_id string "FK -> USERS.id  (1 user has many submissions)"
        answers json
        score int
        submitted boolean
        submitted_at datetime
    }
```

## Setup

1. **Clone the project**
```
git clone https://github.com/emon51/Exam-Management-API.git
```
```
cd Exam-Management-API/backend
```

2. Create a virtual environment
```
python -m venv venv
```
3. Activate virtual environment
- For Windows
     ```
     venv\Scripts\activate
     ```
- For Mac/Linux
     ```
     source venv/bin/activate
     ```
     
4. Install dependencies
```
pip install -r requirements.txt
```
  
5. Run the FastAPI server
   ```
   uvicorn main:app --reload
   ```
6. Open `http://127.0.0.1:8000/docs` in your browser to see API docs.

   **Thank You :)**

