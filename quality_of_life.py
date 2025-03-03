import pandas as pd

def load_data(file_path, sheet_name="Sheet1"):
    """
    Load the Excel sheet into a DataFrame.
    :param file_path: Path to the Excel file.
    :param sheet_name: Name of the sheet to load (default is "Sheet1").
    :return: DataFrame containing the data from the specified sheet.
    """
    # Load the Excel sheet into a DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Replace "?" with None to handle missing values
    df.replace("?", None, inplace=True)  # Replace missing values
    
    return df

def categorize_value(value, thresholds, labels):
    """
    Categorize a numerical value based on given thresholds.
    :param value: The numerical value to categorize.
    :param thresholds: A list of threshold values for categorization.
    :param labels: A list of labels corresponding to the thresholds.
    :return: The label corresponding to the value's category.
    """
    # Iterate through thresholds and return the corresponding label
    for i, threshold in enumerate(thresholds):
        if value <= threshold:
            return labels[i]
    
    # If the value exceeds all thresholds, return the last label
    return labels[-1]

def compute_quality_of_life(data, city):
    """
    Compute the Quality of Life Index for a given city.
    :param data: DataFrame containing quality of life data for cities.
    :param city: The city for which to compute the Quality of Life Index.
    """
    # Filter the dataset for the selected city
    row = data[data['City'] == city]
    if row.empty:
        print("City not found.")
        return
    
    # Print the city name before categorized values
    print(f"City: {city}")
    
    # Extract values and convert to float where possible
    try:
        pp = float(row["Purchasing Power Index"].values[0])
        safety = float(row["Safety Index"].values[0])
        health = float(row["Health Care Index"].values[0])
        climate = float(row["Climate Index"].values[0])
        col = float(row["Cost Of Living Index"].values[0])
        prop = float(row["Property Price to Income Ratio"].values[0])
        traffic = float(row["Traffic Commute Time Index"].values[0])
        pollution = float(row["Pollution Index"].values[0])
    except:
        # If any value is missing or cannot be converted to float, print a message and return
        print("Missing value in data.")
        return
    
    # Compute Quality of Life Index using a weighted formula
    qol = max(0, 100 + pp / 2.5 - prop * 1.0 - col / 10 + safety / 2.0 + health / 2.5 - traffic / 2.0 - pollution * 2.0 / 3.0 + climate / 3.0)
    
    # Define thresholds and labels for categorization
    thresholds = {
        "Purchasing Power Index": [40, 80, 120, 160],
        "Safety Index": [20, 40, 60, 80],
        "Health Care Index": [20, 40, 60, 80],
        "Climate Index": [20, 40, 60, 80],
        "Cost Of Living Index": [20, 40, 60, 80],
        "Property Price to Income Ratio": [2, 4, 6, 8],
        "Traffic Commute Time Index": [20, 40, 60, 80],
        "Pollution Index": [20, 40, 60, 80],
        "Quality of Life Index": [48, 96, 144, 192]
    }
    
    # Labels for categorization
    labels = ["Very Low", "Low", "Moderate", "High", "Very High"]
    
    # Print categorized values for each index
    print(f"Purchasing Power Index: {pp} ({categorize_value(pp, thresholds['Purchasing Power Index'], labels)})")
    print(f"Safety Index: {safety} ({categorize_value(safety, thresholds['Safety Index'], labels)})")
    print(f"Health Care Index: {health} ({categorize_value(health, thresholds['Health Care Index'], labels)})")
    print(f"Climate Index: {climate} ({categorize_value(climate, thresholds['Climate Index'], labels)})")
    print(f"Cost Of Living Index: {col} ({categorize_value(col, thresholds['Cost Of Living Index'], labels)})")
    print(f"Property Price to Income Ratio: {prop} ({categorize_value(prop, thresholds['Property Price to Income Ratio'], labels)})")
    print(f"Traffic Commute Time Index: {traffic} ({categorize_value(traffic, thresholds['Traffic Commute Time Index'], labels)})")
    print(f"Pollution Index: {pollution} ({categorize_value(pollution, thresholds['Pollution Index'], labels)})")
    print(f"Quality of Life Index: {qol} ({categorize_value(qol, thresholds['Quality of Life Index'], labels)})")

# Update file path for correct data loading
if __name__ == "__main__":
    # Path to the Excel file containing quality of life data
    file_path = "data/Random Cities in USA (Quality of Life Index).xlsx"
    
    # Load the data into a DataFrame
    df = load_data(file_path)
    
    # Specify the city for which to compute the Quality of Life Index
    city_name = "Los Angeles, CA"  # Change as needed
    
    # Compute and print the Quality of Life Index for the specified city
    compute_quality_of_life(df, city_name)
