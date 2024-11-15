from typing import Dict, List, Any, Tuple
import numpy as np
from .base import LanguageComponent

class GrammarRule:
    """Represents a single grammar rule in the generated language."""
    
    def __init__(self, name: str, pattern: List[str], probability: float = 1.0):
        self.name = name
        self.pattern = pattern
        self.probability = probability
        
    def __str__(self) -> str:
        return f"{self.name} -> {' '.join(self.pattern)} ({self.probability})"

class GrammarGenerator(LanguageComponent):
    """Generates grammar rules for the artificial language."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.parts_of_speech = ['NOUN', 'VERB', 'ADJ', 'ADV', 'DET', 'PREP']
        self.rules = []
        self.word_order_patterns = []
        
    def generate_word_order(self) -> List[str]:
        """Generate basic word order patterns (SVO, SOV, etc.)."""
        possible_orders = [
            ['SUBJ', 'VERB', 'OBJ'],  # SVO
            ['SUBJ', 'OBJ', 'VERB'],  # SOV
            ['VERB', 'SUBJ', 'OBJ'],  # VSO
        ]
        return np.random.choice(possible_orders)
    
    def generate_phrase_structure(self) -> List[GrammarRule]:
        """Generate phrase structure rules."""
        rules = []
        
        # Noun phrase rules
        np_rules = [
            GrammarRule('NP', ['DET', 'NOUN']),
            GrammarRule('NP', ['DET', 'ADJ', 'NOUN']),
            GrammarRule('NP', ['NOUN']),
        ]
        
        # Verb phrase rules
        vp_rules = [
            GrammarRule('VP', ['VERB']),
            GrammarRule('VP', ['VERB', 'NP']),
            GrammarRule('VP', ['VERB', 'ADV']),
        ]
        
        # Sentence rules
        basic_order = self.generate_word_order()
        s_rules = [
            GrammarRule('S', ['NP', 'VP']),
            GrammarRule('S', basic_order),
        ]
        
        rules.extend(np_rules + vp_rules + s_rules)
        return rules
    
    def generate_morphology(self) -> Dict[str, List[str]]:
        """Generate morphological rules for the language."""
        morphology = {
            'NOUN': {
                'number': ['singular', 'plural'],
                'case': ['nominative', 'accusative', 'genitive'],
            },
            'VERB': {
                'tense': ['present', 'past', 'future'],
                'aspect': ['simple', 'continuous', 'perfect'],
                'person': ['1st', '2nd', '3rd'],
            },
            'ADJ': {
                'degree': ['positive', 'comparative', 'superlative'],
            }
        }
        return morphology
    
    def generate(self) -> Dict[str, Any]:
        """Generate complete grammar rules for the language."""
        grammar = {
            'word_order': self.generate_word_order(),
            'phrase_structure': self.generate_phrase_structure(),
            'morphology': self.generate_morphology(),
        }
        
        self.rules = grammar
        return grammar
    
    def validate(self, grammar: Dict[str, Any]) -> bool:
        """Validate the coherence of generated grammar rules."""
        if not grammar:
            return False
            
        required_keys = ['word_order', 'phrase_structure', 'morphology']
        if not all(key in grammar for key in required_keys):
            return False
            
        # Validate word order
        if not isinstance(grammar['word_order'], list):
            return False
            
        # Validate phrase structure
        if not isinstance(grammar['phrase_structure'], list):
            return False
            
        # Validate morphology
        if not isinstance(grammar['morphology'], dict):
            return False
            
        return True
