import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from turtle import pd
from urllib import response
from wsgiref import headers
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import PyPDF2
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt


class GradingSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Powered Grading System")
        self.root.geometry("1200x800")
        
        # Store questions and answers
        self.questions = []
        self.teacher_answers = []
        self.pdf_path = None
        self.api_key = ""
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttkb.Frame(self.root, padding=10)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # Title
        title_label = ttkb.Label(
            main_frame, 
            text="AI-Powered Grading System", 
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        )
        title_label.pack(pady=10)
        
        # API Key Section
        api_frame = ttkb.Labelframe(main_frame, text="API Configuration", padding=5)
        api_frame.pack(fill=X, pady=5)
        
        ttkb.Label(api_frame, text="Perplexity API Key:").pack(side=LEFT, padx=5)
        self.api_key_entry = ttkb.Entry(api_frame, width=50, show="*")
        self.api_key_entry.pack(side=LEFT, padx=5)
        ttkb.Button(
            api_frame, 
            text="Save Key", 
            command=self.save_api_key,
            bootstyle="success"
        ).pack(side=LEFT, padx=5)
        
        # Question and Answer Input Section
        input_frame = ttkb.Labelframe(main_frame, text="Teacher's Reference", padding=1)
        input_frame.pack(fill=BOTH, expand=YES, pady=1)
        
        # Question input
        ttkb.Label(input_frame, text="Question:", font=("Helvetica", 11, "bold")).pack(anchor=W)
        self.question_text = scrolledtext.ScrolledText(input_frame, height=4, wrap=tk.WORD)
        self.question_text.pack(fill=X, pady=2)
        
        # Answer input
        ttkb.Label(input_frame, text="Teacher's Answer:", font=("Helvetica", 11, "bold")).pack(anchor=W)
        self.answer_text = scrolledtext.ScrolledText(input_frame, height=6, wrap=tk.WORD)
        self.answer_text.pack(fill=X, pady=2)
        
        # Max marks
        marks_frame = ttkb.Frame(input_frame)
        marks_frame.pack(fill=X, pady=5)
        ttkb.Label(marks_frame, text="Maximum Marks:").pack(side=LEFT, padx=5)
        self.max_marks_entry = ttkb.Entry(marks_frame, width=10)
        self.max_marks_entry.insert(0, "10")
        self.max_marks_entry.pack(side=LEFT, padx=5)
        
        ttkb.Button(
            input_frame, 
            text="Add Question-Answer Pair", 
            command=self.add_qa_pair,
            bootstyle="info"
        ).pack(pady=5)
        
        # Display added questions
        self.qa_listbox = tk.Listbox(input_frame, height=3)
        self.qa_listbox.pack(fill=X, pady=5)
        
        # PDF Upload Section
        pdf_frame = ttkb.Labelframe(main_frame, text="Student Submission", padding=10)
        pdf_frame.pack(fill=X, pady=5)
        
        self.pdf_label = ttkb.Label(pdf_frame, text="No PDF selected", bootstyle="secondary")
        self.pdf_label.pack(side=LEFT, padx=5)
        
        ttkb.Button(
            pdf_frame, 
            text="Upload Student PDF", 
            command=self.upload_pdf,
            bootstyle="warning"
        ).pack(side=LEFT, padx=5)
        
        # Grade Button
        ttkb.Button(
            main_frame, 
            text="Grade Submission", 
            command=self.grade_submission,
            bootstyle="success",
            width=20
        ).pack(pady=10)
        
        # Results Section
        results_frame = ttkb.Labelframe(main_frame, text="Grading Results", padding=10)
        results_frame.pack(fill=BOTH, expand=YES, pady=10)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=12, wrap=tk.WORD)
        self.results_text.pack(fill=BOTH, expand=YES)
    
    def save_api_key(self):
        self.api_key = self.api_key_entry.get().strip()
        if self.api_key:
            messagebox.showinfo("Success", "API Key saved successfully!")
        else:
            messagebox.showwarning("Warning", "Please enter a valid API key")
    
    def add_qa_pair(self):
        question = self.question_text.get("1.0", tk.END).strip()
        answer = self.answer_text.get("1.0", tk.END).strip()
        max_marks = self.max_marks_entry.get().strip()
        
        if not question or not answer:
            messagebox.showwarning("Warning", "Please enter both question and answer")
            return
        
        try:
            max_marks = float(max_marks)
        except ValueError:
            messagebox.showwarning("Warning", "Please enter valid maximum marks")
            return
        
        self.questions.append({
            "question": question,
            "answer": answer,
            "max_marks": max_marks
        })
        
        self.qa_listbox.insert(tk.END, f"Q{len(self.questions)}: {question[:50]}... (Max: {max_marks} marks)")
        
        # Clear inputs
        self.question_text.delete("1.0", tk.END)
        self.answer_text.delete("1.0", tk.END)
        
        messagebox.showinfo("Success", "Question-Answer pair added!")
    
    def upload_pdf(self):
        file_path = filedialog.askopenfilename(
            title="Select Student PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if file_path:
            self.pdf_path = file_path
            self.pdf_label.config(text=f"Selected: {file_path.split('/')[-1]}")
    
    def extract_text_from_pdf(self, pdf_path):
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read PDF: {str(e)}")
            return None
    
    def call_perplexity_api(self, prompt):
        if not self.api_key:
            messagebox.showwarning("Warning", "API Key not set")
            return None 
    
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }       
        data = {
            "model": "sonar-pro",       
            "messages": [
                {"role": "user", "content": prompt}
            ],
        # Optional: Add these for better control
        # "temperature": 0.7,
        # "max_tokens": 1000,
        }
    
        try:
            response = requests.post(url, headers=headers, json=data)  # Use json= instead of data=json.dumps()
            response.raise_for_status()
            result = response.json()
        
        # More defensive: check if the expected keys exist
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                messagebox.showerror("Error", "Unexpected API response format")
                return None
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"API request failed: {str(e)}")
            return None
        except (KeyError, IndexError) as e:
            messagebox.showerror("Error", f"Failed to parse API response: {str(e)}")
            return None
        
    
    def grade_submission(self):
        if not self.questions:
            messagebox.showwarning("Warning", "Please add at least one question-answer pair")
            return
        
        if not self.pdf_path:
            messagebox.showwarning("Warning", "Please upload a student PDF")
            return
        
        # Extract student answers from PDF
        student_text = self.extract_text_from_pdf(self.pdf_path)
        if not student_text:
            return
        
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, "Grading in progress...\n\n")
        self.root.update()
        
        total_marks_obtained = 0
        total_max_marks = 0
        self.current_submission_scores = []
        
        for idx, qa in enumerate(self.questions, 1):
            question = qa["question"]
            teacher_answer = qa["answer"]
            max_marks = qa["max_marks"]
            total_max_marks += max_marks
            
            # Create prompt for AI grading
            prompt = f"""
            Grade the following student answer based on the teacher's reference answer.
            
            QUESTION:
            {question}
            
            TEACHER'S REFERENCE ANSWER (This is the primary standard):
            {teacher_answer}
            
            STUDENT'S SUBMISSION (Extracted from PDF):
            {student_text}
            
            GRADING CRITERIA:
            - Maximum Marks: {max_marks}
            - Prioritize matching with the teacher's answer
            - Evaluate accuracy, completeness, and understanding
            - Ignore severe spelling and grammar errors
            - Check whether same keywords are present in {teacher_answer} and {student_text}
            - Be objective and fair
            - Ignore any additional information not relevant to the question
            - Focus on content quality but ignore minor formatting issues and spelling mistakes
            - Deduct marks for missing key points from the teacher's answer but check if the same keywords are present in both answers
            - Do not award marks for irrelevant or incorrect information but also do not deduct marks for minor  spelling mistakes and do not deduct marks for additional irrelevant information.
            - Ignore if there are errors in punctuation, spelling, or grammar.
            - Ignore if there is error in text extraction from PDF.
            - Do leinient checking
            -   ==IMPORTANT==: Check if the same keywords are present in both answers and award marks accordingly.
            Based on the above criteria, grade the student's answer.



            
            Please provide:
            1. Marks awarded (out of {max_marks})
            2. Brief explanation of grading
            3. Specific suggestions for improvement
            
            Format your response as:
            MARKS: [X/{max_marks}]
            EXPLANATION: [Your explanation]
            SUGGESTIONS: [Improvement suggestions]
            """
            
            result = self.call_perplexity_api(prompt)
            
            if result:
                # Parse marks from result
                try:
                    marks_line = [line for line in result.split('\n') if 'MARKS:' in line][0]
                    marks_awarded = float(marks_line.split('[')[1].split('/')[0])
                    self.current_submission_scores.append({
                        "question_number": idx,
                        "marks_obtained": marks_awarded,
                        "max_marks": max_marks
                    })
                    total_marks_obtained += marks_awarded

                except (IndexError, ValueError):
                    marks_awarded = 0.0  # Default to 0 if parsing fails    

                
                
                self.results_text.insert(tk.END, f"{'='*60}\n")
                self.results_text.insert(tk.END, f"QUESTION {idx}:\n{question}\n\n")
                self.results_text.insert(tk.END, f"{result}\n\n")
            else:
                self.results_text.insert(tk.END, f"Failed to grade Question {idx}\n\n")
        
        # Overall summary
        # Calculate percentage with proper parentheses
        percentage = ((marks_awarded / total_max_marks) * 100) 

        # Clear previous results (optional)
        # self.results_text.delete(1.0, tk.END)

        # Display results
        self.results_text.insert(tk.END, f"\n{'='*60}\n")
        self.results_text.insert(tk.END, "OVERALL RESULTS:\n")
        self.results_text.insert(tk.END, f"Total Marks: {marks_awarded}/{total_max_marks}\n")
        self.results_text.insert(tk.END, f"Percentage: {percentage:.2f}%\n")
        self.results_text.insert(tk.END, f"{'='*60}\n")

        # Display bar chart of marks per question
       

        # Prepare data for plotting
        question_labels = [f"Q{s['question_number']}" for s in self.current_submission_scores]
        marks_awarded = [s['marks_awarded'] for s in self.current_submission_scores]
        max_marks_list = [s['max_marks'] for s in self.current_submission_scores]
        
        # Create a DataFrame for easy handling
        df_scores = pd.DataFrame({
            'Question': question_labels,
            'Marks Obtained': marks_awarded,
            'Max Marks': max_marks_list
        })
        
        plt.figure(figsize=(10, 6))
        
        # Bar chart for Marks Obtained
        plt.bar(df_scores['Question'], df_scores['Marks Obtained'], color='skyblue', label='Marks Obtained')
        
        # Optional: Add a line/dots for Max Marks to show the maximum possible score
        plt.plot(df_scores['Question'], df_scores['Max Marks'], marker='_', linestyle='', color='red', label='Max Marks', markersize=20)
        
        # Add labels and title
        plt.xlabel("Question Number")
        plt.ylabel("Marks")
        plt.title("Student Marks Per Question")
        plt.legend()
        plt.grid(axis='y', linestyle='--')
        
        # Add text labels on top of the bars
        for i, row in df_scores.iterrows():
            plt.text(i, row['Marks Obtained'] + 0.1, f"{row['Marks Obtained']:.1f}/{row['Max Marks']:.1f}", ha='center')

        plt.show()


        file_path = r'C:\Users\Nishant\OneDrive\ドキュメント\Book1.csv'
        df = pd.read_csv(file_path)

        # Inspect column names (optional)
        print(df.head())
        marks = df["Marks"]

        range_counts = {
            "0-9": 0,
            "10-19": 0,
            "20-29": 0,
            "30-39": 0,
            "40-50": 0
        }

        for m in marks:
            if 0 <= m <= 9:
                range_counts["0-9"] += 1
            if 10 <= m <= 19:
                range_counts["10-19"] += 1
            if 20 <= m <= 29:
                range_counts["20-29"] += 1
            elif 30 <= m <= 39:
                range_counts["30-39"] += 1
            elif 40 <= m <= 50:
                range_counts["40-50"] += 1

        print(range_counts)
        marks_range = list(range_counts.keys())
        no_of_students = list(range_counts.values())

        plt.bar(marks_range,no_of_students)

        plt.xlabel("Marks Range")
        plt.ylabel("Number of Students")
        plt.title("Number of Students in Each Marks Range")

        plt.show()


        

if __name__ == "__main__":
    root = ttkb.Window(themename="cosmo")
    app = GradingSystemApp(root)
    root.mainloop()
