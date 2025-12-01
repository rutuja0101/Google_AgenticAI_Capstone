from google import genai



# PASTE YOUR NEW KEY INSIDE THE QUOTES BELOW

client = genai.Client(api_key="Insert your API key")



try:

    response = client.models.generate_content(

        model="gemini-2.0-flash", 

        contents="Hello, do you work?"

    )

    print("\n✅ SUCCESS! The Key is working.")

    print("Response: " + response.text)

except Exception as e:

    print("\n❌ FAILURE. The Key is still broken.")

    print("Error details:", e)
