import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from alumni_net.data.data_loader import DataLoader
from alumni_net.models.profile_processor import ProfileProcessor
from alumni_net.models.recommendation_engine import RecommendationEngine
from alumni_net.models.explainer import Explainer
from alumni_net.utils.config import AppConfig

def main():
    """Main function to run the alumni recommendation system."""
    # Load data
    data_loader = DataLoader()
    df, _ = data_loader.load_data()

    # Process profiles
    profile_processor = ProfileProcessor()
    feature_matrix, processed_df = profile_processor.process(df)

    # Initialize recommendation engine and explainer
    recommendation_engine = RecommendationEngine(feature_matrix, processed_df)
    explainer = Explainer(processed_df, profile_processor.vectorizer)

    # Get recommendations for a sample user
    sample_user_id = 1
    user_profile = processed_df[processed_df['id'] == sample_user_id].iloc[0]
    
    print(f"Getting recommendations for: {user_profile['name']}\n")

    recommendations = recommendation_engine.get_recommendations(
        sample_user_id, top_n=AppConfig.TOP_N_RECOMMENDATIONS
    )

    # Print recommendations and explanations
    print("--- Top Recommendations ---")
    for _, rec in recommendations.iterrows():
        explanation = explainer.get_explanation(sample_user_id, rec['id'])
        print(f"- {rec['name']} ({rec['job_title']} at {rec['company']})")
        print(f"  Explanation: {explanation}\n")

if __name__ == "__main__":
    main()
