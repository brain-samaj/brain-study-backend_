# Brain Study Exam Module Database Migration Notes


## New Tables

The exam system requires the following tables:

---

## 1. exam_sessions

Purpose:

Stores every generated exam attempt.

Columns:

- id
- owner_id
- material_id
- exam_type
- difficulty
- status
- total_questions
- total_marks
- obtained_marks
- percentage
- duration_minutes
- started_at
- expires_at
- submitted_at
- created_at


Indexes:

- owner_id
- material_id
- status


---

## 2. exam_questions

Purpose:

Stores generated exam questions.

Supports:

- Objective questions
- Theory questions
- Mixed exams


Columns:

- id
- session_id
- question_number
- question_type
- question
- topic
- difficulty
- marks
- options
- correct_answer
- explanation
- marking_scheme
- model_answer


Indexes:

- session_id


---

## 3. exam_answers

Purpose:

Stores student responses.


Supports:

Objective:

- selected option


Theory:

- typed answer
- handwritten OCR answer
- final merged answer


Columns:

- id
- session_id
- question_id
- selected_option
- text_answer
- ocr_answer
- final_answer
- awarded_marks
- feedback
- reasoning


Indexes:

- session_id
- question_id


---

## 4. exam_answer_attachments

Purpose:

Stores handwritten answer images.


Supports:

- camera capture
- multiple pages
- OCR processing


Columns:

- id
- answer_id
- filename
- storage_path
- mime_type
- page_number
- ocr_status
- ocr_text


Indexes:

- answer_id
- ocr_status


---

## 5. exam_submissions

Purpose:

Creates immutable exam snapshots.

Stores:

- submitted answers
- question snapshot
- attachment references
- submission metadata


---

## 6. exam_results

Purpose:

Permanent grading record.


Stores:

- score
- percentage
- objective performance
- theory performance
- AI feedback
- weaknesses
- strengths
- recommendations


---

# Migration Order

Run migrations in this order:


1. Create exam_sessions


2. Create exam_questions


3. Create exam_answers


4. Create exam_answer_attachments


5. Create exam_submissions


6. Create exam_results



# Relationships


User

|

+-- ExamSession


StudyMaterial

|

+-- ExamSession


ExamSession

|

+-- ExamQuestion

|

+-- ExamAnswer

|

+-- ExamSubmission

|

+-- ExamResult


ExamAnswer

|

+-- ExamAnswerAttachment



# Production Index Strategy


Frequently queried:

- user exam history
- active exams
- grading queue
- OCR queue


Required indexes:

exam_sessions(owner_id,status)

exam_questions(session_id)

exam_answers(session_id,question_id)

exam_answer_attachments(ocr_status)



# Future Scaling


When traffic grows:

Move:

- OCR processing
- AI grading
- Review generation

into background workers:

- Celery
- Redis Queue
- Temporal


Database remains source of truth.
