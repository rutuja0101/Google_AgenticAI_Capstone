import google.generativeai as genai
import os

# Try to get the key from your terminal environment
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("\n❌ ERROR: API Key not found!")
    print("Please run this command in your terminal first:")
    print("export GEMINI_API_KEY='your_actual_key_here'")
else:
    print(f"\n✅ Found API Key! Checking models...")
    try:
        genai.configure(api_key=api_key)
        found_any = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- Available: {m.name}")
                found_any = True
        
        if not found_any:
            print("\n❌ Connected, but no models found. (Check plan/billing?)")
    except Exception as e:
        print(f"\n❌ Connection Error: {e}")
