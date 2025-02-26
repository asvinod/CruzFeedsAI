from google import genai
 

client = genai.Client(api_key="AIzaSyA0t4CkoZyv11xVAkz_zepqBNLuuCWBsDI")
#test_list = ['can', ['you', ['understand this?']]]
test_list=['If I gave you a big string of food items, with their nutritional information and serving size, would you be able to generate healthy meal options with that?']
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=test_list
)

print(response.text)    
