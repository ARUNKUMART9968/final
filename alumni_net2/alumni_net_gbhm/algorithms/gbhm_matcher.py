"""
Graph-Based Hierarchical Matching (GBHM) Algorithm
Core matching logic
"""

import pandas as pd
from typing import Dict, List, Tuple

class GBHMMatcher:
    """Graph-Based Hierarchical Matching Algorithm"""
    
    def __init__(self, alumni_df: pd.DataFrame, student_df: pd.DataFrame):
        """
        Initialize the matcher
        
        Args:
            alumni_df: DataFrame with alumni data
            student_df: DataFrame with student data
        """
        self.alumni_df = alumni_df
        self.student_df = student_df
        
        # Define weights for different connection types
        self.weights = {
            'university': 200,      # Exact match - strongest
            'industry': 160,        # Exact match
            'degree': 100,          # Exact match
            'skill': 90,            # Per skill match
            'interest': 70,         # Per interest match
            'mentoring': 50,        # Per mentoring area match
            'company': 50,          # Company match
            'availability': 50      # Alumni is available
        }
    
    def calculate_hierarchical_score(self, student: pd.Series, alumni: pd.Series) -> Dict:
        """
        Calculate hierarchical match score between student and alumni
        
        Args:
            student: Student data series
            alumni: Alumni data series
            
        Returns:
            Dictionary with score breakdown
        """
        score_breakdown = {}
        total_score = 0
        
        # ============ LEVEL 0: EXACT MATCHES (0 hops) ============
        
        # University match (strongest connection)
        if str(student['university']).lower() == str(alumni['university']).lower():
            score_breakdown['university'] = self.weights['university']
            total_score += score_breakdown['university']
        else:
            score_breakdown['university'] = 0
        
        # Industry match
        if str(student['preferred_industry']).lower() == str(alumni['industry']).lower():
            score_breakdown['industry'] = self.weights['industry']
            total_score += score_breakdown['industry']
        else:
            score_breakdown['industry'] = 0
        
        # Degree match
        if str(student['degree']).lower() == str(alumni['degree']).lower():
            score_breakdown['degree'] = self.weights['degree']
            total_score += score_breakdown['degree']
        else:
            score_breakdown['degree'] = 0
        
        # ============ LEVEL 1: SKILL BRIDGES (1 hop) ============
        
        # Skills matching
        student_skills = set([s.lower() for s in student['skills']])
        alumni_skills = set([s.lower() for s in alumni['skills']])
        common_skills = student_skills & alumni_skills
        
        skill_score = len(common_skills) * self.weights['skill']
        score_breakdown['skills'] = skill_score
        total_score += skill_score
        score_breakdown['common_skills'] = list(common_skills)
        
        # Interests matching
        student_interests = set([i.lower() for i in student['interests']])
        alumni_interests = set([i.lower() for i in alumni['interests']])
        common_interests = student_interests & alumni_interests
        
        interest_score = len(common_interests) * self.weights['interest']
        score_breakdown['interests'] = interest_score
        total_score += interest_score
        score_breakdown['common_interests'] = list(common_interests)
        
        # ============ LEVEL 2: MENTORING MATCH (2 hops) ============
        
        student_needs = set([n.lower() for n in student['looking_for']])
        alumni_offers = set([m.lower() for m in alumni['mentoring_areas']])
        matching_areas = student_needs & alumni_offers
        
        mentoring_score = len(matching_areas) * self.weights['mentoring']
        score_breakdown['mentoring'] = mentoring_score
        total_score += mentoring_score
        score_breakdown['matching_areas'] = list(matching_areas)
        
        # ============ ADDITIONAL FACTORS ============
        
        # Company match
        if 'company' in student.index and student.get('company'):
            if str(student['company']).lower() == str(alumni['company']).lower():
                score_breakdown['company'] = self.weights['company']
                total_score += score_breakdown['company']
            else:
                score_breakdown['company'] = 0
        else:
            score_breakdown['company'] = 0
        
        # Availability bonus
        if alumni['availability'] == 'Available':
            score_breakdown['availability'] = self.weights['availability']
            total_score += score_breakdown['availability']
        else:
            score_breakdown['availability'] = 0
        
        return {
            'total_score': total_score,
            'breakdown': score_breakdown
        }
    
    def get_recommendations(self, student_id: str, top_n: int = 5) -> List[Dict]:
        """
        Get top N alumni recommendations for a student
        
        Args:
            student_id: Student ID
            top_n: Number of recommendations
            
        Returns:
            List of recommendations with details
        """
        # Find student
        student_mask = self.student_df['id'] == student_id
        if not student_mask.any():
            raise ValueError(f"Student {student_id} not found")
        
        student = self.student_df[student_mask].iloc[0]
        
        # Calculate scores for all alumni
        recommendations = []
        
        for idx, alumni in self.alumni_df.iterrows():
            score_data = self.calculate_hierarchical_score(student, alumni)
            
            recommendation = {
                'alumni_id': alumni['id'],
                'alumni_name': alumni['name'],
                'current_position': alumni['current_position'],
                'company': alumni['company'],
                'industry': alumni['industry'],
                'location': alumni['location'],
                'email': alumni['email'],
                'years_experience': alumni['years_experience'],
                'availability': alumni['availability'],
                'skills': alumni['skills'],
                'interests': alumni['interests'],
                'mentoring_areas': alumni['mentoring_areas'],
                'bio': alumni['bio'],
                'total_score': score_data['total_score'],
                'score_breakdown': score_data['breakdown']
            }
            
            recommendations.append(recommendation)
        
        # Sort by total score
        recommendations.sort(key=lambda x: x['total_score'], reverse=True)
        
        # Return top N
        return recommendations[:top_n]
    
    def generate_explanation(self, student: pd.Series, alumni: Dict) -> str:
        """
        Generate human-readable explanation for a match
        
        Args:
            student: Student data
            alumni: Alumni recommendation dict
            
        Returns:
            Explanation string
        """
        reasons = []
        breakdown = alumni['score_breakdown']
        
        # University match
        if breakdown['university'] > 0:
            reasons.append(f"Alumni from {alumni['alumni_id']} - Same university as yours")
        
        # Industry match
        if breakdown['industry'] > 0:
            reasons.append(f"Works in your preferred industry: {alumni['industry']}")
        
        # Degree match
        if breakdown['degree'] > 0:
            reasons.append(f"Similar degree background: {alumni['alumni_id']}")
        
        # Skills
        if breakdown['common_skills']:
            skills_str = ', '.join(breakdown['common_skills'][:3])
            if len(breakdown['common_skills']) > 3:
                skills_str += f" and {len(breakdown['common_skills']) - 3} more"
            reasons.append(f"Shares your skills: {skills_str}")
        
        # Interests
        if breakdown['common_interests']:
            interests_str = ', '.join(breakdown['common_interests'])
            reasons.append(f"Common interests: {interests_str}")
        
        # Mentoring
        if breakdown['matching_areas']:
            areas_str = ', '.join(breakdown['matching_areas'][:2])
            reasons.append(f"Can help with: {areas_str}")
        
        # Availability
        if breakdown['availability'] > 0:
            reasons.append("Available for mentorship")
        
        return " | ".join(reasons) if reasons else "General profile compatibility"
    
    def display_detailed_recommendation(self, student_id: str, rank: int = 1):
        """
        Display detailed information about top recommendation
        
        Args:
            student_id: Student ID
            rank: Which recommendation to display (1 = top)
        """
        recommendations = self.get_recommendations(student_id, top_n=rank)
        if not recommendations or len(recommendations) < rank:
            print("Not enough recommendations")
            return
        
        rec = recommendations[rank - 1]
        
        print(f"\n{'='*80}")
        print(f"RECOMMENDATION #{rank}")
        print(f"{'='*80}\n")
        
        print(f"Name: {rec['alumni_name']}")
        print(f"Position: {rec['current_position']} at {rec['company']}")
        print(f"Industry: {rec['industry']}")
        print(f"Location: {rec['location']}")
        print(f"Years of Experience: {rec['years_experience']}")
        print(f"Availability: {rec['availability']}")
        print(f"Email: {rec['email']}\n")
        
        print(f"Skills: {', '.join(rec['skills'][:5])}")
        if len(rec['skills']) > 5:
            print(f"         ... and {len(rec['skills']) - 5} more")
        
        print(f"Interests: {', '.join(rec['interests'])}")
        print(f"Mentoring Areas: {', '.join(rec['mentoring_areas'])}\n")
        
        print(f"Bio: {rec['bio']}\n")
        
        # Score breakdown
        student = self.student_df[self.student_df['id'] == student_id].iloc[0]
        explanation = self.generate_explanation(student, rec)
        
        print(f"{'='*80}")
        print(f"MATCH SCORE: {rec['total_score']} points")
        print(f"{'='*80}\n")
        
        print("Score Breakdown:")
        for key, value in rec['score_breakdown'].items():
            if key not in ['common_skills', 'common_interests', 'matching_areas']:
                print(f"  • {key.capitalize()}: {value} points")
        
        print(f"\nWhy This Match:\n{explanation}\n")