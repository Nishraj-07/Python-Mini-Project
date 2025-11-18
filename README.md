This repository contains my mini project for the First Year BTech CSE program at MIT-WPU.
The project is implemented in Python and demonstrates essential concepts and skills learned during the course.
**Grade.py** implements an AI-powered grading system as a desktop GUI application using Python and the Tkinter/ttkbootstrap library. Its main features and workflow:

- **User Interface:** The app provides fields for teachers to input questions, answers, and maximum marks for each question. Teachers can add multiple question-answer pairs to a list.
- **API Key Entry:** Users must supply a Perplexity AI API key to utilize AI grading features.
- **Student Submission:** Users upload a student’s answer PDF, from which the program extracts text.
- **AI Grading Logic:** For each question, the system sends a prompt to Perplexity AI including the question, teacher’s reference answer, extracted student response, and grading criteria.
- **Result Parsing:** The AI returns marks awarded, explanations, and improvement suggestions in a formatted response. The app parses this to tally total marks and provides feedback on every question.
- **Summary and Display:** The app displays results per question, plus an overall score and percentage.

Additional features include success/error notifications and defensive error handling for missing API keys, invalid inputs, and API request failures.

The overall purpose of Grade.py is to automate evaluating student PDF submissions against reference answers using AI, visualizing results in an interactive GUI.
