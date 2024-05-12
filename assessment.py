import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, norm
import statsmodels.api as sm

# Load the dataset
file_path = '/Users/hassan/Downloads/HoloLearn Assessment_April 27, 2024_05.48.csv'
data = pd.read_csv(file_path)

# Clean the dataset (assuming the first two rows are metadata)
cleaned_data = data[2:]
cleaned_data['QID36'] = cleaned_data['QID36'].astype(int)
cleaned_data['SC0'] = pd.to_numeric(cleaned_data['SC0'], errors='coerce')

# Remove specific IDs
filtered_data = cleaned_data[~cleaned_data['QID36'].isin([2222, 1101])]

# Separate into control and treatment groups based on ID prefixes
control_group = filtered_data[filtered_data['QID36'].astype(str).str.startswith('10')]
treatment_group = filtered_data[filtered_data['QID36'].astype(str).str.startswith('11')]

# Descriptive statistics
control_stats = control_group['SC0'].describe()
treatment_stats = treatment_group['SC0'].describe()

# Perform a t-test
t_stat, p_value = ttest_ind(control_group['SC0'].dropna(), treatment_group['SC0'].dropna())

# Calculating normal distributions
control_mean = control_group['SC0'].mean()
control_std = control_group['SC0'].std()

treatment_mean = treatment_group['SC0'].mean()
treatment_std = treatment_group['SC0'].std()

# KDE and Normal Distribution Plot
sns.set(style="white")
plt.figure(figsize=(12, 8))
sns.kdeplot(control_group['SC0'].dropna(), color="#4D4DFF", fill= True, label='Control Group KDE')
sns.kdeplot(treatment_group['SC0'].dropna(), color="#C724B1", fill= True, label='Experimental Group KDE')

# Plot normal distribution
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
control_norm = norm.pdf(x, control_group['SC0'].mean(), control_group['SC0'].std())
treatment_norm = norm.pdf(x, treatment_group['SC0'].mean(), treatment_group['SC0'].std())
plt.plot(x, control_norm, color="#4D4DFF", linestyle='--', label='Control Group Normal')
plt.plot(x, treatment_norm, color="#C724B1", linestyle='--', label='Experimental Group Normal')

# Defining the vertical offset
vertical_offset = max(control_norm) * 0.02  # Adjust this factor to change the height of the annotation

# Annotating the mean values on the plot
plt.text(control_mean, max(control_norm) + vertical_offset, '{:.2f}'.format(control_mean), horizontalalignment='center', color="#4D4DFF")
plt.text(treatment_mean, max(treatment_norm) + vertical_offset, '{:.2f}'.format(treatment_mean), horizontalalignment='center', color="#C724B1")

#plt.title('KDE and Normal Distribution of Control vs. Treatment Groups')
plt.xlabel('Score')
plt.ylabel('Density')
plt.legend()
plt.show()

# Regression analysis
control_group['Intercept'] = 1
treatment_group['Intercept'] = 1

# Fit the regression model
control_model = sm.OLS(control_group['SC0'], control_group[['Intercept']])
treatment_model = sm.OLS(treatment_group['SC0'], treatment_group[['Intercept']])
control_results = control_model.fit()
treatment_results = treatment_model.fit()

# Print the regression summary
print(control_results.summary())
print(treatment_results.summary())

# Create a data frame for the results
results_df = pd.DataFrame({
    'Group': ['Control', 'Treatment'],
    'Mean': [control_mean, treatment_mean],
    'Std Dev': [control_std, treatment_std],
    'T-Stat': [t_stat, np.nan],
    'P-Value': [p_value, np.nan]
})

# Display the results
print(results_df)

# Calculate the T-test statistic
t_stat, p_value = ttest_ind(control_group['SC0'].dropna(), treatment_group['SC0'].dropna())

# Display the T-test results
print(f'T-Statistic: {t_stat:.3f}')
print(f'P-Value: {p_value:.3f}')

# Add the T-Test stats to the
results_df['T-Stat'] = [t_stat, np.nan]
results_df['P-Value'] = [p_value, np.nan]

# Display the updated results
print(results_df)

# Boxplot without p-value
plt.figure(figsize=(10, 6))
sns.boxplot(data=[control_group['SC0'].dropna(), treatment_group['SC0'].dropna()], width=0.5)
sns.swarmplot(data=[control_group['SC0'].dropna(), treatment_group['SC0'].dropna()], color='black')
plt.title('Boxplot of Scores')
plt.xlabel('Group')
plt.ylabel('Scores')
plt.xticks([0, 1], ['Control', 'Treatment'])
plt.show()

# Difference plot
plt.figure(figsize=(10, 6))
sns.pointplot(x=['Control', 'Treatment'], y=[control_mean, treatment_mean], color='black')
plt.title('Mean Scores by Group')
plt.xlabel('Group')
plt.ylabel('Mean Score')
plt.show()

# Violin plot with split violins and
plt.figure(figsize=(10, 6))
sns.violinplot(x='QID36', y='SC0', data=filtered_data, split=True, inner='quartile')
plt.title('Violin Plot of Scores by Group')
plt.xlabel('Group')
plt.ylabel('Scores')
plt.xticks([0, 1], ['Control', 'Treatment'])
plt.show()


# Boxplot with p-value
plt.figure(figsize=(10, 6))
sns.boxplot(data=[control_group['SC0'].dropna(), treatment_group['SC0'].dropna()], width=0.5)
sns.swarmplot(data=[control_group['SC0'].dropna(), treatment_group['SC0'].dropna()], color='black')
plt.title('Boxplot of Scores with P-Value Annotation')
plt.xlabel('Group')
plt.ylabel('Scores')
plt.xticks([0, 1], ['Control', 'Treatment'])
plt.text(0.5, max(control_group['SC0'].max(), treatment_group['SC0'].max()) + 1, 'p-value = {:.3f}'.format(p_value), ha='center', va='bottom', color='red')
plt.show()
