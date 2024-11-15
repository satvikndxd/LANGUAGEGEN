"""Phonology generation module."""

from typing import List, Dict, Any
import random
import re

class Phoneme:
    """Represents a single sound unit in the language."""
    
    def __init__(self, symbol: str, features: Dict[str, Any]):
        self.symbol = symbol
        self.features = features
        
    def __str__(self) -> str:
        return self.symbol
        
    def __repr__(self) -> str:
        return f"Phoneme({self.symbol}, {self.features})"

class PhonologyGenerator:
    """Generates the sound system for the language."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config['phonology']
        self.consonants = self._create_phonemes(self.config['consonants'], 'consonant')
        self.vowels = self._create_phonemes(self.config['vowels'], 'vowel')
        self.syllable_structure = self.config['syllable_structure']
        self.max_syllables = self.config['max_syllables']
        
    def _create_phonemes(self, symbols: str, phoneme_type: str) -> List[Phoneme]:
        """Create Phoneme objects from symbols."""
        phonemes = []
        for symbol in symbols:
            features = self._get_phoneme_features(symbol, phoneme_type)
            phonemes.append(Phoneme(symbol, features))
        return phonemes
    
    def _get_phoneme_features(self, symbol: str, phoneme_type: str) -> Dict[str, Any]:
        """Define phonological features for a symbol."""
        if phoneme_type == 'consonant':
            # Simplified feature system for consonants
            features = {
                'type': 'consonant',
                'voiced': symbol in 'bdgmnŋzʒvðrl',
                'manner': self._get_manner(symbol),
                'place': self._get_place(symbol)
            }
        else:
            # Simplified feature system for vowels
            features = {
                'type': 'vowel',
                'height': self._get_vowel_height(symbol),
                'backness': self._get_vowel_backness(symbol),
                'rounded': symbol in 'ouɔʊ'
            }
        return features
    
    def _get_manner(self, symbol: str) -> str:
        """Determine manner of articulation."""
        if symbol in 'ptk':
            return 'stop'
        elif symbol in 'bdg':
            return 'voiced_stop'
        elif symbol in 'fvθð':
            return 'fricative'
        elif symbol in 'szʃʒ':
            return 'sibilant'
        elif symbol in 'mn':
            return 'nasal'
        elif symbol in 'l':
            return 'lateral'
        elif symbol in 'r':
            return 'rhotic'
        elif symbol in 'h':
            return 'glottal'
        return 'other'
    
    def _get_place(self, symbol: str) -> str:
        """Determine place of articulation."""
        if symbol in 'pbm':
            return 'labial'
        elif symbol in 'fv':
            return 'labiodental'
        elif symbol in 'θð':
            return 'dental'
        elif symbol in 'tdszln':
            return 'alveolar'
        elif symbol in 'ʃʒ':
            return 'postalveolar'
        elif symbol in 'kg':
            return 'velar'
        elif symbol in 'ŋ':
            return 'velar'
        elif symbol in 'h':
            return 'glottal'
        return 'other'
    
    def _get_vowel_height(self, symbol: str) -> str:
        """Determine vowel height."""
        if symbol in 'iɪu':
            return 'high'
        elif symbol in 'eɛoɔ':
            return 'mid'
        elif symbol in 'aæɑ':
            return 'low'
        elif symbol in 'ə':
            return 'mid'
        return 'other'
    
    def _get_vowel_backness(self, symbol: str) -> str:
        """Determine vowel backness."""
        if symbol in 'iɪeɛæ':
            return 'front'
        elif symbol in 'ə':
            return 'central'
        elif symbol in 'uoɔɑ':
            return 'back'
        return 'other'
    
    def generate_syllable(self) -> str:
        """Generate a single syllable based on the language's phonotactics."""
        pattern = random.choice(self.syllable_structure)
        syllable = ''
        
        for char in pattern:
            if char == 'C':
                syllable += random.choice(self.consonants).symbol
            elif char == 'V':
                syllable += random.choice(self.vowels).symbol
                
        return syllable
    
    def generate_word(self, min_syllables: int = 1) -> str:
        """Generate a word with the specified number of syllables."""
        num_syllables = random.randint(min_syllables, self.max_syllables)
        return ''.join(self.generate_syllable() for _ in range(num_syllables))
    
    def is_valid_word(self, word: str) -> bool:
        """Check if a word follows the language's phonological rules."""
        # Basic validation: check if word only contains valid phonemes
        valid_symbols = set(self.config['consonants'] + self.config['vowels'])
        return all(char in valid_symbols for char in word)
