from bs4 import BeautifulSoup
import re

def is_safe(dietary_restrictions, individual_restrictions):
    for restriction in individual_restrictions:
        if restriction in dietary_restrictions:
            return False
    return True 

def is_friendly(dietary_restrictions, individual_restrictions):        
    for restriction in individual_restrictions:
        if restriction not in dietary_restrictions:
            if restriction == "Vegetarian" and "Vegan" not in dietary_restrictions:
                return False
    return True 

def filter_by_restrictions(cleaned_data, individual_restrictions):
    final_data = []

    restrictions = [] 
    friendly = []
    
    if len(individual_restrictions) == 0: # If no dietary restrictions, no need to filter the data 
        return cleaned_data

    for r in individual_restrictions: # For every dietary restriction the individual has
        if (r == "Halal" or r == "Gluten Friendly" or r == "Vegan" or r == "Vegetarian"):
            friendly.append(r) # Organize into two categories, the restrictions and the friendly category 
        else:
            restrictions.append(r) 

    for d in cleaned_data:
        d_restrictions = d[-1]
        if len(d_restrictions) == 0: # If food item itself has no restrictions, it's good to eat
            final_data.append(d)
            #print(d)
        else:
            if is_safe(d_restrictions, restrictions):
                if len(friendly) == 0:
                    final_data.append(d)
                    #print(d)
                else:
                    if is_friendly(d_restrictions, friendly):
                        final_data.append(d)
                        #print(d)
    return final_data

def parse_nutritional_info(html):
    soup = BeautifulSoup(html, "lxml")
    data = []
    allergens = []
    cleaned_data = [] 

    
    for item in soup.find_all("div", class_="labelrecipe", ):
        data.append(item.text.strip())
    for item in soup.find_all("font", attrs={"face": "arial"}):
        if item.get("size") in ["4", "5"]: 
            data.append(item.text.strip())
    webcodevalues = soup.find("span", class_="labelwebcodesvalue")
    if webcodevalues != None:
        images = webcodevalues.find_all('img')
        for item in images: 
            allergens.append(item['alt'])

    cleaned_data.append(data[0])
    cleaned_data.append(data[2])
    
    for d in data:
        #print(d)
        if (d != "" and d != []):
            if re.match(r'(\d+(\.\d+)?|[-\s]+)(g|mg)', d):
                if '-\xa0-\xa0-\xa0' in d:
                    cleaned_data.append('- ' + d[d.index('-\xa0-\xa0-\xa0') + len('-\xa0-\xa0-\xa0'):])
                else:
                    cleaned_data.append(d)
            elif ("Calories" in d):
                cleaned_data.append(d[d.index("Calories") + len("Calories") + 1:])            
    cleaned_data.append(allergens)       
    
    return cleaned_data
    
def parse_menu(html):
    soup = BeautifulSoup(html, "lxml")
    data = []

    for link in soup.find_all("div", class_="longmenucoldispname"):
        a_tag = link.find("a")
        if a_tag:
            href = a_tag.get("href")
            if (href != None):
                #print(href)
                data.append(href)
    return data 

def parse_dining_hall_page(html):
    soup = BeautifulSoup(html, "lxml")
    data = []

    for link in soup.find_all("span", class_="shortmenunutritive"):
        a_tag = link.find("a")
        if a_tag:
            href = a_tag.get("href")
            if (href != None):
                #print(href)
                data.append(href)
    return data
    
def parse_dining_halls(html):
    soup = BeautifulSoup(html, "lxml")
    data = []

    for link in soup.find_all("li", class_="locations"):
        a_tag = link.find("a")
        if a_tag:
            href = a_tag.get("href") 
            if (href != None):
                data.append(href)
                
    return data
