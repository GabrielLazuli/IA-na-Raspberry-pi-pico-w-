"""
Quiz Module for Raspberry Pi Pico W
Provides personalized quiz functionality using Gemini API
"""

import json
import time
from config import DEBUG_MODE


class QuizModule:
    def __init__(self, gemini_client, keyboard):
        self.gemini_client = gemini_client
        self.keyboard = keyboard
        self.current_score = 0
        self.total_questions = 0
        self.quiz_history = []
        
        # Predefined topics and difficulties
        self.topics = {
            '1': 'Science',
            '2': 'History',
            '3': 'Geography',
            '4': 'Literature',
            '5': 'Mathematics',
            '6': 'Technology',
            '7': 'Sports',
            '8': 'Movies',
            '9': 'Music',
            '10': 'General Knowledge'
        }
        
        self.difficulties = {
            '1': 'easy',
            '2': 'medium',
            '3': 'hard'
        }
        
        if DEBUG_MODE:
            print("Quiz module initialized")
    
    def display_topics(self):
        """Display available quiz topics"""
        print("\n=== Quiz Topics ===")
        for key, topic in self.topics.items():
            print(f"{key}. {topic}")
        print("0. Custom topic")
    
    def display_difficulties(self):
        """Display difficulty levels"""
        print("\n=== Difficulty Levels ===")
        for key, difficulty in self.difficulties.items():
            print(f"{key}. {difficulty.title()}")
    
    def get_topic_choice(self):
        """Get topic choice from user"""
        while True:
            self.display_topics()
            choice = self.keyboard.get_input_prompt("Select topic (0-10): ")
            
            if choice == '0':
                custom_topic = self.keyboard.get_input_prompt("Enter custom topic: ")
                if custom_topic.strip():
                    return custom_topic.strip()
                else:
                    print("Invalid topic. Please try again.")
            elif choice in self.topics:
                return self.topics[choice]
            else:
                print("Invalid choice. Please try again.")
    
    def get_difficulty_choice(self):
        """Get difficulty choice from user"""
        while True:
            self.display_difficulties()
            choice = self.keyboard.get_input_prompt("Select difficulty (1-3): ")
            
            if choice in self.difficulties:
                return self.difficulties[choice]
            else:
                print("Invalid choice. Please try again.")
    
    def generate_question(self, topic, difficulty):
        """Generate a quiz question"""
        try:
            print(f"Generating {difficulty} question about {topic}...")
            question_data = self.gemini_client.generate_quiz_question(topic, difficulty)
            return question_data
        except Exception as e:
            if DEBUG_MODE:
                print(f"Question generation error: {e}")
            # Fallback question
            return {
                "question": f"What is an important fact about {topic}?",
                "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                "correct_answer": "A",
                "explanation": "This is a fallback question due to generation error."
            }
    
    def ask_question(self, question_data):
        """Ask a question and get user's answer"""
        print(f"\n=== Question {self.total_questions + 1} ===")
        print(f"Question: {question_data['question']}")
        print("\nOptions:")
        
        for option in question_data['options']:
            print(f"  {option}")
        
        while True:
            user_answer = self.keyboard.get_input_prompt(
                "Your answer (A, B, C, or D): "
            ).upper().strip()
            
            if user_answer in ['A', 'B', 'C', 'D']:
                return user_answer
            else:
                print("Please enter A, B, C, or D.")
    
    def check_answer(self, user_answer, question_data):
        """Check if the answer is correct"""
        correct_answer = question_data['correct_answer'].upper()
        is_correct = user_answer == correct_answer
        
        print(f"\n=== Answer Result ===")
        if is_correct:
            print("✓ Correct!")
            self.current_score += 1
        else:
            print("✗ Incorrect!")
            print(f"The correct answer was: {correct_answer}")
        
        print(f"Explanation: {question_data['explanation']}")
        self.total_questions += 1
        
        return is_correct
    
    def display_score(self):
        """Display current score"""
        if self.total_questions > 0:
            percentage = (self.current_score / self.total_questions) * 100
            print(f"\n=== Current Score ===")
            print(f"Correct: {self.current_score}/{self.total_questions}")
            print(f"Percentage: {percentage:.1f}%")
        else:
            print("No questions answered yet.")
    
    def single_question_quiz(self):
        """Single question quiz mode"""
        print("\n=== Single Question Quiz ===")
        
        topic = self.get_topic_choice()
        difficulty = self.get_difficulty_choice()
        
        question_data = self.generate_question(topic, difficulty)
        user_answer = self.ask_question(question_data)
        is_correct = self.check_answer(user_answer, question_data)
        
        # Save to history
        self.quiz_history.append({
            'topic': topic,
            'difficulty': difficulty,
            'question': question_data['question'],
            'user_answer': user_answer,
            'correct_answer': question_data['correct_answer'],
            'is_correct': is_correct,
            'timestamp': time.time()
        })
        
        self.display_score()
    
    def multiple_question_quiz(self):
        """Multiple question quiz mode"""
        print("\n=== Multiple Question Quiz ===")
        
        # Get number of questions
        while True:
            try:
                num_questions = int(self.keyboard.get_input_prompt(
                    "How many questions? (1-10): "
                ))
                if 1 <= num_questions <= 10:
                    break
                else:
                    print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Please enter a valid number.")
        
        topic = self.get_topic_choice()
        difficulty = self.get_difficulty_choice()
        
        # Reset score for this quiz
        start_score = self.current_score
        start_total = self.total_questions
        
        print(f"\nStarting {num_questions}-question quiz on {topic} ({difficulty})")
        
        for i in range(num_questions):
            print(f"\n--- Question {i + 1} of {num_questions} ---")
            
            question_data = self.generate_question(topic, difficulty)
            user_answer = self.ask_question(question_data)
            is_correct = self.check_answer(user_answer, question_data)
            
            # Save to history
            self.quiz_history.append({
                'topic': topic,
                'difficulty': difficulty,
                'question': question_data['question'],
                'user_answer': user_answer,
                'correct_answer': question_data['correct_answer'],
                'is_correct': is_correct,
                'timestamp': time.time()
            })
            
            # Show progress
            quiz_score = self.current_score - start_score
            quiz_total = self.total_questions - start_total
            print(f"Quiz progress: {quiz_score}/{quiz_total}")
            
            if i < num_questions - 1:
                continue_quiz = self.keyboard.get_input_prompt(
                    "Continue to next question? (y/n): "
                ).lower()
                if continue_quiz != 'y':
                    break
        
        # Final quiz results
        final_score = self.current_score - start_score
        final_total = self.total_questions - start_total
        final_percentage = (final_score / final_total * 100) if final_total > 0 else 0
        
        print(f"\n=== Quiz Complete ===")
        print(f"Topic: {topic} ({difficulty})")
        print(f"Score: {final_score}/{final_total} ({final_percentage:.1f}%)")
        
        if final_percentage >= 80:
            print("Excellent work! 🌟")
        elif final_percentage >= 60:
            print("Good job! 👍")
        else:
            print("Keep practicing! 📚")
    
    def view_history(self):
        """View quiz history"""
        if not self.quiz_history:
            print("No quiz history available.")
            return
        
        print("\n=== Quiz History ===")
        print(f"Total questions answered: {len(self.quiz_history)}")
        
        correct_count = sum(1 for q in self.quiz_history if q['is_correct'])
        total_count = len(self.quiz_history)
        overall_percentage = (correct_count / total_count * 100) if total_count > 0 else 0
        
        print(f"Overall accuracy: {correct_count}/{total_count} ({overall_percentage:.1f}%)")
        
        # Show recent questions
        print(f"\nLast 5 questions:")
        recent_questions = self.quiz_history[-5:]
        
        for i, q in enumerate(recent_questions, 1):
            status = "✓" if q['is_correct'] else "✗"
            print(f"{i}. {status} {q['topic']} ({q['difficulty']})")
            print(f"   Q: {q['question'][:50]}...")
    
    def reset_score(self):
        """Reset the quiz score"""
        confirm = self.keyboard.get_input_prompt(
            "Are you sure you want to reset your score? (y/n): "
        ).lower()
        
        if confirm == 'y':
            self.current_score = 0
            self.total_questions = 0
            self.quiz_history = []
            print("Score reset successfully!")
        else:
            print("Score reset cancelled.")
    
    def run(self):
        """Run the quiz module"""
        while True:
            print("\n=== Quiz Module ===")
            print("1. Single Question")
            print("2. Multiple Questions")
            print("3. View Score")
            print("4. View History")
            print("5. Reset Score")
            print("0. Back to main menu")
            
            choice = self.keyboard.get_input_prompt("Select option: ")
            
            if choice == '0':
                break
            elif choice == '1':
                self.single_question_quiz()
            elif choice == '2':
                self.multiple_question_quiz()
            elif choice == '3':
                self.display_score()
            elif choice == '4':
                self.view_history()
            elif choice == '5':
                self.reset_score()
            else:
                print("Invalid option. Please try again.")