import polars as pl
import os
import threading
import numpy as np 

def filter_csv(dining_hall, meal, dietary_restrictions):
    friendly = [] 
    restrictions = [] 

    for r in dietary_restrictions: 
        if (r == "Halal" or r == "Gluten Friendly" or r == "Vegan" or r == "Vegetarian"):
            friendly.append(r) 
        else:
            restrictions.append(r) 
    
    df = pl.read_csv(f"data/{dining_hall}_{meal}.csv")
    restrictions_column = df["Dietary Restrictions"]

    mask = pl.lit(True)

    for restriction in restrictions:
        mask = mask & (~pl.col("Dietary Restrictions").str.contains(restriction))

    for need in friendly:
        mask = mask & pl.col("Dietary Restrictions").str.contains(need)
    
    filtered_df = df.filter(mask)

    # if True:
    #     filtered_out_df = df.filter(~mask)
    #     print("\n--- FILTERED OUT ROWS ---")
    #     print(filtered_out_df)
    #     print("\n--- KEPT ROWS ---")
    #     print(filtered_df)

    return filtered_df


def flatten_dietary_restrictions(row):
    if isinstance(row[-1], list):
        row[-1] = ', '.join(row[-1])
    return row 

def save_dining_hall_information(data, dining_hall, meal):
    #print(data.shape)
    #print(data) 

    data = np.array([flatten_dietary_restrictions(row) for row in data])
    
    filename = f"data/{dining_hall}_{meal}.csv"
    
    headers = ["Food Item", "Serving Size", "Calories", "Total Fat", "Total Carb", "Sat Fat", 
               "Dietary Fiber", "Trans Fat", "Sugar", "Cholesterol", "Protein", "Sodium", "Dietary Restrictions"]
    
    df = pl.DataFrame(data, schema=headers)
    
    df_cleaned = df.filter(~pl.col("Food Item").is_null())

    df_cleaned = df_cleaned.with_columns(
        pl.when(
            pl.col("Dietary Restrictions").str.contains("(?i)Vegan") &
            ~pl.col("Dietary Restrictions").str.contains("(?i)Vegetarian")  
        )
        .then(pl.col("Dietary Restrictions") + ", Vegetarian")
        .otherwise(pl.col("Dietary Restrictions"))
        .alias("Dietary Restrictions")
    )

    df_cleaned = df_cleaned.with_columns(
        pl.when(
            pl.col("Dietary Restrictions").str.contains("(?i)Vegan|Vegetarian") &
            ~pl.col("Dietary Restrictions").str.contains("(?i)Halal")  
        )
        .then(pl.col("Dietary Restrictions") + ", Halal")
        .otherwise(pl.col("Dietary Restrictions"))
        .alias("Dietary Restrictions")
    )


    df_cleaned.write_csv(filename)