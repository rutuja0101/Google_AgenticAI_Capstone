#!/usr/bin/env python3
"""
Quick Fix Script - Test Your API Key and Setup
This will verify everything is working before running the full demo
"""

import os
import sys

print("🔍 Checking your setup...")
print("-" * 40)

# Check Python version
import platform
python_version = platform.python_version()
print(f"✅ Python version: {python_version}")

# Check for API key
gemini_key = os.getenv('GEMINI_API_KEY')
if gemini_key:
    print(f"✅ GEMINI_API_KEY found: {gemini_key[:10]}...")
else:
    print("❌ No GEMINI_API_KEY found")
    print("\nTo fix this, run:")
    print("export GEMINI_API_KEY='your-actual-key-here'")
    sys.exit(1)

# Try to import and test Gemini
try:
    print("\n📦 Testing Google Gemini connection...")
    import google.generativeai as genai
    
    # Configure with your API key
    genai.configure(api_key=gemini_key)
    
    # Try different model names
    model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    working_model = None
    for model_name in model_names:
        try:
            print(f"   Trying model: {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'Hello, AI Agents Course!'")
            print(f"   ✅ {model_name} works!")
            print(f"   Response: {response.text[:50]}...")
            working_model = model_name
            break
        except Exception as e:
            print(f"   ❌ {model_name} failed: {str(e)[:50]}...")
    
    if working_model:
        print(f"\n🎉 Success! Use model: {working_model}")
        print("\n📝 Next steps:")
        print(f"1. Open personal_task_agent.py")
        print(f"2. Find: genai.GenerativeModel('gemini-pro')")
        print(f"3. Change to: genai.GenerativeModel('{working_model}')")
        print(f"4. Save and run: python3 demo.py")
    else:
        print("\n❌ No models worked. Check your API key is valid.")
        
except ImportError:
    print("❌ google-generativeai not installed")
    print("\nTo fix this, run:")
    print("pip3 install google-generativeai")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nMake sure your API key is valid")
