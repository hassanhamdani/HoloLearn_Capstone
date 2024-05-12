import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('/Users/hassan/Desktop/Hololearn data/HoloLearn Pre-Study Survey_April 30, 2024_07.54.csv')

# Clean the data
data_cleaned = data[2:]  # Adjust this if your data has different rows for headers or metadata

# Generate counts for Q14
q14_counts = data_cleaned['Q14'].dropna().value_counts()

# Define colors for the pie chart wedges
colors = ['#4D4DFF', '#C724B1', '#AB24C7']

# Create a pie chart without labels on the pie slices
fig, ax = plt.subplots()
wedges, texts = ax.pie(q14_counts, startangle=90, colors=colors)

# Equal aspect ratio ensures that pie is drawn as a circle.
ax.axis('equal')

# Add a legend with the labels.
plt.legend(wedges, q14_counts.index, loc="lower center",  bbox_to_anchor=(0, -0.1,1,1))

#plt.title('Frequency of Using VR Technology')
plt.show()
