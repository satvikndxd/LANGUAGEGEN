from language_core.base import LanguageGenerator
from language_core.grammar import GrammarGenerator
from language_core.vocabulary import VocabularyGenerator

def main():
    # Configuration for the language generation
    config = {
        'vocabulary_size': 1000,
        'min_syllables': 1,
        'max_syllables': 3,
        'complexity': 'medium'  # Can be 'simple', 'medium', or 'complex'
    }
    
    # Create the language generator
    lang_gen = LanguageGenerator(config)
    
    # Add components
    grammar_gen = GrammarGenerator(config)
    vocab_gen = VocabularyGenerator(config)
    
    lang_gen.add_component('grammar', grammar_gen)
    lang_gen.add_component('vocabulary', vocab_gen)
    
    # Generate the language
    language = lang_gen.generate_language()
    
    # Print some examples
    print("Generated Language Example:")
    print("\nGrammar Rules:")
    for rule in language['grammar']['phrase_structure']:
        print(f"- {rule}")
        
    print("\nMorphological Rules:")
    for pos, features in language['grammar']['morphology'].items():
        print(f"\n{pos}:")
        for feature, values in features.items():
            print(f"  {feature}: {', '.join(values)}")
            
    print("\nSample Vocabulary:")
    for pos, words in language['vocabulary'].items():
        print(f"\n{pos} examples:")
        # Print first 5 words of each type
        for word in words[:5]:
            print(f"- {word}")

if __name__ == "__main__":
    main()
