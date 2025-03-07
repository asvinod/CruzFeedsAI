from flask import Flask, render_template, request, redirect, url_for, session
from gemini import call_to_gemini
from menu import return_as_str

app = Flask(__name__)
app.secret_key = "your_secret_key" 

@app.route('/', methods=['GET', 'POST'])
def select_dining_hall():
    if request.method == 'POST':
        dining_hall = request.form.get('dining_hall')
        session['dining_hall'] = dining_hall  
        print(f"Dining Hall Selected: {dining_hall}")
        return redirect(url_for('select_meal'))  
    return render_template('select_dining_hall.html')

@app.route('/meal-selection', methods=['GET', 'POST'])
def select_meal():
    if request.method == 'POST':
        meal_selection = request.form.get('meal_selection')
        session['meal_selection'] = meal_selection  
        print(f"Meal Selected: {meal_selection}")
        return redirect(url_for('select_dietary_restrictions'))  

    return render_template('select_meal.html')  

@app.route('/dietary-restrictions', methods = ['GET', 'POST'])
def select_dietary_restrictions():
    restrictions = ["Peanut", "Tree Nut", "Gluten Friendly", "Milk", \
    "Egg", "Soy", "Shellfish", "Fish", "Sesame", "Alcohol", "Vegetarian", \
    "Vegan", "Halal", "Beef", "Pork"]

    if request.method == 'POST':
        selected_restrictions = request.form.getlist('restrictions')
        session['selected_restrictions'] = selected_restrictions
        print(f"Restrictions Selected: {selected_restrictions}")
        return redirect(url_for('display_meal_plans'))
    return render_template('select_dietary_restrictions.html', restrictions=restrictions)

@app.route('/meal-plans')
def display_meal_plans():
    dining_hall = session.get('dining_hall', 'Unknown')
    meal_selection = session.get('meal_selection', 'Unknown')
    selected_restrictions = session.get('selected_restrictions', 'Unknown')

    #menu = return_as_str(dining_hall=dining_hall, meal=meal_selection, dietary_restrictions=selected_restrictions)
    #prompt = "Create meal options with their nutritional information with the given menu: " + menu

    #result = call_to_gemini(prompt)
    #print(result)
    result = 'test'

    return render_template('meal_plans.html', result="Hello World")


if __name__ == '__main__':
    app.run(debug=True)
