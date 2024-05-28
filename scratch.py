import os
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
import numpy as np


# Define a function to calculate the probability of running out of stock
def out_of_stock_prob(data, item, lead_time=0):

    row = data[data["Type of item"] == item]

    # Handle potential errors
    if row.empty:
        print(f"Item '{item}' not found in data.")
        return None
    elif row["standard deviation"].values[0] == 0:
        print(
            f"Standard deviation for item '{item}' is zero. Cannot calculate probability."
        )
        return None

    inventory = row["number of items"].values[0]
    average_sales = row["average items sold per month"].values[0]
    std_dev = row["standard deviation"].values[0]

    # Calculate demand during lead time
    demand = average_sales * (1 + lead_time)

    # Calculate z-score
    z_score = (inventory - demand) / std_dev

    # Calculate probability using the standard normal distribution (z-score)
    p_out_of_stock = 1 - norm.cdf(z_score)

    return p_out_of_stock


# Load data into a DataFrame
data = {
    "Type of item": [
        "iphones",
        "ipads",
        "laptops",
        "workstations",
        "game stations",
        "PCs",
        "dishwashers",
        "hoods",
        "refrigerators",
        "freezers",
        "microwaves",
        "laundry machines",
        "dryers",
        "stoves",
    ],
    "number of items": [130, 102, 58, 30, 120, 89, 29, 80, 31, 50, 67, 25, 17, 37],
    "average items sold per month": [
        100,
        78,
        68,
        29,
        113,
        87,
        20,
        70,
        28,
        45,
        63,
        30,
        21,
        30,
    ],
    "standard deviation": [14, 16, 5.2, 3.1, 9, 10.2, 3, 3, 1.5, 3.4, 4, 2.3, 2.1, 4.1],
}

df = pd.DataFrame(data)
datums = data
df["Stockout Probability"] = df.apply(
    lambda row: out_of_stock_prob(df, row["Type of item"]), axis=1
)


def clean():
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".png"):
            os.remove(os.path.join(os.getcwd(), filename))
    try:
        os.rmdir("graphs")
    except:
        print("done``")


def generage_pngs():
    if os.path.exists(os.path.join(os.getcwd(), "graphs")) == False:
        os.makedirs(os.path.join(os.getcwd(), "graphs"))
    for index, row in df.iterrows():
        # Extract data from the row
        item = row["Type of item"]
        inventory = row["number of items"]
        average_sales = row["average items sold per month"]
        std_dev = row["standard deviation"]
        stockout_probability = row["Stockout Probability"]
        # Calculate x-axis values for the normal distribution
        x = np.linspace(
            norm.ppf(0.01, loc=inventory, scale=std_dev),
            norm.ppf(0.99, loc=inventory, scale=std_dev),
            100,
        )
        # Generate the normal distribution PDF
        y = norm.pdf(x, loc=inventory, scale=std_dev)
        # Create the plot
        plt.figure(figsize=(8, 5))
        plt.plot(x, y, label="Normal Distribution")
        plt.axvline(x=inventory, color="r", linestyle="--", label="Inventory Level")
        plt.axvline(
            x=inventory - (stockout_probability * std_dev),
            color="g",
            linestyle="--",
            label="Stockout Threshold",
        )
        plt.xlabel("Inventory Level")
        plt.ylabel("Probability Density")
        plt.title(f"Stockout Probability for {item}")
        plt.legend()
        plt.grid(True)
        plt.savefig(
            os.path.join(os.getcwd(), "graphs", f"{item}_stockout_probability.png")
        )
        plt.close()


clean()

df.to_csv("data_with_probabilities.csv", index=False)
generage_pngs()
