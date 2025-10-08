# # main.py
# """
# Main entry point for Alumni Network recommendation system
# """

# import sys
# import os

# # Add the project root to the Python path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from alumni_net.data.data_loader import DataLoader
# from alumni_net.models.profile_processor import ProfileProcessor
# from alumni_net.models.recommendation_engine import RecommendationEngine
# from alumni_net.utils.config import AppConfig

# def print_separator():
#     """Print a visual separator"""
#     print("\n" + "="*80 + "\n")

# def display_recommendation(rec, idx):
#     """Display a single recommendation with details"""
#     alumni = rec['alumni']
#     score = rec['match_score']
#     breakdown = rec['score_breakdown']
    
#     print(f"{idx}. {alumni['name']}")
#     print(f"   Position: {alumni['current_position']} at {alumni['company']}")
#     print(f"   Industry: {alumni['industry']}")
#     print(f"   Location: {alumni['location']}")
#     print(f"   Match Score: {score:.2%}")
#     print(f"   Score Breakdown:")
#     print(f"     - Semantic Similarity: {breakdown['semantic_similarity']:.2%}")
#     print(f"     - Skill Match: {breakdown['skill_match']:.2%}")
#     print(f"     - Industry/Interest: {breakdown['industry_interest']:.2%}")
#     print(f"     - Education Match: {breakdown['education_match']:.2%}")
#     print()

# def main():
#     """Main function to run the alumni recommendation system."""
    
#     print("🎓 Alumni Network - Student-Alumni Matching System")
#     print_separator()
    
#     # Step 1: Load data
#     print("📊 Loading data...")
#     data_loader = DataLoader()
#     alumni_df, student_df = data_loader.load_data()
#     print(f"✓ Loaded {len(alumni_df)} alumni and {len(student_df)} students")
#     print_separator()
    
#     # Step 2: Process profiles
#     print("🔄 Processing profiles with NLP...")
#     profile_processor = ProfileProcessor()
#     profile_processor.process_profiles(alumni_df, student_df)
#     print("✓ Profile processing complete")
#     print_separator()
    
#     # Step 3: Initialize recommendation engine
#     print("🤖 Initializing recommendation engine...")
#     recommendation_engine = RecommendationEngine(profile_processor)
#     recommendation_engine.fit(alumni_df, student_df)
#     print("✓ Recommendation engine ready")
#     print_separator()
    
#     # Step 4: Generate recommendations for each student
#     for idx, student_row in student_df.iterrows():
#         student_id = student_row['id']
#         student_name = student_row['name']
        
#         print(f"👤 Student: {student_name} ({student_id})")
#         print(f"   Degree: {student_row['degree']} at {student_row['university']}")
#         print(f"   Career Goals: {student_row['career_goals']}")
#         print(f"   Looking For: {', '.join(student_row['looking_for'])}")
#         print(f"   Preferred Industry: {student_row['preferred_industry']}")
#         print()
        
#         # Get recommendations
#         recommendations = recommendation_engine.get_recommendations(
#             student_id, 
#             top_n=AppConfig.TOP_N_RECOMMENDATIONS
#         )
        
#         print(f"🎯 Top {len(recommendations)} Alumni Recommendations:")
#         print("-" * 80)
        
#         for i, rec in enumerate(recommendations, 1):
#             display_recommendation(rec, i)
            
#             # Get detailed explanation
#             explanation = recommendation_engine.get_match_explanation(
#                 student_id, 
#                 rec['alumni']['id']
#             )
            
#             if explanation['explanations']:
#                 print(f"   💡 Why this match:")
#                 for exp in explanation['explanations']:
#                     print(f"      • {exp}")
#                 print()
        
#         print_separator()
    
#     print("✅ Recommendation process complete!")

# if __name__ == "__main__":
#     try:
#         main()
#     except Exception as e:
#         print(f"\n❌ Error occurred: {str(e)}")
#         import traceback
#         traceback.print_exc()


# main.py - Interactive Version
"""
Interactive Alumni Network recommendation system
Enter student details to get personalized alumni recommendations
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from alumni_net.data.data_loader import DataLoader
from alumni_net.models.profile_processor import ProfileProcessor
from alumni_net.models.recommendation_engine import RecommendationEngine
from alumni_net.utils.config import AppConfig
import pandas as pd

def print_separator(char="=", length=80):
    """Print a visual separator"""
    print("\n" + char * length + "\n")

def print_header():
    """Print application header"""
    print("\n" + "="*80)
    print("🎓 ALUMNI NETWORK - STUDENT-ALUMNI MATCHING SYSTEM")
    print("="*80 + "\n")

def display_recommendation(rec, idx):
    """Display a single recommendation with details"""
    alumni = rec['alumni']
    score = rec['match_score']
    breakdown = rec['score_breakdown']
    explanation = rec.get('explanation', {})
    
    print(f"\n{'─'*80}")
    print(f"🏆 RECOMMENDATION #{idx}")
    print(f"{'─'*80}")
    print(f"\n👤 Name: {alumni['name']}")
    print(f"💼 Position: {alumni['current_position']}")
    print(f"🏢 Company: {alumni['company']}")
    print(f"🏭 Industry: {alumni['industry']}")
    print(f"📍 Location: {alumni['location']}")
    print(f"🎓 Education: {alumni['degree']} from {alumni['university']} ({alumni['graduation_year']})")
    print(f"⏱️  Experience: {alumni['years_experience']} years")
    print(f"📧 Email: {alumni['email']}")
    
    print(f"\n🎯 Match Score: {score:.1%}")
    print(f"\n📊 Score Breakdown:")
    print(f"   • Semantic Similarity: {breakdown['semantic_similarity']/0.4:.1%} (Weight: 40%)")
    print(f"   • Skill Match: {breakdown['skill_match']/0.3:.1%} (Weight: 30%)")
    print(f"   • Industry/Interest: {breakdown['industry_interest']/0.2:.1%} (Weight: 20%)")
    print(f"   • Education Match: {breakdown['education_match']/0.1:.1%} (Weight: 10%)")
    
    # Display detailed match information
    if explanation and explanation.get('explanations'):
        print(f"\n💡 Why This Match:")
        for exp in explanation['explanations']:
            print(f"   ✓ {exp}")
    
    # Display alumni's skills and interests
    print(f"\n🔧 Skills: {', '.join(alumni['skills'][:5])}")
    if len(alumni['skills']) > 5:
        print(f"          ... and {len(alumni['skills'])-5} more")
    
    print(f"❤️  Interests: {', '.join(alumni['interests'])}")
    print(f"🎯 Mentoring Areas: {', '.join(alumni['mentoring_areas'])}")
    print(f"✅ Availability: {alumni['availability']}")
    
    print(f"\n📝 Bio: {alumni['bio']}")

def get_student_input():
    """Get student details from user input"""
    print("\n📝 ENTER STUDENT DETAILS")
    print("─"*80)
    
    student_data = {}
    
    # Basic Information
    student_data['name'] = input("\n👤 Your Name: ").strip()
    student_data['email'] = input("📧 Your Email: ").strip()
    
    # Education
    student_data['university'] = input("🎓 University: ").strip()
    student_data['degree'] = input("📚 Degree Program (e.g., Computer Science): ").strip()
    student_data['expected_graduation'] = input("📅 Expected Graduation Year: ").strip()
    
    try:
        student_data['gpa'] = float(input("📊 GPA (e.g., 3.8): ").strip())
    except:
        student_data['gpa'] = 3.5
    
    # Skills
    print("\n🔧 Skills (comma-separated, e.g., Python, Java, Machine Learning):")
    skills_input = input("   ").strip()
    student_data['skills'] = [s.strip() for s in skills_input.split(',') if s.strip()]
    
    # Interests
    print("\n❤️  Interests (comma-separated, e.g., AI, Data Science, Robotics):")
    interests_input = input("   ").strip()
    student_data['interests'] = [i.strip() for i in interests_input.split(',') if i.strip()]
    
    # Career Goals
    print("\n🎯 Career Goals (describe what you want to achieve):")
    student_data['career_goals'] = input("   ").strip()
    
    # Preferred Industry
    student_data['preferred_industry'] = input("\n🏭 Preferred Industry (e.g., Technology, Healthcare): ").strip()
    
    # Looking For
    print("\n🔍 What are you looking for? (comma-separated)")
    print("   Examples: Technical Mentorship, Career Advice, Interview Preparation")
    looking_for_input = input("   ").strip()
    student_data['looking_for'] = [l.strip() for l in looking_for_input.split(',') if l.strip()]
    
    # Projects
    print("\n🚀 Projects/Experience (brief description):")
    student_data['projects'] = input("   ").strip()
    
    return student_data

def create_profile_text(student_data):
    """Create profile text for NLP processing"""
    text_parts = [
        f"Degree: {student_data['degree']}",
        f"University: {student_data['university']}",
        f"Skills: {', '.join(student_data['skills'])}",
        f"Interests: {', '.join(student_data['interests'])}",
        f"Career Goals: {student_data['career_goals']}",
        f"Looking For: {', '.join(student_data['looking_for'])}",
        f"Industry: {student_data['preferred_industry']}",
        f"Projects: {student_data['projects']}"
    ]
    return ' '.join(text_parts)

def main():
    """Main function to run the interactive recommendation system."""
    
    print_header()
    
    print("Welcome! This system will match you with alumni mentors based on your profile.\n")
    
    # Option to use existing student or create new
    print("Choose an option:")
    print("1. Enter new student details")
    print("2. Use existing student profile (demo)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    # Load existing data
    print("\n📊 Loading alumni database...")
    data_loader = DataLoader()
    alumni_df, student_df = data_loader.load_data()
    print(f"✓ Loaded {len(alumni_df)} alumni profiles")
    
    # Process existing alumni profiles
    print("\n🔄 Processing alumni profiles with NLP...")
    profile_processor = ProfileProcessor()
    
    if choice == "2":
        # Use existing student
        print("\n📋 Available Students:")
        for idx, student in student_df.iterrows():
            print(f"{idx+1}. {student['name']} - {student['degree']} at {student['university']}")
        
        student_idx = int(input("\nSelect student number: ").strip()) - 1
        student_data = student_df.iloc[student_idx].to_dict()
        student_id = student_data['id']
        
        # Process all profiles
        profile_processor.process_profiles(alumni_df, student_df)
        
    else:
        # Get new student input
        student_data = get_student_input()
        student_data['id'] = 'NEW_STUDENT'
        student_data['profile_text'] = create_profile_text(student_data)
        student_id = 'NEW_STUDENT'
        
        # Add new student to dataframe
        new_student_df = pd.DataFrame([student_data])
        combined_student_df = pd.concat([student_df, new_student_df], ignore_index=True)
        
        # Process profiles including new student
        profile_processor.process_profiles(alumni_df, combined_student_df)
        student_df = combined_student_df
    
    print("✓ Profile processing complete")
    
    # Initialize recommendation engine
    print("\n🤖 Generating personalized recommendations...")
    recommendation_engine = RecommendationEngine(profile_processor)
    recommendation_engine.fit(alumni_df, student_df)
    
    # Get number of recommendations
    try:
        num_recs = int(input(f"\nHow many recommendations do you want? (1-{len(alumni_df)}): ").strip())
        num_recs = min(max(1, num_recs), len(alumni_df))
    except:
        num_recs = 3
    
    # Generate recommendations
    recommendations = recommendation_engine.get_recommendations(student_id, top_n=num_recs)
    
    # Display student profile summary
    print_separator("=")
    print("👤 YOUR PROFILE SUMMARY")
    print_separator("=")
    print(f"Name: {student_data['name']}")
    print(f"Education: {student_data['degree']} at {student_data['university']}")
    print(f"Skills: {', '.join(student_data['skills'][:5])}")
    print(f"Interests: {', '.join(student_data['interests'])}")
    print(f"Career Goals: {student_data['career_goals']}")
    print(f"Preferred Industry: {student_data['preferred_industry']}")
    
    # Display recommendations
    print_separator("=")
    print(f"🎯 TOP {len(recommendations)} ALUMNI RECOMMENDATIONS")
    print_separator("=")
    
    for i, rec in enumerate(recommendations, 1):
        # Get detailed explanation
        explanation = recommendation_engine.get_match_explanation(
            student_id, 
            rec['alumni']['id']
        )
        rec['explanation'] = explanation
        
        display_recommendation(rec, i)
    
    print_separator("=")
    print("✅ RECOMMENDATION PROCESS COMPLETE!")
    print("\n💡 Next Steps:")
    print("   1. Review the recommended alumni profiles above")
    print("   2. Reach out via email to introduce yourself")
    print("   3. Mention specific reasons why you'd like to connect")
    print("   4. Be respectful of their time and availability")
    print_separator("=")
    
    # Option to save results
    save_choice = input("\n💾 Would you like to see a summary? (y/n): ").strip().lower()
    if save_choice == 'y':
        print("\n📊 QUICK SUMMARY")
        print("─"*80)
        for i, rec in enumerate(recommendations, 1):
            alumni = rec['alumni']
            print(f"{i}. {alumni['name']} ({alumni['current_position']} at {alumni['company']}) - Match: {rec['match_score']:.1%}")
        print("─"*80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()