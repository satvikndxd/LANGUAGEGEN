"""Test cases for the phonology module."""

import pytest
from language_core.config import load_config
from language_core.phonology import PhonologyGenerator, Phoneme

@pytest.fixture
def config():
    return load_config()

@pytest.fixture
def phonology(config):
    return PhonologyGenerator(config)

def test_phoneme_creation():
    """Test creation of Phoneme objects."""
    p = Phoneme('p', {'type': 'consonant', 'voiced': False})
    assert str(p) == 'p'
    assert p.features['type'] == 'consonant'
    assert p.features['voiced'] is False

def test_phonology_initialization(phonology):
    """Test initialization of PhonologyGenerator."""
    assert len(phonology.consonants) > 0
    assert len(phonology.vowels) > 0
    assert len(phonology.syllable_structure) > 0
    assert phonology.max_syllables > 0

def test_syllable_generation(phonology):
    """Test syllable generation."""
    syllable = phonology.generate_syllable()
    assert len(syllable) > 0
    assert phonology.is_valid_word(syllable)

def test_word_generation(phonology):
    """Test word generation."""
    word = phonology.generate_word()
    assert len(word) > 0
    assert phonology.is_valid_word(word)

def test_word_validation(phonology):
    """Test word validation."""
    # Valid word
    assert phonology.is_valid_word('pat')
    # Invalid word (contains invalid symbol)
    assert not phonology.is_valid_word('pat!')
