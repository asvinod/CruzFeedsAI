from requester import request_html, requests
from parser import parse_dining_hall_page, parse_menu, parse_nutritional_info, parse_dining_halls
from storage import save_dining_hall_information, filter_csv
import polars as pl 
import numpy as np 
import threading 

def save_all_menus():
    dining_halls = ["John", "Crown", "Kresge", "Rachel", "Cowell"]
    meal_options = ["Breakfast", "Lunch", "Dinner", "Late"]

    threads = []

    for dining_hall in dining_halls:
        for meal in meal_options:
            thread = threading.Thread(target=save_menu, args=(dining_hall, meal))
            thread.start()
            threads.append(thread)
    for thread in threads:
        thread.join()
            
def save_menu(dining_hall, meal):
    menu = get_menu(dining_hall=dining_hall, meal=meal) 
    save_dining_hall_information(menu, dining_hall, meal)

def get_menu(url="https://nutrition.sa.ucsc.edu/location.aspx", dining_hall="John", meal="Dinner", calories=0, dietary_restrictions=["Vegetarian", "Gluten Friendly"], header_url="https://nutrition.sa.ucsc.edu/"):
    menu_list = np.empty((1000, 13), dtype=object)
    session = requests.Session()
    session.headers.update(
        {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
    )

    dining_halls_list_html = session.get(url)
    dining_halls_list = parse_dining_halls(dining_halls_list_html.text)

    i = 0

    for dining_hall_url in dining_halls_list:
        #print(dining_hall_url)
        if (dining_hall in dining_hall_url):
            dining_hall_html = session.get(header_url + dining_hall_url)
            dining_hall_menus = parse_dining_hall_page(dining_hall_html.text)
    
            for menu in dining_hall_menus:
                if (meal in menu):
                    menu_html = session.get(header_url + menu)
                    menu = parse_menu(menu_html.text)
                    for item in menu:
                        item_html = session.get(header_url + item)
                        item_information = parse_nutritional_info(item_html.text)
                        if (len(item_information) == 13):
                            print(item_information) 
                            print(i)
                            menu_list[i] = item_information
                            i += 1
                        #print(item_information)
    return menu_list

def display_as_str():
    menu = get_menu()

    item_information = ["Food Item", "Serving Size", "Calories", "Total Fat", "Total Carb", "Sat Fat",
    "Dietary Fiber", "Trans Fat", "Sugars", "Cholesterol", "Protein", "Sodium", "Allergens"]

    for l in menu:
        length = len(l)
        i = 0 
        while i < length:
            print(item_information[i] + ": ", end="")
            print(l[i])
            i += 1 
        print()

def return_as_str():
    menu = get_menu()
    menu_str = "" 

    item_information = ["Food Item", "Serving Size", "Calories", "Total Fat", "Total Carb", "Sat Fat",
    "Dietary Fiber", "Trans Fat", "Sugars", "Cholesterol", "Protein", "Sodium", "Allergens"]

    for l in menu:
        length = len(item_information)
        i = 0 
        #print(l)
        while i < length:
            menu_str += str(item_information[i]) + ": " + str(l[i]) + "\n"
            i += 1
        menu_str += "\n"
    return menu_str 

def main():
    #save_all_menus()
    filter_csv("John", "Dinner", ["Vegan"])
if __name__ == "__main__":
    main()