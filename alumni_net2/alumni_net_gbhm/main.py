"""
Main entry point for Graph-Based Hierarchical Matching (GBHM) System
Alumni Mentorship Recommendation Engine
"""

import pandas as pd
from data.alumni_data import ALUMNI_DATA
from data.student_data import STUDENT_DATA
from algorithms.gbhm_matcher import GBHMMatcher
from utils.helpers import (
    print_header, print_success, print_error, print_info,
    print_separator, load_data_to_dataframes, 
    display_student_profile, display_recommendations_summary
)

def display_interactive_menu():
    """Display interactive menu"""
    print_header("ALUMNI NETWORK - GBHM RECOMMENDATION SYSTEM", "=", 80)
    
    print("\n" + "="*80)
    print("AVAILABLE OPTIONS:".center(80))
    print("="*80 + "\n")
    
    print("1. Get recommendations for a specific student")
    print("2. View all students")
    print("3. View all alumni")
    print("4. Compare two alumni for a student")
    print("5. Detailed analysis of recommendations")
    print("0. Exit\n")
    
    return input("Enter your choice (0-5): ").strip()

def show_all_students(student_df):
    """Display all available students"""
    print_header("ALL AVAILABLE STUDENTS", "=", 80)
    
    for idx, student in student_df.iterrows():
        print(f"\n{idx+1}. {student['name']} (ID: {student['id']})")
        print(f"   University: {student['university']}")
        print(f"   Degree: {student['degree']}")
        print(f"   Career Goals: {student['career_goals'][:60]}...")
    
    print_separator()

def show_all_alumni(alumni_df):
    """Display all available alumni"""
    print_header("ALL AVAILABLE ALUMNI", "=", 80)
    
    for idx, alumni in alumni_df.iterrows():
        print(f"\n{idx+1}. {alumni['name']} (ID: {alumni['id']})")
        print(f"   Position: {alumni['current_position']} at {alumni['company']}")
        print(f"   University: {alumni['university']}")
        print(f"   Industry: {alumni['industry']}")
        print(f"   Availability: {alumni['availability']}")
    
    print_separator()

def get_student_recommendations(matcher, student_df, alumni_df):
    """Get recommendations for selected student"""
    
    print_header("STUDENT SELECTION", "=", 80)
    
    # Show all students
    for idx, student in student_df.iterrows():
        print(f"{idx+1}. {student['name']} (ID: {student['id']})")
    
    print()
    student_choice = input("Select student number: ").strip()
    
    try:
        student_idx = int(student_choice) - 1
        if student_idx < 0 or student_idx >= len(student_df):
            print_error("Invalid selection!")
            return
        
        student_id = student_df.iloc[student_idx]['id']
        student = student_df.iloc[student_idx]
        
        # Display student profile
        display_student_profile(student)
        
        # Get number of recommendations
        num_recs = input("\nHow many recommendations do you want? (1-5): ").strip()
        try:
            num_recs = int(num_recs)
            num_recs = min(max(1, num_recs), len(alumni_df))
        except:
            num_recs = 3
        
        # Get recommendations
        print_info("Calculating recommendations...")
        recommendations = matcher.get_recommendations(student_id, top_n=num_recs)
        
        # Display summary
        display_recommendations_summary(recommendations, count=num_recs)
        
        # Show detailed recommendations
        detail_choice = input("\nDo you want to see detailed information? (y/n): ").strip().lower()
        
        if detail_choice == 'y':
            for i in range(1, min(num_recs + 1, 4)):
                if i <= len(recommendations):
                    print_header(f"RECOMMENDATION #{i} - DETAILED VIEW", "-", 80)
                    
                    rec = recommendations[i-1]
                    
                    print(f"Name: {rec['alumni_name']}")
                    print(f"Position: {rec['current_position']}")
                    print(f"Company: {rec['company']}")
                    print(f"Industry: {rec['industry']}")
                    print(f"Location: {rec['location']}")
                    print(f"Years of Experience: {rec['years_experience']}")
                    print(f"Availability: {rec['availability']}")
                    print(f"Email: {rec['email']}\n")
                    
                    print("Skills:")
                    for skill in rec['skills']:
                        print(f"  • {skill}")
                    
                    print("\nInterests:")
                    for interest in rec['interests']:
                        print(f"  • {interest}")
                    
                    print("\nMentoring Areas:")
                    for area in rec['mentoring_areas']:
                        print(f"  • {area}")
                    
                    print(f"\nBio: {rec['bio']}\n")
                    
                    print(f"{'='*80}")
                    print(f"MATCH SCORE: {rec['total_score']} points")
                    print(f"{'='*80}\n")
                    
                    print("Score Breakdown:")
                    breakdown = rec['score_breakdown']
                    for key, value in breakdown.items():
                        if key not in ['common_skills', 'common_interests', 'matching_areas']:
                            if value > 0:
                                print(f"  ✓ {key.capitalize()}: {value} points")
                    
                    # Explanation
                    explanation = matcher.generate_explanation(student, rec)
                    print(f"\nWhy This Match:")
                    for reason in explanation.split(" | "):
                        print(f"  ✓ {reason}")
                    
                    print_separator("-")
    
    except Exception as e:
        print_error(f"Error: {str(e)}")

def compare_alumni(matcher, student_df, alumni_df):
    """Compare two alumni for a student"""
    
    print_header("COMPARE TWO ALUMNI", "=", 80)
    
    # Select student
    for idx, student in student_df.iterrows():
        print(f"{idx+1}. {student['name']}")
    
    student_choice = int(input("\nSelect student number: ").strip()) - 1
    student_id = student_df.iloc[student_choice]['id']
    student = student_df.iloc[student_choice]
    
    # Get recommendations
    recommendations = matcher.get_recommendations(student_id, top_n=len(alumni_df))
    
    # Select two alumni
    print("\nAvailable Alumni:")
    for idx, rec in enumerate(recommendations):
        print(f"{idx+1}. {rec['alumni_name']} - Score: {rec['total_score']}")
    
    alumni1_choice = int(input("\nSelect first alumni number: ").strip()) - 1
    alumni2_choice = int(input("Select second alumni number: ").strip()) - 1
    
    rec1 = recommendations[alumni1_choice]
    rec2 = recommendations[alumni2_choice]
    
    print_header("ALUMNI COMPARISON", "=", 80)
    
    print(f"\n{'ATTRIBUTE':<30} {'ALUMNI 1':<25} {'ALUMNI 2':<25}")
    print("-" * 80)
    
    print(f"{'Name':<30} {rec1['alumni_name']:<25} {rec2['alumni_name']:<25}")
    print(f"{'Position':<30} {rec1['current_position']:<25} {rec2['current_position']:<25}")
    print(f"{'Company':<30} {rec1['company']:<25} {rec2['company']:<25}")
    print(f"{'Industry':<30} {rec1['industry']:<25} {rec2['industry']:<25}")
    print(f"{'Years Experience':<30} {str(rec1['years_experience']):<25} {str(rec2['years_experience']):<25}")
    print(f"{'Match Score':<30} {str(rec1['total_score']):<25} {str(rec2['total_score']):<25}")
    print(f"{'Availability':<30} {rec1['availability']:<25} {rec2['availability']:<25}")
    
    print("\n" + "="*80)
    print("DETAILED COMPARISON")
    print("="*80)
    
    print(f"\n{rec1['alumni_name']} ({rec1['total_score']} points)")
    print("-" * 40)
    explanation1 = matcher.generate_explanation(student, rec1)
    print(explanation1)
    
    print(f"\n{rec2['alumni_name']} ({rec2['total_score']} points)")
    print("-" * 40)
    explanation2 = matcher.generate_explanation(student, rec2)
    print(explanation2)
    
    print("\n" + "="*80)
    if rec1['total_score'] > rec2['total_score']:
        print(f"✓ {rec1['alumni_name']} is a better match ({rec1['total_score']} vs {rec2['total_score']})")
    elif rec2['total_score'] > rec1['total_score']:
        print(f"✓ {rec2['alumni_name']} is a better match ({rec2['total_score']} vs {rec1['total_score']})")
    else:
        print("✓ Both alumni are equally matched")
    print("="*80 + "\n")

def detailed_analysis(matcher, student_df, alumni_df):
    """Show detailed analysis of recommendations"""
    
    print_header("DETAILED ANALYSIS", "=", 80)
    
    # Get all students recommendations
    for student_idx, student in student_df.iterrows():
        print(f"\n{'='*80}")
        print(f"STUDENT: {student['name']} ({student['id']})")
        print(f"{'='*80}\n")
        
        print(f"University: {student['university']}")
        print(f"Degree: {student['degree']}")
        print(f"Preferred Industry: {student['preferred_industry']}")
        print(f"Skills: {', '.join(student['skills'][:3])}...")
        print(f"Career Goals: {student['career_goals'][:70]}...\n")
        
        # Get recommendations
        recommendations = matcher.get_recommendations(student['id'], top_n=5)
        
        print(f"{'RANK':<5} {'ALUMNI NAME':<20} {'SCORE':<10} {'REASON':<45}")
        print("-" * 80)
        
        for rank, rec in enumerate(recommendations, 1):
            reason = matcher.generate_explanation(student, rec)
            reason = reason[:42] + "..." if len(reason) > 45 else reason
            print(f"{rank:<5} {rec['alumni_name']:<20} {rec['total_score']:<10} {reason:<45}")

def main():
    """Main function"""
    
    print_header("LOADING DATA...", "=", 80)
    
    # Load data
    alumni_df, student_df = load_data_to_dataframes(ALUMNI_DATA, STUDENT_DATA)
    
    print_success(f"Loaded {len(alumni_df)} alumni profiles")
    print_success(f"Loaded {len(student_df)} student profiles")
    print_separator()
    
    # Initialize matcher
    print_info("Initializing Graph-Based Hierarchical Matching Engine...")
    matcher = GBHMMatcher(alumni_df, student_df)
    print_success("System ready!")
    
    # Main loop
    while True:
        choice = display_interactive_menu()
        
        if choice == '1':
            get_student_recommendations(matcher, student_df, alumni_df)
        
        elif choice == '2':
            show_all_students(student_df)
        
        elif choice == '3':
            show_all_alumni(alumni_df)
        
        elif choice == '4':
            compare_alumni(matcher, student_df, alumni_df)
        
        elif choice == '5':
            detailed_analysis(matcher, student_df, alumni_df)
        
        elif choice == '0':
            print_header("Thank you for using GBHM System!", "=", 80)
            break
        
        else:
            print_error("Invalid choice! Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_header("Program interrupted by user. Goodbye!", "=", 80)
    except Exception as e:
        print_error(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()