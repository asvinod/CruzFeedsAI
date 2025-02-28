from google import genai
from main import return_as_str
 

client = genai.Client(api_key="AIzaSyA0t4CkoZyv11xVAkz_zepqBNLuuCWBsDI")
menu = return_as_str() 
test_list=["Create a few meal options from the provided menu:" + menu]
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=test_list
)

print(response.text)    
