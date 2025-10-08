# models/recommendation_engine.py
"""
Recommendation engine for alumni-student matching
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

class RecommendationEngine:
    """Generate recommendations for student-alumni matching"""
    
    def __init__(self, profile_processor=None):
        """
        Initialize recommendation engine
        
        Args:
            profile_processor: ProfileProcessor instance
        """
        self.profile_processor = profile_processor
        self.alumni_df = None
        self.student_df = None
        self.similarity_scores = {}
        
    def fit(self, alumni_df: pd.DataFrame, student_df: pd.DataFrame):
        """
        Fit the recommendation engine with data
        
        Args:
            alumni_df: DataFrame with alumni data
            student_df: DataFrame with student data
        """
        self.alumni_df = alumni_df
        self.student_df = student_df
        
    def get_recommendations(self, student_id: str, top_n: int = 3) -> List[Dict]:
        """
        Get top N alumni recommendations for a student
        
        Args:
            student_id: Student ID
            top_n: Number of recommendations
            
        Returns:
            List of recommendation dictionaries
        """
        student_idx = self.student_df[self.student_df['id'] == student_id].index[0]
        student_data = self.student_df.iloc[student_idx]
        
        # Calculate similarity scores for all alumni
        scores = []
        
        for idx, alumni in self.alumni_df.iterrows():
            score_details = self._calculate_match_score(student_data, alumni)
            scores.append({
                'alumni_id': alumni['id'],
                'alumni_name': alumni['name'],
                'total_score': score_details['total_score'],
                'score_breakdown': score_details
            })
        
        # Sort by total score and get top N
        scores.sort(key=lambda x: x['total_score'], reverse=True)
        top_recommendations = scores[:top_n]
        
        # Add detailed alumni information
        recommendations = []
        for rec in top_recommendations:
            alumni_data = self.alumni_df[self.alumni_df['id'] == rec['alumni_id']].iloc[0]
            recommendations.append({
                'alumni': alumni_data.to_dict(),
                'match_score': rec['total_score'],
                'score_breakdown': rec['score_breakdown']
            })
        
        return recommendations
    
    def _calculate_match_score(self, student: pd.Series, alumni: pd.Series) -> Dict:
        """
        Calculate detailed match score between student and alumni
        
        Args:
            student: Student data
            alumni: Alumni data
            
        Returns:
            Dictionary with score breakdown
        """
        scores = {}
        
        # 1. Semantic similarity using embeddings (40% weight)
        if self.profile_processor and self.profile_processor.student_embeddings is not None:
            student_idx = self.student_df[self.student_df['id'] == student['id']].index[0]
            alumni_idx = self.alumni_df[self.alumni_df['id'] == alumni['id']].index[0]
            
            student_emb = self.profile_processor.student_embeddings[student_idx].reshape(1, -1)
            alumni_emb = self.profile_processor.alumni_embeddings[alumni_idx].reshape(1, -1)
            
            semantic_score = cosine_similarity(student_emb, alumni_emb)[0][0]
            scores['semantic_similarity'] = float(semantic_score) * 0.4
        else:
            scores['semantic_similarity'] = 0.2
        
        # 2. Skill overlap (30% weight)
        student_skills = set([s.lower() for s in student['skills']])
        alumni_skills = set([s.lower() for s in alumni['skills']])
        
        if student_skills and alumni_skills:
            skill_overlap = len(student_skills.intersection(alumni_skills)) / len(student_skills.union(alumni_skills))
            scores['skill_match'] = skill_overlap * 0.3
        else:
            scores['skill_match'] = 0.0
        
        # 3. Industry/Interest alignment (20% weight)
        industry_match = 0.0
        student_interests = set([i.lower() for i in student['interests']])
        alumni_interests = set([i.lower() for i in alumni['interests']])
        
        # Check industry preference
        if student['preferred_industry'].lower() in alumni['industry'].lower():
            industry_match = 0.15
        
        # Check interest overlap
        if student_interests and alumni_interests:
            interest_overlap = len(student_interests.intersection(alumni_interests)) / max(len(student_interests), 1)
            industry_match += interest_overlap * 0.05
        
        scores['industry_interest'] = industry_match
        
        # 4. Educational background (10% weight)
        edu_score = 0.0
        if student['university'].lower() == alumni['university'].lower():
            edu_score = 0.08  # Same university
        if student['degree'].lower() in alumni['degree'].lower():
            edu_score += 0.02  # Similar degree
        
        scores['education_match'] = edu_score
        
        # Calculate total score
        scores['total_score'] = sum([
            scores['semantic_similarity'],
            scores['skill_match'],
            scores['industry_interest'],
            scores['education_match']
        ])
        
        return scores
    
    def get_match_explanation(self, student_id: str, alumni_id: str) -> Dict:
        """
        Get detailed explanation for a specific match
        
        Args:
            student_id: Student ID
            alumni_id: Alumni ID
            
        Returns:
            Dictionary with match explanation
        """
        student = self.student_df[self.student_df['id'] == student_id].iloc[0]
        alumni = self.alumni_df[self.alumni_df['id'] == alumni_id].iloc[0]
        
        score_details = self._calculate_match_score(student, alumni)
        
        # Generate human-readable explanations
        explanations = []
        
        # Skill matches
        student_skills = set([s.lower() for s in student['skills']])
        alumni_skills = set([s.lower() for s in alumni['skills']])
        common_skills = student_skills.intersection(alumni_skills)
        
        if common_skills:
            explanations.append(f"Shared skills: {', '.join(common_skills)}")
        
        # Industry alignment
        if student['preferred_industry'].lower() in alumni['industry'].lower():
            explanations.append(f"Works in your preferred industry: {alumni['industry']}")
        
        # Interest alignment
        student_interests = set([i.lower() for i in student['interests']])
        alumni_interests = set([i.lower() for i in alumni['interests']])
        common_interests = student_interests.intersection(alumni_interests)
        
        if common_interests:
            explanations.append(f"Common interests: {', '.join(common_interests)}")
        
        # Educational background
        if student['university'].lower() == alumni['university'].lower():
            explanations.append(f"Alumni from {alumni['university']}")
        
        # Mentoring alignment
        student_needs = set([n.lower() for n in student['looking_for']])
        alumni_offers = set([m.lower() for m in alumni['mentoring_areas']])
        matching_areas = student_needs.intersection(alumni_offers)
        
        if matching_areas:
            explanations.append(f"Can help with: {', '.join(matching_areas)}")
        
        return {
            'score_breakdown': score_details,
            'explanations': explanations,
            'total_score': score_details['total_score']
        }