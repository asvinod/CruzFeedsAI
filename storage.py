import pandas as pd
import os


def save_to_csv_item(data, filename="data/output.csv"):
    headers = ["Food Item", "Serving Size", "Calories", "Total Fat", "Total Carb", "Sat Fat", 
               "Dietary Fiber", "Trans Fat", "Sugar", "Cholesterol", "Protein", "Sodium", "Dietary Restrictions"]
    try:
        if os.path.exists(filename):
            os.remove(filename)
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        if isinstance(data[0], list):
            df = pd.DataFrame(data, columns=headers)
        else:
            df = pd.DataFrame([data], columns=headers)
        
        df.to_csv(filename, index=False)
    
    except Exception as e:
        print(f"Error saving data: {e}")