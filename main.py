from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from gemini import call_to_gemini
from menu import return_as_str, get_menu
from celery import Celery 
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

        task = scrape_website_task.apply_async(args=[dining_hall, meal_selection, selected_restrictions])
        
        return redirect(url_for('loading_meal_plans', task_id=task.id))
    return render_template('select_dietary_restrictions.html', restrictions=restrictions)

@celery.task (bind=True)
def scrape_website_task(self, dining_hall, meal_selection, selected_restrictions):
    prompt = "Given the following menu, generate some healthy meal options: "
    #meal_options = call_to_gemini(prompt + return_as_str(dining_hall=dining_hall, meal=meal_selection, dietary_restrictions=selected_restrictions))
    #print(meal_options)
    menu = "menu: " + return_as_str(dining_hall=dining_hall, meal=meal_selection, dietary_restrictions=selected_restrictions)
    meal_plans = call_to_gemini(menu)
    #time.sleep(5)  # Simulating a long-running task
    
    # Returning some result for demonstration
    return {'status': 'Task completed!', 'result': meal_plans}

@app.route('/loading-meal-plans')
def loading_meal_plans():
    task_id = request.args.get('task_id')
    return render_template('meal_plans.html', task_id=task_id)

@app.route('/status/<task_id>')
def task_status(task_id):
    task = scrape_website_task.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # This is the exception raised
        }
    return jsonify(response)

#@app.route('/generate-plans')
#def generating_meal_plans():


if __name__ == '__main__':
    app.run(debug=True)
