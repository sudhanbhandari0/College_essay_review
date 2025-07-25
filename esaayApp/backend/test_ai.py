from ai_service import AIService

def test_ai_service():
    print("Testing AI Service...")

    # Create AI service
    ai_service = AIService()

    # Test loading model
    print("\n1. Testing model loading...")
    success = ai_service.load_model()

    if success:
        print("✅ Model loaded successfully!")

        # Test generating feedback
        print("\n2. Testing feedback generation...")
        test_essay = (
            "Interacting with customers at the deli catalyzes my linguistic journey. One day, my Spanish teacher introduces himself in German, which sounds beautiful and rich. I immediately install Duolingo and practice. My enthusiasm for Spanish initially leads to studying German, then studying the cyrillic alphabet for Russian, then memorizing over 60 Hiragana and Katakana characters for Japanese. Now I am watching documentaries and Netflix series in other languages, reading books like “Western Philosophy in Simple Spanish” and “World War 1 in Simple German,” (by Olly Richards, leader of the YouTube language dorks)."
        )

        feedback = ai_service.generate_feedback(test_essay)
        print(f"✅ Feedback generated:\n{feedback}")
    else:
        print("❌ Model loading failed!")

if __name__ == "__main__":
    test_ai_service()