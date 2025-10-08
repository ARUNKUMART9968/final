# models/profile_processor.py
"""
NLP processing for alumni and student profiles
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
import spacy
import warnings
warnings.filterwarnings('ignore')

class ProfileProcessor:
    """Process profiles using NLP techniques"""
    
    def __init__(self):
        """Initialize NLP models"""
        print("Initializing NLP models...")
        
        # Load spaCy model for NER and text processing
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("SpaCy model not found. Using basic processing.")
            self.nlp = None
        
        # Initialize sentence transformer for semantic embeddings
        print("Loading sentence transformer model...")
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        self.alumni_embeddings = None
        self.student_embeddings = None
        self.alumni_tfidf = None
        self.student_tfidf = None
        
    def process_profiles(self, alumni_df: pd.DataFrame, student_df: pd.DataFrame):
        """
        Process all profiles and create embeddings
        
        Args:
            alumni_df: DataFrame with alumni data
            student_df: DataFrame with student data
        """
        print("Processing alumni profiles...")
        self.alumni_embeddings = self._create_embeddings(alumni_df['profile_text'].tolist())
        
        print("Processing student profiles...")
        self.student_embeddings = self._create_embeddings(student_df['profile_text'].tolist())
        
        # Create TF-IDF features
        print("Creating TF-IDF features...")
        all_texts = alumni_df['profile_text'].tolist() + student_df['profile_text'].tolist()
        self.tfidf_vectorizer.fit(all_texts)
        
        self.alumni_tfidf = self.tfidf_vectorizer.transform(alumni_df['profile_text'])
        self.student_tfidf = self.tfidf_vectorizer.transform(student_df['profile_text'])
        
    def _create_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Create sentence embeddings for texts
        
        Args:
            texts: List of text strings
            
        Returns:
            numpy array of embeddings
        """
        embeddings = self.sentence_model.encode(texts, show_progress_bar=False)
        return embeddings
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract skills from text using NER and pattern matching
        
        Args:
            text: Input text
            
        Returns:
            List of extracted skills
        """
        skills = []
        
        # Common technical skills patterns
        tech_skills = [
            'python', 'java', 'javascript', 'c++', 'sql', 'r', 'scala',
            'machine learning', 'deep learning', 'data science', 'ai',
            'cloud computing', 'docker', 'kubernetes', 'aws', 'azure',
            'react', 'node.js', 'angular', 'vue.js', 'tensorflow',
            'pytorch', 'scikit-learn', 'pandas', 'numpy'
        ]
        
        text_lower = text.lower()
        for skill in tech_skills:
            if skill in text_lower:
                skills.append(skill)
        
        return list(set(skills))
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of entity types and values
        """
        entities = {
            'organizations': [],
            'locations': [],
            'persons': []
        }
        
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ == "ORG":
                    entities['organizations'].append(ent.text)
                elif ent.label_ == "LOC" or ent.label_ == "GPE":
                    entities['locations'].append(ent.text)
                elif ent.label_ == "PERSON":
                    entities['persons'].append(ent.text)
        
        return entities
    
    def calculate_skill_overlap(self, skills1: List[str], skills2: List[str]) -> float:
        """
        Calculate skill overlap between two skill lists
        
        Args:
            skills1: First skill list
            skills2: Second skill list
            
        Returns:
            Overlap score between 0 and 1
        """
        if not skills1 or not skills2:
            return 0.0
        
        set1 = set([s.lower() for s in skills1])
        set2 = set([s.lower() for s in skills2])
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    def get_profile_features(self, profile_text: str) -> Dict:
        """
        Extract comprehensive features from profile text
        
        Args:
            profile_text: Profile text
            
        Returns:
            Dictionary of extracted features
        """
        features = {
            'skills': self.extract_skills(profile_text),
            'entities': self.extract_entities(profile_text),
            'text_length': len(profile_text),
            'word_count': len(profile_text.split())
        }
        
        return features