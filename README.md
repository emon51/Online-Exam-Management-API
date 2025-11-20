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
     
3. Install dependencies
```
pip install -r requirements.txt
```
