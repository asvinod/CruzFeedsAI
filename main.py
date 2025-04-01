from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from gemini import call_to_gemini
from menu import return_as_str, get_menu
from celery import Celery, chain
import time

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = "redis://localhost:6379/0"
app.config['CELERY_RESULT_BACKEND'] = "redis://localhost:6379/0"

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

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
        dining_hall = session.get('dining_hall', 'Unknown')
        meal_selection = session.get('meal_selection', 'Unknown')
        arguments = [selected_restrictions, dining_hall, meal_selection]

        workflow = chain(scrape_menu.s(dining_hall, meal_selection, selected_restrictions),
                 generate_meal_options.s())
                    
        task = workflow.apply_async()
        
        return redirect(url_for('loading_meal_plans', task_id=task.id))
    return render_template('select_dietary_restrictions.html', restrictions=restrictions)

@celery.task 
def scrape_menu(dining_hall, meal_selection, selected_restrictions):
    menu = return_as_str(dining_hall=dining_hall, meal=meal_selection, dietary_restrictions=selected_restrictions)    
    return menu

@celery.task
def generate_meal_options(menu):
    print(menu)
    prompt = "Given the following menu, generate some healthy meal options: "
    meal_options = call_to_gemini(prompt + menu)

    return meal_options

@app.route('/loading-meal-plans')
def loading_meal_plans():
    task_id = request.args.get('task_id')
    return render_template('meal_plans.html', task_id=task_id)

@app.route('/status/<task_id>')
def task_status(task_id):
    task = generate_meal_options.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Pending...'}
    elif task.state != 'FAILURE':
        response = {'state': task.state, 'status': task.info}
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {'state': task.state, 'status': str(task.info)}  # Show error if failed

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
