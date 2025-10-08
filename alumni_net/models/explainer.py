
import pandas as pd

class Explainer:
    def __init__(self, df, vectorizer):
        self.df = df
        self.vectorizer = vectorizer

    def get_explanation(self, user_id, recommended_id):
        """
        Generates an explanation for a recommendation.
        """
        user_profile = self.df[self.df['id'] == user_id].iloc[0]
        recommended_profile = self.df[self.df['id'] == recommended_id].iloc[0]

        user_features = user_profile['text_features']
        recommended_features = recommended_profile['text_features']

        # Get the feature names from the vectorizer
        feature_names = self.vectorizer.get_feature_names_out()

        # Find common features
        user_skills_interests = set(user_features.split())
        recommended_skills_interests = set(recommended_features.split())

        common_features = list(user_skills_interests.intersection(recommended_skills_interests))

        if not common_features:
            return "Recommendation based on general profile similarity."

        explanation = f"You and {recommended_profile['name']} share common interests and skills: {', '.join(common_features)}."
        return explanation