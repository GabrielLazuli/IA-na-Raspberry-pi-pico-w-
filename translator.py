"""
Translation Module for Raspberry Pi Pico W
Provides text translation functionality using Gemini API
"""

from config import DEBUG_MODE


class Translator:
    def __init__(self, gemini_client, keyboard):
        self.gemini_client = gemini_client
        self.keyboard = keyboard
        self.supported_languages = {
            '1': 'English',
            '2': 'Spanish',
            '3': 'Portuguese',
            '4': 'French',
            '5': 'German',
            '6': 'Italian',
            '7': 'Chinese',
            '8': 'Japanese',
            '9': 'Korean',
            '10': 'Russian'
        }
        
        if DEBUG_MODE:
            print("Translator module initialized")
    
    def display_language_menu(self):
        """Display available languages"""
        print("\n=== Available Languages ===")
        for key, language in self.supported_languages.items():
            print(f"{key}. {language}")
        print("0. Back to main menu")
    
    def get_language_choice(self, prompt="Select language: "):
        """Get language choice from user"""
        while True:
            print(f"\n{prompt}")
            self.display_language_menu()
            
            choice = self.keyboard.get_input_prompt("Enter choice (0-10): ")
            
            if choice == '0':
                return None
            elif choice in self.supported_languages:
                return self.supported_languages[choice]
            else:
                print("Invalid choice. Please try again.")
    
    def translate_interactive(self):
        """Interactive translation mode"""
        print("\n=== Translation Module ===")
        print("Translate text between different languages")
        
        while True:
            # Get source language
            print("\nSelect source language (or Auto-detect):")
            print("A. Auto-detect")
            self.display_language_menu()
            
            source_choice = self.keyboard.get_input_prompt("Enter choice (A or 0-10): ").upper()
            
            if source_choice == '0':
                return
            elif source_choice == 'A':
                source_language = "auto"
            elif source_choice in self.supported_languages:
                source_language = self.supported_languages[source_choice]
            else:
                print("Invalid choice. Please try again.")
                continue
            
            # Get target language
            target_language = self.get_language_choice("Select target language:")
            if target_language is None:
                return
            
            # Get text to translate
            text_to_translate = self.keyboard.get_input_prompt(
                "Enter text to translate (type DONE when finished): "
            )
            
            if not text_to_translate.strip():
                print("No text entered.")
                continue
            
            # Perform translation
            try:
                print("\nTranslating...")
                
                if source_language == "auto":
                    translated_text = self.gemini_client.translate_text(
                        text_to_translate, 
                        target_language
                    )
                else:
                    translated_text = self.gemini_client.translate_text(
                        text_to_translate, 
                        target_language, 
                        source_language
                    )
                
                # Display results
                print(f"\n=== Translation Result ===")
                print(f"Original: {text_to_translate}")
                if source_language != "auto":
                    print(f"From: {source_language}")
                print(f"To: {target_language}")
                print(f"Translation: {translated_text}")
                
                # Ask if user wants to continue
                continue_choice = self.keyboard.get_input_prompt(
                    "\nTranslate another text? (y/n): "
                ).lower()
                
                if continue_choice != 'y':
                    break
                    
            except Exception as e:
                print(f"Translation error: {e}")
                print("Please check your connection and try again.")
    
    def translate_text(self, text, target_language, source_language="auto"):
        """Translate text directly (for use by other modules)"""
        try:
            return self.gemini_client.translate_text(text, target_language, source_language)
        except Exception as e:
            if DEBUG_MODE:
                print(f"Translation error: {e}")
            return f"Translation error: {e}"
    
    def quick_translate(self):
        """Quick translation with minimal input"""
        print("\n=== Quick Translate ===")
        
        # Common language pairs
        common_pairs = {
            '1': ('English', 'Spanish'),
            '2': ('English', 'Portuguese'),
            '3': ('English', 'French'),
            '4': ('Spanish', 'English'),
            '5': ('Portuguese', 'English'),
            '6': ('French', 'English')
        }
        
        print("Quick translation options:")
        for key, (source, target) in common_pairs.items():
            print(f"{key}. {source} → {target}")
        print("0. Custom translation")
        
        choice = self.keyboard.get_input_prompt("Select option: ")
        
        if choice == '0':
            self.translate_interactive()
        elif choice in common_pairs:
            source_lang, target_lang = common_pairs[choice]
            
            text = self.keyboard.get_input_prompt("Enter text to translate: ")
            if text.strip():
                try:
                    print("Translating...")
                    result = self.gemini_client.translate_text(text, target_lang, source_lang)
                    print(f"\n{source_lang}: {text}")
                    print(f"{target_lang}: {result}")
                except Exception as e:
                    print(f"Translation error: {e}")
        else:
            print("Invalid option selected.")
    
    def run(self):
        """Run the translation module"""
        while True:
            print("\n=== Translation Module ===")
            print("1. Interactive Translation")
            print("2. Quick Translate")
            print("0. Back to main menu")
            
            choice = self.keyboard.get_input_prompt("Select option: ")
            
            if choice == '0':
                break
            elif choice == '1':
                self.translate_interactive()
            elif choice == '2':
                self.quick_translate()
            else:
                print("Invalid option. Please try again.")