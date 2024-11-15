from typing import Dict, List, Any, Optional
import numpy as np
from collections import defaultdict
from .base import LanguageComponent

class Word:
    """Represents a word in the generated language."""
    
    def __init__(self, 
                 form: str,
                 meaning: str,
                 pos: str,
                 morphology: Optional[Dict[str, str]] = None):
        self.form = form
        self.meaning = meaning
        self.pos = pos
        self.morphology = morphology or {}
        
    def __str__(self) -> str:
        return f"{self.form} ({self.pos}): {self.meaning}"

class VocabularyGenerator(LanguageComponent):
    """Generates vocabulary for the artificial language."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.consonants = list('ptkbdgmnŋszʃʒfvθðhrl')
        self.vowels = list('ieaouəɪɛæɑɔʊʌ')
        self.syllable_patterns = ['CV', 'CVC', 'V', 'VC']
        self.vocabulary = defaultdict(list)
        
    def generate_syllable(self) -> str:
        """Generate a single syllable based on phonological patterns."""
        pattern = np.random.choice(self.syllable_patterns)
        syllable = ''
        
        for char in pattern:
            if char == 'C':
                syllable += np.random.choice(self.consonants)
            elif char == 'V':
                syllable += np.random.choice(self.vowels)
                
        return syllable
    
    def generate_word_form(self, min_syllables: int = 1, max_syllables: int = 3) -> str:
        """Generate a word form using syllable patterns."""
        num_syllables = np.random.randint(min_syllables, max_syllables + 1)
        return ''.join(self.generate_syllable() for _ in range(num_syllables))
    
    def generate_basic_vocabulary(self, size: int = 1000) -> Dict[str, List[Word]]:
        """Generate basic vocabulary items across different parts of speech."""
        pos_distribution = {
            'NOUN': 0.4,
            'VERB': 0.3,
            'ADJ': 0.15,
            'ADV': 0.05,
            'DET': 0.05,
            'PREP': 0.05
        }
        
        vocabulary = defaultdict(list)
        used_forms = set()
        
        for pos, prob in pos_distribution.items():
            num_words = int(size * prob)
            
            for i in range(num_words):
                # Generate unique word form
                while True:
                    form = self.generate_word_form()
                    if form not in used_forms:
                        used_forms.add(form)
                        break
                
                # Create placeholder meaning (in practice, this would be more sophisticated)
                meaning = f"{pos.lower()}_meaning_{i}"
                
                word = Word(form=form,
                           meaning=meaning,
                           pos=pos)
                           
                vocabulary[pos].append(word)
        
        return vocabulary
    
    def apply_morphology(self, word: Word, morphology: Dict[str, List[str]]) -> List[Word]:
        """Apply morphological rules to generate word forms."""
        if word.pos not in morphology:
            return [word]
            
        variants = []
        base_form = word.form
        
        for feature, values in morphology[word.pos].items():
            for value in values:
                # Generate a simple suffix for demonstration
                suffix = self.generate_syllable()
                new_form = base_form + suffix
                
                variant = Word(
                    form=new_form,
                    meaning=word.meaning,
                    pos=word.pos,
                    morphology={feature: value}
                )
                variants.append(variant)
                
        return variants
    
    def generate(self) -> Dict[str, Any]:
        """Generate complete vocabulary for the language."""
        # Generate basic vocabulary
        basic_vocabulary = self.generate_basic_vocabulary()
        
        # Generate morphological variants
        morphology = {
            'NOUN': {
                'number': ['singular', 'plural'],
                'case': ['nominative', 'accusative']
            },
            'VERB': {
                'tense': ['present', 'past', 'future']
            }
        }
        
        expanded_vocabulary = defaultdict(list)
        
        for pos, words in basic_vocabulary.items():
            for word in words:
                variants = self.apply_morphology(word, morphology)
                expanded_vocabulary[pos].extend(variants)
        
        self.vocabulary = expanded_vocabulary
        return dict(expanded_vocabulary)
    
    def validate(self, vocabulary: Dict[str, List[Word]]) -> bool:
        """Validate the generated vocabulary."""
        if not vocabulary:
            return False
            
        # Check if we have words for each major part of speech
        required_pos = ['NOUN', 'VERB', 'ADJ']
        if not all(pos in vocabulary for pos in required_pos):
            return False
            
        # Check if words have valid forms
        for pos, words in vocabulary.items():
            if not words:  # Each POS should have at least one word
                return False
                
            for word in words:
                if not isinstance(word, Word):
                    return False
                if not word.form or not word.meaning:
                    return False
                    
        return True
