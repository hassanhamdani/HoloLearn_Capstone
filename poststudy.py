import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Load data
file_path = '/Users/hassan/Desktop/Hololearn data/HoloLearn Post Survey_April 30, 2024_10.35.csv'
data = pd.read_csv(file_path)

# Rename columns to align with analysis requirements
data.rename(columns={"Confidence": "Q1", "Satisfaction": "Q22", "Relevance": "Q26"}, inplace=True)

# Define the full Likert scale mapping
likert_scale_mapping = {
    'Definitely false': 1, 'Probably false': 2, 'Neither true nor false': 3,
    'Probably true': 4, 'Definitely true': 5
}

# Map the survey responses to numeric scores
for col in data.columns:
    if col.startswith('Q'):
        data[col] = data[col].map(likert_scale_mapping)

# Adjust for negatively worded questions
negative_questions = ['Q2','Q6', 'Q8', 'Q13', 'Q14', 'Q17', 'Q20', 'Q21', 'Q33']
for q in negative_questions:
    if q in data.columns:
        data[q] = 6 - data[q]

# Segment data into treatment and control groups
treatment = data[data['Participant Info'].str.startswith('11')]
control = data[data['Participant Info'].str.startswith('10')]

# Define dimension-specific question columns correctly
dimension_questions = {
    'Confidence': ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9'],
    'Attention': ['Q10', 'Q11', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17', 'Q18', 'Q19', 'Q20', 'Q21'],
    'Satisfaction': ['Q22', 'Q23', 'Q24', 'Q25', 'Q26'],
    'Relevance': ['Q27', 'Q29', 'Q30', 'Q31', 'Q32', 'Q33', 'Q34', 'Q35']
}

# Calculate mean scores and perform t-tests
mean_scores_control = {}
mean_scores_treatment = {}
t_test_results = {}
for dim, questions in dimension_questions.items():
    mean_scores_control[dim] = control[questions].mean().mean()
    mean_scores_treatment[dim] = treatment[questions].mean().mean()
    t_stat, p_val = ttest_ind(treatment[questions].dropna().mean(axis=1),
                              control[questions].dropna().mean(axis=1), equal_var=False)
    t_test_results[dim] = (t_stat, p_val)

# Plotting the results
fig, ax = plt.subplots()
index = range(len(dimension_questions))
bar_width = 0.35

ax.bar(index, [mean_scores_control[dim] for dim in dimension_questions], bar_width, label='Control', color='#4D4DFF')
ax.bar([p + bar_width for p in index], [mean_scores_treatment[dim] for dim in dimension_questions], bar_width, label='Experimental', color='#C724B1')

ax.set_xlabel('Dimensions')
ax.set_ylabel('Scores')
#ax.set_title('Mean Scores by Dimension and Group')
ax.set_xticks([p + bar_width / 2 for p in index])
ax.set_xticklabels(list(dimension_questions.keys()))
ax.set_ylim(0, 4.2)  # Extending y-axis limit to 4
ax.legend(loc='upper right')  # Moving the legend outside the plot

#plt.tight_layout()  # Adjust layout to make room for legend
plt.show()
# Display t-test results up to 3 sig figs
for dim, (t_stat, p_val) in t_test_results.items():
    print(f'{dim}: t-statistic = {t_stat:.3f}, p-value = {p_val:.3f}')