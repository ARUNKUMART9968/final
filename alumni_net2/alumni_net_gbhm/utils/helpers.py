"""
Helper functions and utilities
"""

import pandas as pd
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

def print_header(text: str, char: str = "=", length: int = 80):
    """Print formatted header"""
    print(f"\n{Fore.CYAN}{char * length}")
    print(f"{text.center(length)}")
    print(f"{char * length}{Style.RESET_ALL}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_error(text: str):
    """Print error message"""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def print_info(text: str):
    """Print info message"""
    print(f"{Fore.BLUE}ℹ {text}{Style.RESET_ALL}")

def print_separator(char: str = "-", length: int = 80):
    """Print separator line"""
    print(f"{Fore.YELLOW}{char * length}{Style.RESET_ALL}")

def load_data_to_dataframes(alumni_data: list, student_data: list) -> tuple:
    """
    Convert static data to pandas DataFrames
    
    Args:
        alumni_data: List of alumni dictionaries
        student_data: List of student dictionaries
        
    Returns:
        Tuple of (alumni_df, student_df)
    """
    alumni_df = pd.DataFrame(alumni_data)
    student_df = pd.DataFrame(student_data)
    
    return alumni_df, student_df

def display_student_profile(student: pd.Series):
    """Display student profile summary"""
    print(f"\n{Fore.MAGENTA}Student Profile Summary:{Style.RESET_ALL}")
    print_separator("-")
    print(f"Name: {student['name']}")
    print(f"Email: {student['email']}")
    print(f"Expected Graduation: {student['expected_graduation']}")
    print(f"University: {student['university']}")
    print(f"Degree: {student['degree']}")
    print(f"GPA: {student['gpa']}")
    print(f"Skills: {', '.join(student['skills'][:4])}")
    if len(student['skills']) > 4:
        print(f"         ... and {len(student['skills']) - 4} more")
    print(f"Interests: {', '.join(student['interests'])}")
    print(f"Career Goals: {student['career_goals']}")
    print(f"Looking For: {', '.join(student['looking_for'])}")
    print(f"Preferred Industry: {student['preferred_industry']}")
    print_separator("-")

def display_recommendations_summary(recommendations: list, count: int = 5):
    """Display summary of all recommendations"""
    print(f"\n{Fore.CYAN}TOP {len(recommendations[:count])} ALUMNI RECOMMENDATIONS:{Style.RESET_ALL}")
    print_separator("-")
    
    for i, rec in enumerate(recommendations[:count], 1):
        print(f"\n{i}. {rec['alumni_name']} - Score: {Fore.GREEN}{rec['total_score']}{Style.RESET_ALL}")
        print(f"   Position: {rec['current_position']} at {rec['company']}")
        print(f"   Industry: {rec['industry']} | Experience: {rec['years_experience']} years")
        print(f"   Location: {rec['location']}")
    
    print_separator("-")