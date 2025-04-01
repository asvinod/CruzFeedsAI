from requester import request_html, requests
from parser import parse_dining_hall_page, parse_menu, parse_nutritional_info, parse_dining_halls, filter_by_restrictions
from storage import save_to_csv_item
import pandas as pd

def get_menu(url="https://nutrition.sa.ucsc.edu/location.aspx", dining_hall="John", meal="Breakfast", calories=0, dietary_restrictions=["Vegetarian", "Gluten Friendly"], header_url="https://nutrition.sa.ucsc.edu/"):
    menu_list = [] 
    session = requests.Session()
    session.headers.update(
        {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
    )

    dining_halls_list_html = session.get(url)
    print(dining_halls_list_html)
    dining_halls_list = parse_dining_halls(dining_halls_list_html.text)

    for dining_hall_url in dining_halls_list:
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
                        menu_list.append(item_information)
                        #print(item_information)
    menu_list = filter_by_restrictions(menu_list, dietary_restrictions)
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

def return_as_str(url="https://nutrition.sa.ucsc.edu/location.aspx", dining_hall="John", meal="Breakfast", calories=0, dietary_restrictions=["Vegetarian", "Gluten Friendly"], header_url="https://nutrition.sa.ucsc.edu/"):
    menu = get_menu(url, dining_hall, meal, calories, dietary_restrictions, header_url)
    menu_str = "" 

    item_information = ["Food Item", "Serving Size", "Calories", "Total Fat", "Total Carb", "Sat Fat",
    "Dietary Fiber", "Trans Fat", "Sugars", "Cholesterol", "Protein", "Sodium", "Allergens"]

    for l in menu:
        length = len(l)
        i = 0 
        while i < length:
            menu_str += str(item_information[i]) + ": " + str(l[i]) + "\n"
            i += 1
        menu_str += "\n"
    return menu_str 

def main():
    print(return_as_str())
    """
    url = "https://nutrition.sa.ucsc.edu/label.aspx?locationNum=40&locationName=John+R.+Lewis+%26+College+Nine+Dining+Hall&dtdate=02%2f27%2f2025&RecNumAndPort=888815*2"
    session = requests.Session()
    session.headers.update(
        {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
    )

    dining_halls_list_html = session.get(url)
    data = parse_nutritional_info(dining_halls_list_html.text)
    print(data)"""

if __name__ == "__main__":
    main()