"""Example script demonstrating word generation."""

from language_core.config import load_config
from language_core.phonology import PhonologyGenerator

def main():
    # Load default configuration
    config = load_config()
    
    # Initialize phonology generator
    phonology = PhonologyGenerator(config)
    
    print("AI Language Generator - Word Generation Example")
    print("=============================================")
    
    # Generate and display some syllables
    print("\nGenerated Syllables:")
    print("-------------------")
    for _ in range(5):
        syllable = phonology.generate_syllable()
        print(f"Syllable: {syllable}")
    
    # Generate and display some words
    print("\nGenerated Words:")
    print("---------------")
    for _ in range(10):
        word = phonology.generate_word()
        print(f"Word: {word}")
    
    # Demonstrate word validation
    print("\nWord Validation:")
    print("---------------")
    test_words = ['pat', 'kæt', 'dɔg', 'pat!', 'xyz']
    for word in test_words:
        valid = phonology.is_valid_word(word)
        print(f"Word '{word}' is {'valid' if valid else 'invalid'}")

if __name__ == "__main__":
    main()
