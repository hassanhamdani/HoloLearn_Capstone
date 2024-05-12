import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load the survey data
file_path = '/Users/hassan/Desktop/Hololearn data/XR HoloLearn Post Survey_April 30, 2024_10.34.csv'  # Update the file path here
survey_data = pd.read_csv(file_path)

# Define mappings for MARS ratings
response_mappings = {
     'Q01': {
        'Not interesting at all': 1,
        'Mostly uninteresting': 2,
        'OK, neither interesting nor uninteresting; would engage user for a brief time (< 5 minutes)': 3,
        'Moderately interesting; would engage user for some time (5-10 minutes total)': 4,
        'Very interesting, would engage user in repeat use': 5
    },
    'Q02': {
        'No interactive features and/or no response to user interaction': 1,
        'Insufficient interactivity, or feedback, or user input options, limiting functions': 2,
        'Basic interactive features to function adequately': 3,
        'Offers a variety of interactive features/feedback/user input options': 4,
        'Very high level of responsiveness through interactive features/feedback/user input options': 5
    },
    'Q03': {
        'Completely inappropriate/unclear/confusing': 1,
        'Mostly inappropriate/unclear/confusing': 2,
        'Acceptable but not targeted. May be inappropriate/unclear/confusing': 3,
        'Well-targeted, with negligible issues': 4,
        'Perfectly targeted, no issues found': 5
    },
    'Q04': {
        'App is broken; no/insufficient/inaccurate response (e.g., crashes/bugs/broken features, etc.)': 1,
        'Some functions work, but lagging or contains major technical problems': 2,
        'App works overall. Some technical problems need fixing/Slow at times': 3,
        'Mostly functional with minor/negligible problems': 4,
        'Perfect/timely response; no technical bugs found/contains a ‘loading time left’ indicator': 5
    },
    'Q05': {
        'No/limited instructions; menu labels/icons are confusing; complicated': 1,
        'Useable after a lot of time/effort': 2,
        'Useable after some time/effort': 3,
        'Easy to learn how to use the app (or has clear instructions)': 4,
        'Able to use app immediately; intuitive; simple': 5
    },
    'Q06': {
        'Completely inconsistent/confusing': 1,
        'Often inconsistent/confusing': 2,
        'OK with some inconsistencies/confusing elements': 3,
        'Mostly consistent/intuitive with negligible problems': 4,
        'Perfectly consistent and intuitive': 5
    },
    'Q07': {
        'Very bad design, cluttered, some options impossible to select/locate/see/read device display required': 1,
        'Bad design, random, unclear, some options difficult to select/locate/see/read': 2,
        'Satisfactory, few problems with selecting/locating/seeing/reading items or with minor screen size issues': 3,
        'Mostly clear, able to select/locate/see/read items': 4,
        'Professional, simple, clear, orderly, logically organized, device display optimized. Every design detail considered': 5
    },
    'Q08': {
        'Graphics appear amateur, very poor visual design - disproportionate, completely stylistically inconsistent': 1,
        'Low quality/low-resolution graphics; low-quality visual design – disproportionate, stylistically inconsistent': 2,
        'Moderate quality graphics and visual design (generally consistent in style)': 3,
        'High quality/resolution graphics and visual design – mostly proportionate, stylistically consistent': 4,
        'Very high quality/resolution graphics and visual design - proportionate, stylistically consistent': 5
    },
    'Q09': {
        'No visual appeal, unpleasant to look at, poorly designed, clashing/mismatched colors': 1,
        'Little visual appeal – poorly designed, bad use of color, visually boring': 2,
        'Some visual appeal – average, neither pleasant nor unpleasant': 3,
        'High level of visual appeal – seamless graphics – consistent and professionally designed': 4,
        'As above + very attractive, memorable, stands out; use of color enhances app features/menus': 5
    },
    'Q10': {
        'N/A There is no information within the app': 1,
        'Irrelevant/inappropriate/incoherent/incorrect': 2,
        'Poor. Barely relevant/appropriate/coherent/may be incorrect': 3,
        'Moderately relevant/appropriate/coherent/and appears correct': 4,
        'Highly relevant, appropriate, coherent, and correct': 5
    },
    'Q11': {
        'N/A There is no information within the app': 1,
        'Minimal or overwhelming': 2,
        'Insufficient or possibly overwhelming': 3,
        'OK but not comprehensive or concise': 4,
        'Offers a broad range of information, has some gaps or unnecessary detail; or has no link to more information and resources': 5
    },
    'Q12': {
        'N/A There is no visual information within the app (e.g., it only contains audio or text)': 1,
        'Completely unclear/confusing/wrong or necessary but missing': 2,
        'Mostly unclear/confusing/wrong': 3,
        'OK but often unclear/confusing/wrong': 4,
        'Mostly clear/logical/correct with negligible issues': 5
    }
}

# Apply mappings to the data
for question, mapping in response_mappings.items():
    survey_data[question] = survey_data[question].map(mapping)

# Calculate the mean scores for each MARS section
mean_scores = {
    'Engagement': survey_data[['Q01', 'Q02', 'Q03']].mean(axis=1).mean(),
    'Functionality': survey_data[['Q04', 'Q05', 'Q06']].mean(axis=1).mean(),
    'Aesthetics': survey_data[['Q07', 'Q08', 'Q09']].mean(axis=1).mean(),
    'Information': survey_data[['Q10', 'Q11', 'Q12']].mean(axis=1).mean()
}

# Plotting the combined average scores with color alternation
fig, ax = plt.subplots()
categories = ['Engagement', 'Functionality', 'Aesthetics', 'Information']
scores = [mean_scores['Engagement'], mean_scores['Functionality'], mean_scores['Aesthetics'], mean_scores['Information']]
colors = ['#4D4DFF', '#C724B1', '#4D4DFF', '#C724B1']  # Alternating colors

ax.bar(categories, scores, color=colors)
ax.set_xlabel('MARS Sections')
ax.set_ylabel('Average Rating')
#ax.set_title('Average Ratings Across MARS Sections')
ax.set_ylim(0, 5)

plt.show()

# Select the text-based response columns, assuming they end with 'a'
# Assuming metadata is in the first few rows; adjust as necessary if different
metadata_rows = 2  # Update this if the number of metadata rows differs
survey_data = survey_data.iloc[metadata_rows:]  # Skip metadata rows

# Select the text-based response columns, assuming they end with 'a'
text_columns = [col for col in survey_data.columns if col.endswith('a')]
textual_comments = survey_data[text_columns]

# Combine all textual comments into a single string, excluding specific words
excluded_words = {'comments', 'better', 'sometimes'}  # Set of words to exclude
filtered_comments = ' '.join([word for item in textual_comments.values.flatten() if pd.notna(item) for word in item.split() if word.lower() not in excluded_words])

# Define a custom color function to alternate colors
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "#4D4DFF" if random_state.randint(0, 1) else "#C724B1"

# Generate and display the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white', color_func=color_func).generate(filtered_comments)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
#plt.title("Word Cloud of Textual Comments in Application Survey")
plt.show()


q13_counts = survey_data['Q13'].value_counts()
colors = ['#4D4DFF', '#C724B1', '#D3D3D3', '#A9A9A9']  # Specified colors

# Create the pie chart
plt.figure(figsize=(8, 6))
plt.pie(q13_counts, autopct='%1.1f%%', startangle=140, colors=colors)
#plt.title('Would You Recommend the App?')
plt.legend(q13_counts.index, title="Recommendation Level", loc="lower center", bbox_to_anchor=(0.5, -0.3))
plt.show()