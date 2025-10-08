# data/data_loader.py
"""
Data loading and preprocessing utilities
"""

import pandas as pd
from typing import List, Dict, Tuple
from .sample_data import ALUMNI_DATA, STUDENT_DATA

class DataLoader:
    """Handle data loading and basic preprocessing"""
    
    def __init__(self):
        self.alumni_df = None
        self.student_df = None
        
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load alumni and student data from static sources
        
        Returns:
            Tuple of (alumni_df, student_df)
        """
        # Convert to DataFrames
        self.alumni_df = pd.DataFrame(ALUMNI_DATA)
        self.student_df = pd.DataFrame(STUDENT_DATA)
        
        # Add profile text for NLP processing
        self.alumni_df['profile_text'] = self._create_alumni_profile_text()
        self.student_df['profile_text'] = self._create_student_profile_text()
        
        return self.alumni_df, self.student_df
    
    def _create_alumni_profile_text(self) -> pd.Series:
        """Create combined text from alumni profiles for NLP processing"""
        profile_texts = []
        
        for _, row in self.alumni_df.iterrows():
            text_parts = [
                f"Position: {row['current_position']}",
                f"Company: {row['company']}",
                f"Industry: {row['industry']}",
                f"Degree: {row['degree']}",
                f"University: {row['university']}",
                f"Skills: {', '.join(row['skills'])}",
                f"Bio: {row['bio']}",
                f"Interests: {', '.join(row['interests'])}",
                f"Mentoring: {', '.join(row['mentoring_areas'])}"
            ]
            profile_texts.append(' '.join(text_parts))
            
        return pd.Series(profile_texts)
    
    def _create_student_profile_text(self) -> pd.Series:
        """Create combined text from student profiles for NLP processing"""
        profile_texts = []
        
        for _, row in self.student_df.iterrows():
            text_parts = [
                f"Degree: {row['degree']}",
                f"University: {row['university']}",
                f"Skills: {', '.join(row['skills'])}",
                f"Interests: {', '.join(row['interests'])}",
                f"Career Goals: {row['career_goals']}",
                f"Looking For: {', '.join(row['looking_for'])}",
                f"Industry: {row['preferred_industry']}",
                f"Projects: {row['projects']}"
            ]
            profile_texts.append(' '.join(text_parts))
            
        return pd.Series(profile_texts)
    
    def get_alumni_by_id(self, alumni_id: str) -> Dict:
        """Get alumni details by ID"""
        if self.alumni_df is None:
            self.load_data()
        
        alumni = self.alumni_df[self.alumni_df['id'] == alumni_id]
        if len(alumni) > 0:
            return alumni.iloc[0].to_dict()
        return None
    
    def get_student_by_id(self, student_id: str) -> Dict:
        """Get student details by ID"""
        if self.student_df is None:
            self.load_data()
        
        student = self.student_df[self.student_df['id'] == student_id]
        if len(student) > 0:
            return student.iloc[0].to_dict()
        return None