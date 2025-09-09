"""
Chat Module for Raspberry Pi Pico W
Provides open chat functionality with Gemini API
"""

import time
from config import DEBUG_MODE


class ChatModule:
    def __init__(self, gemini_client, keyboard):
        self.gemini_client = gemini_client
        self.keyboard = keyboard
        self.conversation_history = []
        self.max_history_length = 10  # Limit to conserve memory
        self.session_start_time = time.time()
        
        if DEBUG_MODE:
            print("Chat module initialized")
    
    def add_to_history(self, user_message, ai_response):
        """Add conversation to history"""
        self.conversation_history.append({
            'user': user_message,
            'ai': ai_response,
            'timestamp': time.time()
        })
        
        # Keep only the last N conversations to save memory
        if len(self.conversation_history) > self.max_history_length:
            self.conversation_history = self.conversation_history[-self.max_history_length:]
    
    def get_context(self):
        """Get conversation context for API"""
        if not self.conversation_history:
            return None
        
        # Build context from recent conversations
        context_parts = []
        for conv in self.conversation_history[-3:]:  # Last 3 conversations
            context_parts.append(f"User: {conv['user']}")
            context_parts.append(f"Assistant: {conv['ai']}")
        
        return "\n".join(context_parts)
    
    def format_ai_response(self, response):
        """Format AI response for better display"""
        # Simple text wrapping for better readability
        max_width = 60
        words = response.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_width:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(" ".join(current_line))
        
        return "\n".join(lines)
    
    def display_conversation_history(self):
        """Display recent conversation history"""
        if not self.conversation_history:
            print("No conversation history yet.")
            return
        
        print("\n=== Recent Conversation ===")
        for i, conv in enumerate(self.conversation_history[-5:], 1):
            timestamp = time.localtime(conv['timestamp'])
            time_str = f"{timestamp.tm_hour:02d}:{timestamp.tm_min:02d}"
            
            print(f"\n[{time_str}] You:")
            print(f"  {conv['user']}")
            print(f"[{time_str}] Gemini:")
            print(f"  {self.format_ai_response(conv['ai'])}")
    
    def get_chat_statistics(self):
        """Get chat session statistics"""
        session_duration = time.time() - self.session_start_time
        hours = int(session_duration // 3600)
        minutes = int((session_duration % 3600) // 60)
        
        return {
            'messages_sent': len(self.conversation_history),
            'session_duration_hours': hours,
            'session_duration_minutes': minutes,
            'average_response_length': (
                sum(len(conv['ai']) for conv in self.conversation_history) / 
                len(self.conversation_history)
            ) if self.conversation_history else 0
        }
    
    def simple_chat(self):
        """Simple chat mode without context"""
        print("\n=== Simple Chat Mode ===")
        print("Chat with Gemini AI (type 'quit' to exit)")
        print("Each message is independent - no conversation memory")
        
        while True:
            user_input = self.keyboard.get_input_prompt("\nYou: ")
            
            if user_input.lower().strip() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
            
            if not user_input.strip():
                print("Please enter a message.")
                continue
            
            try:
                print("Gemini is thinking...")
                response = self.gemini_client.chat_response(user_input)
                
                print(f"\nGemini:")
                print(self.format_ai_response(response))
                
                # Add to history (for statistics, even in simple mode)
                self.add_to_history(user_input, response)
                
            except Exception as e:
                print(f"Sorry, I encountered an error: {e}")
                print("Please try again.")
    
    def contextual_chat(self):
        """Contextual chat mode with conversation memory"""
        print("\n=== Contextual Chat Mode ===")
        print("Chat with Gemini AI with conversation memory")
        print("Type 'quit' to exit, 'clear' to clear history, 'history' to see recent messages")
        
        while True:
            user_input = self.keyboard.get_input_prompt("\nYou: ")
            
            if user_input.lower().strip() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
            elif user_input.lower().strip() == 'clear':
                self.conversation_history = []
                print("Conversation history cleared.")
                continue
            elif user_input.lower().strip() == 'history':
                self.display_conversation_history()
                continue
            
            if not user_input.strip():
                print("Please enter a message.")
                continue
            
            try:
                print("Gemini is thinking...")
                context = self.get_context()
                response = self.gemini_client.chat_response(user_input, context)
                
                print(f"\nGemini:")
                print(self.format_ai_response(response))
                
                # Add to history
                self.add_to_history(user_input, response)
                
            except Exception as e:
                print(f"Sorry, I encountered an error: {e}")
                print("Please try again.")
    
    def quick_questions(self):
        """Quick questions mode with predefined prompts"""
        print("\n=== Quick Questions Mode ===")
        
        quick_prompts = {
            '1': "Tell me an interesting fact",
            '2': "Give me a creative writing prompt",
            '3': "Explain a scientific concept simply",
            '4': "Suggest a fun activity",
            '5': "Share a motivational quote",
            '6': "Help me solve a problem",
            '7': "Tell me about today's technology",
            '8': "Recommend something to learn",
            '9': "Create a short story",
            '10': "Ask me a philosophical question"
        }
        
        while True:
            print("\nQuick question options:")
            for key, prompt in quick_prompts.items():
                print(f"{key}. {prompt}")
            print("0. Back to chat menu")
            print("C. Custom question")
            
            choice = self.keyboard.get_input_prompt("Select option: ")
            
            if choice == '0':
                break
            elif choice.upper() == 'C':
                custom_prompt = self.keyboard.get_input_prompt("Enter your question: ")
                if custom_prompt.strip():
                    try:
                        print("Gemini is thinking...")
                        response = self.gemini_client.chat_response(custom_prompt)
                        print(f"\nGemini:")
                        print(self.format_ai_response(response))
                        self.add_to_history(custom_prompt, response)
                    except Exception as e:
                        print(f"Error: {e}")
            elif choice in quick_prompts:
                try:
                    print("Gemini is thinking...")
                    response = self.gemini_client.chat_response(quick_prompts[choice])
                    print(f"\nGemini:")
                    print(self.format_ai_response(response))
                    self.add_to_history(quick_prompts[choice], response)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Invalid option.")
    
    def chat_settings(self):
        """Chat settings and information"""
        print("\n=== Chat Settings ===")
        
        while True:
            stats = self.get_chat_statistics()
            
            print(f"\nSession Statistics:")
            print(f"Messages sent: {stats['messages_sent']}")
            print(f"Session duration: {stats['session_duration_hours']}h {stats['session_duration_minutes']}m")
            print(f"Average response length: {stats['average_response_length']:.0f} characters")
            print(f"Memory limit: {self.max_history_length} conversations")
            
            print(f"\nOptions:")
            print("1. View conversation history")
            print("2. Clear conversation history")
            print("3. Change memory limit")
            print("4. Export conversation")
            print("0. Back to chat menu")
            
            choice = self.keyboard.get_input_prompt("Select option: ")
            
            if choice == '0':
                break
            elif choice == '1':
                self.display_conversation_history()
            elif choice == '2':
                confirm = self.keyboard.get_input_prompt(
                    "Clear conversation history? (y/n): "
                ).lower()
                if confirm == 'y':
                    self.conversation_history = []
                    print("History cleared.")
            elif choice == '3':
                try:
                    new_limit = int(self.keyboard.get_input_prompt(
                        f"Enter new memory limit (1-20, current: {self.max_history_length}): "
                    ))
                    if 1 <= new_limit <= 20:
                        self.max_history_length = new_limit
                        print(f"Memory limit set to {new_limit}")
                    else:
                        print("Please enter a number between 1 and 20.")
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == '4':
                self.export_conversation()
            else:
                print("Invalid option.")
    
    def export_conversation(self):
        """Export conversation to text format"""
        if not self.conversation_history:
            print("No conversation to export.")
            return
        
        print("\n=== Conversation Export ===")
        export_text = []
        export_text.append(f"Gemini Chat Session Export")
        export_text.append(f"Session started: {time.ctime(self.session_start_time)}")
        export_text.append(f"Total messages: {len(self.conversation_history)}")
        export_text.append("=" * 50)
        
        for i, conv in enumerate(self.conversation_history, 1):
            timestamp = time.ctime(conv['timestamp'])
            export_text.append(f"\nMessage {i} - {timestamp}")
            export_text.append(f"You: {conv['user']}")
            export_text.append(f"Gemini: {conv['ai']}")
            export_text.append("-" * 30)
        
        # In a real implementation, this would save to a file
        # For now, just display the export
        print("\nConversation export (first 500 characters):")
        full_export = "\n".join(export_text)
        print(full_export[:500] + "..." if len(full_export) > 500 else full_export)
        print(f"\nFull export: {len(full_export)} characters")
    
    def run(self):
        """Run the chat module"""
        while True:
            print("\n=== Chat with Gemini ===")
            print("1. Simple Chat (no memory)")
            print("2. Contextual Chat (with memory)")
            print("3. Quick Questions")
            print("4. Chat Settings")
            print("0. Back to main menu")
            
            choice = self.keyboard.get_input_prompt("Select option: ")
            
            if choice == '0':
                break
            elif choice == '1':
                self.simple_chat()
            elif choice == '2':
                self.contextual_chat()
            elif choice == '3':
                self.quick_questions()
            elif choice == '4':
                self.chat_settings()
            else:
                print("Invalid option. Please try again.")