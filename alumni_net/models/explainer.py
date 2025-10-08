# models/explainer.py
"""
Explainability module for recommendations
(Note: This is now integrated into RecommendationEngine.get_match_explanation)
"""

import pandas as pd
from typing import Dict, List

class Explainer:
    """Provides explanations for recommendation matches"""
    
    def __init__(self, alumni_df: pd.DataFrame, student_df: pd.DataFrame):
        """
        Initialize explainer with data
        
        Args:
            alumni_df: Alumni DataFrame
            student_df: Student DataFrame
        """
        self.alumni_df = alumni_df
        self.student_df = student_df
    
    def get_explanation(self, student_id: str, alumni_id: str) -> str:
        """
        Generate a simple explanation for why an alumni matches a student
        
        Args:
            student_id: Student ID
            alumni_id: Alumni ID
            
        Returns:
            Human-readable explanation string
        """
        student = self.student_df[self.student_df['id'] == student_id].iloc[0]
        alumni = self.alumni_df[self.alumni_df['id'] == alumni_id].iloc[0]
        
        explanations = []
        
        # Check skill overlap
        student_skills = set([s.lower() for s in student['skills']])
        alumni_skills = set([s.lower() for s in alumni['skills']])
        common_skills = student_skills.intersection(alumni_skills)
        
        if common_skills:
            explanations.append(f"Shared skills: {', '.join(list(common_skills)[:3])}")
        
        # Check interest overlap
        student_interests = set([i.lower() for i in student['interests']])
        alumni_interests = set([i.lower() for i in alumni['interests']])
        common_interests = student_interests.intersection(alumni_interests)
        
        if common_interests:
            explanations.append(f"Common interests: {', '.join(list(common_interests)[:3])}")
        
        # Check industry match
        if student['preferred_industry'].lower() in alumni['industry'].lower():
            explanations.append(f"Works in your preferred industry ({alumni['industry']})")
        
        # Check university match
        if student['university'].lower() == alumni['university'].lower():
            explanations.append(f"Alumni from {alumni['university']}")
        
        # Check mentoring alignment
        student_needs = set([n.lower() for n in student['looking_for']])
        alumni_offers = set([m.lower() for m in alumni['mentoring_areas']])
        matching_areas = student_needs.intersection(alumni_offers)
        
        if matching_areas:
            explanations.append(f"Can help with: {', '.join(list(matching_areas)[:2])}")
        
        if explanations:
            return " | ".join(explanations)
        else:
            return "General profile compatibility based on overall career goals and background"
    
    def get_detailed_explanation(self, student_id: str, alumni_id: str) -> Dict:
        """
        Generate detailed explanation with score components
        
        Args:
            student_id: Student ID
            alumni_id: Alumni ID
            
        Returns:
            Dictionary with detailed breakdown
        """
        student = self.student_df[self.student_df['id'] == student_id].iloc[0]
        alumni = self.alumni_df[self.alumni_df['id'] == alumni_id].iloc[0]
        
        result = {
            'student': {
                'name': student['name'],
                'skills': student['skills'],
                'interests': student['interests'],
                'goals': student['career_goals']
            },
            'alumni': {
                'name': alumni['name'],
                'position': alumni['current_position'],
                'company': alumni['company'],
                'skills': alumni['skills'],
                'interests': alumni['interests']
            },
            'matches': {
                'skills': list(set([s.lower() for s in student['skills']]).intersection(
                              set([s.lower() for s in alumni['skills']]))),
                'interests': list(set([i.lower() for i in student['interests']]).intersection(
                                 set([i.lower() for i in alumni['interests']]))),
                'university_match': student['university'].lower() == alumni['university'].lower()
            }
        }
        
        return result