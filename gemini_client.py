"""
Gemini API Client for Raspberry Pi Pico W
Handles communication with Google's Gemini 1.5 Flash API
"""

import json
import time
from config import GEMINI_API_KEY, GEMINI_API_URL, TIMEOUT_SECONDS, DEBUG_MODE


class GeminiClient:
    def __init__(self, wifi_manager):
        self.wifi_manager = wifi_manager
        self.api_key = GEMINI_API_KEY
        self.api_url = GEMINI_API_URL
        self.headers = {
            'Content-Type': 'application/json',
            'x-goog-api-key': self.api_key
        }
        
        if DEBUG_MODE:
            print("Gemini API Client initialized")
    
    def generate_content(self, prompt, temperature=0.7, max_tokens=1000):
        """Generate content using Gemini API"""
        if not self.wifi_manager.is_connected:
            raise Exception("WiFi not connected")
        
        # Prepare request payload
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": temperature,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": max_tokens,
                "stopSequences": []
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }
        
        try:
            if DEBUG_MODE:
                print(f"Sending request to Gemini API...")
            
            response = self.wifi_manager.make_request(
                self.api_url,
                method='POST',
                headers=self.headers,
                data=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract the generated text
                if 'candidates' in result and len(result['candidates']) > 0:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        generated_text = candidate['content']['parts'][0]['text']
                        
                        if DEBUG_MODE:
                            print(f"Generated text length: {len(generated_text)} characters")
                        
                        return generated_text
                    else:
                        raise Exception("Invalid response format")
                else:
                    raise Exception("No candidates in response")
            else:
                error_msg = f"API request failed with status {response.status_code}"
                if DEBUG_MODE:
                    try:
                        error_detail = response.json()
                        print(f"Error details: {error_detail}")
                    except:
                        print(f"Error response: {response.text}")
                raise Exception(error_msg)
                
        except Exception as e:
            if DEBUG_MODE:
                print(f"Gemini API error: {e}")
            raise e
        finally:
            # Close response to free memory
            if 'response' in locals():
                response.close()
    
    def translate_text(self, text, target_language, source_language="auto"):
        """Translate text using Gemini API"""
        if source_language == "auto":
            prompt = f"Translate the following text to {target_language}. Only return the translation, no additional text:\n\n{text}"
        else:
            prompt = f"Translate the following text from {source_language} to {target_language}. Only return the translation, no additional text:\n\n{text}"
        
        return self.generate_content(prompt, temperature=0.3)
    
    def generate_quiz_question(self, topic, difficulty="medium", question_type="multiple_choice"):
        """Generate a quiz question on a specific topic"""
        prompt = f"""Create a {difficulty} difficulty {question_type} question about {topic}.
Format your response as JSON with the following structure:
{{
    "question": "The question text",
    "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
    "correct_answer": "A",
    "explanation": "Explanation of why this is correct"
}}

Only return the JSON, no additional text."""
        
        response = self.generate_content(prompt, temperature=0.7)
        
        try:
            # Parse the JSON response
            quiz_data = json.loads(response)
            return quiz_data
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "question": response[:200] + "..." if len(response) > 200 else response,
                "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                "correct_answer": "A",
                "explanation": "Unable to parse structured response"
            }
    
    def chat_response(self, message, context=None):
        """Generate a chat response"""
        if context:
            prompt = f"Context: {context}\n\nUser: {message}\n\nAssistant:"
        else:
            prompt = f"User: {message}\n\nAssistant:"
        
        return self.generate_content(prompt, temperature=0.8)
    
    def check_api_status(self):
        """Check if API is accessible"""
        try:
            test_response = self.generate_content("Hello", max_tokens=10)
            return True, "API is working"
        except Exception as e:
            return False, str(e)