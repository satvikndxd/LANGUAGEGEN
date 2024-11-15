"""Configuration settings for language generation."""

from typing import Dict, Any
import yaml

DEFAULT_CONFIG = {
    'language': {
        'name': 'NewLang',
        'complexity': 'medium',  # simple, medium, complex
        'features': {
            'case_system': True,
            'gender': False,
            'number': True,
            'tense': True,
            'aspect': True,
            'mood': False
        }
    },
    'phonology': {
        'consonants': 'ptkbdgmnŋszʃʒfvθðhrl',
        'vowels': 'ieaouəɪɛæɑɔʊʌ',
        'syllable_structure': ['CV', 'CVC', 'V', 'VC'],
        'max_syllables': 3
    },
    'grammar': {
        'word_order': 'SVO',  # SVO, SOV, VSO
        'alignment': 'nominative-accusative',  # nominative-accusative, ergative-absolutive
        'morphology_type': 'fusional'  # isolating, agglutinative, fusional
    },
    'vocabulary': {
        'initial_size': 1000,
        'distribution': {
            'NOUN': 0.4,
            'VERB': 0.3,
            'ADJ': 0.15,
            'ADV': 0.05,
            'DET': 0.05,
            'PREP': 0.05
        }
    }
}

def load_config(config_path: str = None) -> Dict[str, Any]:
    """Load configuration from file or return default config."""
    if config_path:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            # Merge with defaults for any missing values
            return {**DEFAULT_CONFIG, **config}
    return DEFAULT_CONFIG.copy()

def save_config(config: Dict[str, Any], config_path: str) -> None:
    """Save configuration to file."""
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
