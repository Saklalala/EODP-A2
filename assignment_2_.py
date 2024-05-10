# -*- coding: utf-8 -*-
"""Assignment 2 .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1--BWFjtOaQc9fC-n659zvxTvYTzvtcYg
"""

# hi we can use this google colab to write our code part~
# plz write detailed comments to describe what the code does.
# In this way, it's not only convenient for us to understand the code to write the report, but also convenient for markers to go through our code

# import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""https://www.kaggle.com/datasets/ruchi798/bookcrossing-dataset/data
This is the link to the Kaggle website where we can find our data set

# Rearch Question: which factors have a relatively significant impact on book ratings

DATA PRE-PROCESSING
"""

# load data files
Books = pd.read_csv("BX-Books.csv")
Users = pd.read_csv("BX-Users.csv")
Ratings = pd.read_csv("BX-Ratings.csv")

# check whether there are missing values in books csv file--- no missing values
Books.isna().sum()
# check whether there are missing values in Ratings csv file--- no missing values
Ratings.isna().sum()
# check whether there are missing values in Users csv file--- there are missing values
Users.isna().sum()

# we find there no missing values in Books and Ratings csv files
# so we only need to handle missing values in Users csv file

# let's first draw the rating distribution to see what it looks like
# Set the style of the plot
sns.set_style("whitegrid")

# Plotting the rating distribution
plt.figure(figsize=(10, 6))
sns.histplot(data=Ratings, x='Book-Rating', bins=10)
plt.xlabel('Book Rating')
plt.ylabel('Frequency')
plt.title('Distribution of Book Ratings')
plt.show()

"""STRIP PUNCTUATION"""

# Pattern = all non numbers
# Age is numerical values only
Users['User-Age'] = Users['User-Age'].replace('[^0-9]','', regex = True)

# Pattern = all non alphabetic
# Country is alphabetical values only
Users['User-Country'] = Users['User-Country'].replace('[^a-zA-z ]+','', regex = True)





#USERS
# missing values in the City column will be removed.
# Allow for special characters in locations, since they can be different languages
# Validate City and  State are not "n/a"
Users.dropna(subset=['User-City'], inplace=True)
Users.drop(Users[Users['User-City'].str.contains('n/a')].index, inplace = True, errors = 'ignore')
Users.drop(Users[Users['User-State'].str.contains('n/a')].index, inplace = True, errors = 'ignore')

# check how many unique values in city/states/country column
# there are so many different values about cities and states  so we choose to use city feature to do analysis
unique_cities = Users['User-City'].nunique()
unique_states = Users['User-State'].nunique()
unique_countries = Users['User-Country'].nunique()

print(f"Number of unique cities: {unique_cities}")  # 9323 cities
print(f"Number of unique states: {unique_states}")  # 1074 cities
print(f"Number of unique countries: {unique_countries}")  # 169 countires

# the missing values can be reasonably inferred or filled based on other information in the dataset
# for example, we can use values in state column to infer corresponding missing countries values
existing_countries = Users.copy()  # Create a copy of the DataFrame with no missing values of countries
# Create a mapping of states to countries in the existing data
state_country_map = dict(zip(existing_countries['User-State'], existing_countries['User-Country']))
# Identify rows with missing or ' ' values in 'User-Country' column
missing_countries = Users[Users['User-Country'].isnull() | (Users['User-Country'] == ' ')]
# Iterate over missing countries and fill them based on the state-country map
for index, row in missing_countries.iterrows():
    if row['User-State'] in state_country_map:
        Users.at[index, 'User-Country'] = state_country_map[row['User-State']]
print(Users.isna().sum())  # then there are no missing values in Users' columns except for age column
Users.dropna(subset=['User-Country'], inplace=True)
print(Users.isna().sum())
# Drop cities where character is not alphabetical
Users.drop(Users[Users['User-City'].str.contains('^[0-9 -&*?.]' )].index, inplace = True, errors = 'ignore')
Users

# print the country column and find some countires'number counts are high and some countries' number counts are extreme low
print(Users['User-Country'].value_counts())
# so Let's rename every country that appears less than 500 times as 'others' to help us to visualsise the country distribution
country_counts = Users['User-Country'].value_counts()

# Filter countries with counts less than 500
countries_to_rename = country_counts[country_counts < 500].index.tolist()

# Map these countries to 'others'
Users['User-Country'] = Users['User-Country'].replace(countries_to_rename, 'others')

# let's visulise the User-Coutry distribution
# Plotting the bar chart
plt.figure(figsize=(10, 6))  # Adjust the figure size if needed
country_counts.plot(kind='bar')

# Set plot title and labels
plt.title('Distribution of Users by Country')
plt.xlabel('Country')
plt.ylabel('Number of Users')

# Show the plot
plt.show()

# Validate age 0 < x < 100, if outside range, turn to N/A
Users['User-Age'] = pd.to_numeric(Users['User-Age'], errors = 'coerce')

# Replace NaN values with missing values
missing_value = pd.NA
Users['User-Age'].fillna(missing_value, inplace=True)

# Filter rows where age is outside the specified range
Users['User-Age'].loc[(Users['User-Age'] >= 100)] = pd.NA
Users['User-Age'].loc[(Users['User-Age'] <= 0)] = pd.NA

# Convert 'User-Age' column to integer
Users['User-Age'] = Users['User-Age'].astype('Int64')

# Plotting the age distribution
plt.figure(figsize=(10, 6))
plt.hist(Users['User-Age'].dropna(), bins=5, color='skyblue', edgecolor='black')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title('Age Distribution of Users')
plt.grid(True)
plt.show()

"""DISCRETISING DATA (GROUPING DATA INTO CATEGORIES)"""

# discretize the data of age column into categories
# Fill missing values in 'User-Age' column with -1
Users['User-Age'] = Users['User-Age'].fillna(-1)
# Define the bin edges and labels
# use -1 to represent missing values of age rows ->we don't used data imputation with mean
# cuz there are so many missing values of age, hard to impuate them with one value to do analysis -> put them into one category to analyse
# use 1 to represent 0-20 age interval, 2 for 20-40 and so on
bins = [-1, 0, 20, 40, 60, 80, 100]
labels = [-1, 1, 2, 3, 4, 5]

# Discretize the 'User-Age' column into categories
Users['Age_Category'] = pd.cut(Users['User-Age'], bins=bins, labels=labels, right=False)

# Plot the histogram
plt.figure(figsize=(8, 6))
Users['Age_Category'].value_counts().sort_index().plot(kind='bar')
plt.xlabel('Age Category')
plt.ylabel('Count')
plt.title('Distribution of User Ages in Categories')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()
Users
#Discretise the rating column of rating csv file

"""Encoding the 'User-Country' column data -> convert them to numerical values for later model analysis
At here we use label encoding method, cuz the number of unique countries is very large, label encoding can be a more practical choice compared with on-hot encoding which will create a separate binary column for each country, resulting in a large number of columns. This can lead to the "curse of dimensionality" in machine learning, where the model's performance may suffer due to the increased number of features.
"""

# Import LabelEncoder from sklearn
from sklearn.preprocessing import LabelEncoder

# Initialize LabelEncoder
label_encoder = LabelEncoder()

# Encode 'User-Country' column
Users['User-Country_Encoded'] = label_encoder.fit_transform(Users['User-Country'])

# Check the encoded values and corresponding original values
encoded_values = pd.DataFrame({
    'Original_Country': Users['User-Country'],
    'Encoded_Country': Users['User-Country_Encoded']
})

# Display the encoded values for us to see what just happened
encoded_values

Users

# only keep features which we will used in later model training
Users_cleaned= Users[['User-ID','Age_Category','User-Country_Encoded']]
Users_cleaned
# data preprocessing of Users file is done

# Books and Ratings csv file data preprocessing
# Validate ISBN
# All ISBN are 10 characters long, and the last digit can be a number from 0 to 9 or the letter 'X', which represents the number 10.
# so i did some chaneges to keep the letter X
import re
# Define a regex pattern to match non-numeric characters except 'X' at the end
pattern = re.compile(r'[^0-9X]$')

Books.drop(Books[Books['ISBN'].str.contains(pattern)].index, inplace=True, errors='ignore')
Ratings.drop(Ratings[Ratings['ISBN'].str.contains(pattern)].index, inplace=True, errors='ignore')


# Year of publication (1920<x<2024)
Books.drop(Books[Books['Year-Of-Publication'] < 1920].index, inplace = True, errors = 'ignore')
Books.drop(Books[Books['Year-Of-Publication'] > 2024].index, inplace = True, errors = 'ignore')

# Drop rows with missing values in 'Year-Of-Publication' column
Books.dropna(subset=['Year-Of-Publication'], inplace=True)

# categorize the year of publication into groups and then plot them
# Define the bin edges and labels for categorization
# 1 to represent 1920-1940 interval, 2 to represent 1940-1960 interval and so on
bin_edges = [1920, 1940, 1960, 1980, 2000, 2024]
bin_labels = [1, 2, 3, 4, 5]

# Create a new column 'Publication-Decade' based on the bins
Books['Publication-Decade'] = pd.cut(Books['Year-Of-Publication'], bins=bin_edges, labels=bin_labels)

# Count the number of books in each publication decade
publication_counts = Books['Publication-Decade'].value_counts().sort_index()

# Plotting the bar chart
plt.bar(publication_counts.index, publication_counts.values, color='skyblue')

# Adding labels and title
plt.xlabel('Publication Decade')
plt.ylabel('Number of Books')
plt.title('Number of Books Published in Each Decade')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Display the plot
plt.show()

# we find a large number of books are concentrated between 1980 - 2024 from histogram below

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Initialize NLTK resources
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Define a function to preprocess textual data of titles/authors/publishers of Books csv file
def preprocess_text(text):
    # Remove special characters and convert to lowercase
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stopwords and perform stemming/lemmatization
    tokens = [stemmer.stem(token) for token in tokens if token not in stop_words]

    # Join tokens back into a string
    return ' '.join(tokens)

# Apply preprocessing to Book-Title, Book-Author, and Book-Publisher columns
Books['Book-Title'] = Books['Book-Title'].apply(preprocess_text)
Books['Book-Author'] = Books['Book-Author'].apply(preprocess_text)
Books['Book-Publisher'] = Books['Book-Publisher'].apply(preprocess_text)

# encoding the Book-Author and Book-publisher
from sklearn.preprocessing import LabelEncoder

# Initialize LabelEncoder
label_encoder = LabelEncoder()

# Encode Book-Author
Books['Encoded-Book-Author'] = label_encoder.fit_transform(Books['Book-Author'])

# Encode Book-Publisher
Books['Encoded-Book-Publisher'] = label_encoder.fit_transform(Books['Book-Publisher'])

# using the  TF-IDF vectorization to convert the textual data in the "Book-Title" column
# into a numerical format that can be used for machine learning models
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the 'Book-Title' column
tfidf_matrix = tfidf_vectorizer.fit_transform(Books['Book-Title'])

# Convert TF-IDF matrix to DataFrame
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())

# Print the TF-IDF matrix
print(tfidf_df)
# we find this is a  really high-dimensional feature space then we need to use PCA to reduce dimensionality

from gensim.models import Word2Vec
from sklearn.decomposition import PCA

# Tokenize book titles
tokenized_titles = Books['Book-Title'].apply(lambda x: x.split())

# Train Word2Vec model
word2vec_model = Word2Vec(sentences=tokenized_titles, vector_size=100, window=5, min_count=1, sg=0)

# Get Word2Vec embeddings for each title
def get_word2vec_embeddings(title, model):
    # Initialize an empty array to store word vectors
    embeddings = []
    for word in title:
        # Check if the word is in the Word2Vec vocabulary
        if word in model.wv.key_to_index:
            embeddings.append(model.wv[word])
    # Calculate the mean of word vectors for the title
    if embeddings:
        return pd.Series(np.mean(embeddings, axis=0))
    else:
        return pd.Series([0] * 100)  # If no embeddings found, return zeros

# Convert embedding list to DataFrame
word2vec_embeddings = tokenized_titles.apply(lambda x: get_word2vec_embeddings(x, word2vec_model))

# Initialize PCA with 1 component
pca = PCA(n_components=1)

# Fit PCA to Word2Vec embeddings
pca.fit(word2vec_embeddings)

# Transform Word2Vec embeddings to 1 dimension
word2vec_embeddings_pca = pca.transform(word2vec_embeddings)

# Calculate the percentage of variance explained by each component
explained_variance_ratio = pca.explained_variance_ratio_

print("Percentage of Variance Explained by PCA Component:", explained_variance_ratio)

# only keep columns which will be used in later models training
Books_cleaned = Books[['ISBN', 'Publication-Decade','Encoded-Book-Author','Encoded-Book-Publisher']]
Books_cleaned['embedding'] = word2vec_embeddings_pca
Books_cleaned



"""Merge Tables"""

# Merge Ratings table with Users table on 'User-ID'
ratings_users_merged = pd.merge(Ratings, Users_cleaned, on='User-ID', how='inner')

# Merge Books table with merged Ratings and Users table on 'ISBN'
final_merged_table = pd.merge(ratings_users_merged, Books_cleaned, on='ISBN', how='inner')

final_merged_table = final_merged_table.drop(['ISBN', 'User-ID'], axis=1)
# find there are 15 missing values in 'publication-decade' and drop them
final_merged_table.dropna(subset=['Publication-Decade'], inplace=True)

# then use a standard scaler to scale the numerical values in the columns of final merged table except for 'Book-Rating' column
# Standard scaling is important because it brings all features to a similar scale, which is essential for many machine learning algorithms.
# It prevents features with larger scales from dominating those with smaller scales, ensuring fair comparisons and accurate model training.
from sklearn.preprocessing import StandardScaler

# Get the numerical columns except 'Book-Rating'
numerical_columns = [col for col in final_merged_table.columns if col != 'Book-Rating']

# Initialize the StandardScaler
scaler = StandardScaler()

# Fit and transform the numerical columns
final_merged_table[numerical_columns] = scaler.fit_transform(final_merged_table[numerical_columns])

# Display the scaled numerical columns
final_merged_table

# Using a correlation matrix and heatmap helps identify multicollinearity which is the presence of highly correlated independent variables in a regression analysis.
# Multicollinearity can lead to several problems
# 1: When predictors are highly correlated, it becomes difficult for the model to estimate the individual effect of each predictor accurately.
# 2: Multicollinearity can cause coefficients to have high variability, making them sensitive to small changes in the data.
# This makes it challenging to interpret the impact of each predictor on the target variable consistently.
correlation_matrix = final_merged_table.corr()

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.show()
# find there are no clear multicollinearity bewtween each features, which is nice for us to estimate the individual effect of each predictor accurately.

"""**Using Linear Regression**"""

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Separate target variable (Book-Rating) and predictors (features)
X = final_merged_table.drop(['Book-Rating'], axis=1)  # Features
y = final_merged_table['Book-Rating']  # Target variable

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Choose a regressor (e.g., Linear Regression)
regressor = LinearRegression()

# Perform cross-validation on the training data
cv_scores = cross_val_score(regressor, X_train, y_train, cv=5, scoring='neg_mean_squared_error')

# Convert negative scores to positive and take the average
cv_scores_positive = -cv_scores
cv_mse_mean = cv_scores_positive.mean()

# Train the regressor on the entire training data
regressor.fit(X_train, y_train)

# Make predictions on the test data
y_pred = regressor.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Cross-validated Mean Squared Error (CV MSE): {cv_mse_mean}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"R-squared (R2): {r2}")

#Lower MSE and higher R-squared values indicate better performance.
#In this case, the MSE is relatively low but the R-squared value is also quite low,
# indicating that the linear regression model does not explain much of the variability in the data.

# Get the coefficients (feature importances) from the trained model
feature_importances = regressor.coef_

# Map feature names to their corresponding coefficients
feature_importance_dict = dict(zip(X.columns, feature_importances))

# Sort features by their importance (absolute values)
sorted_features = sorted(feature_importance_dict.items(), key=lambda x: abs(x[1]), reverse=True)

# Display feature importances
print("Feature Importances:")
for feature, importance in sorted_features:
    print(f"{feature}: {importance}")

# Optionally, you can visualize the feature importances using a bar plot
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.barh([x[0] for x in sorted_features], [abs(x[1]) for x in sorted_features])
plt.xlabel('Feature Importance (Absolute Value)')
plt.title('Feature Importances for Book Ratings')
plt.show()

"""# using decision tree regressor"""

from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, cross_val_score

# Split the data into features (X) and target (y)
X = final_merged_table.drop(['Book-Rating'], axis=1)
y = final_merged_table['Book-Rating']

# Initialize the Decision Tree Regressor
dt_regressor = DecisionTreeRegressor(random_state=42)

# Perform cross-validation with 5 folds
cv_scores = cross_val_score(dt_regressor, X, y, cv=5, scoring='neg_mean_squared_error')

# Convert negative scores to positive and take the average
cv_mse = -cv_scores.mean()

# Print the cross-validated Mean Squared Error (CV MSE)
print(f"Cross-validated Mean Squared Error (CV MSE): {cv_mse}")

# we get a bigger mse relative using linear regression, means it is not a good model to use
# compared with using decision tree, linear regression is a relatively better choice

#A higher Mean Squared Error (MSE) in the cross-validated Decision Tree Regressor model indicates that the model's predictions are further from the actual values compared to the Linear Regression model.
# This can affect the reliability of the feature importances obtained from the Decision Tree Regressor,
# as the model itself is not performing well in terms of prediction accuracy-> so i don't visualise feature importance in this model

# Define a function to map ratings to classes
def map_ratings_to_class(rating):
    if rating <= 4:
        return 0
    elif 5 <= rating <= 7:
        return 1
    else:
        return 2

# Apply the function to create a new column 'Rating-Class'
final_merged_table['Rating-Class'] = final_merged_table['Book-Rating'].apply(map_ratings_to_class)

"""**Using decision tree classification method**"""

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score

# Assuming your DataFrame is named final_merged_table

# Splitting the data into features (X) and target variable (y)
X = final_merged_table.drop(['Book-Rating', 'Rating-Class'], axis=1)  # Features are all columns except 'Book-Rating' and 'Rating-Class'
y = final_merged_table['Rating-Class']  # Target variable is 'Rating-Class'

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Decision Tree Classifier
clf = DecisionTreeClassifier(random_state=42)

# Fit the classifier to the training data
clf.fit(X_train, y_train)

# Make predictions on the test data
y_pred = clf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(classification_rep)

#The model performs relatively well for predicting higher ratings (class 2), with a higher precision, recall, and F1-score compared to the other classes.
# However, it struggles with lower ratings (class 0) and shows moderate performance for mid-range ratings (class 1).
#Overall, while the model can distinguish between the classes to some extent, there is room for improvement, especially in correctly identifying lower ratings.

# Plotting feature importance
plt.figure(figsize=(10, 6))
feat_importances = pd.Series(clf.feature_importances_, index=X.columns)
feat_importances.nlargest(6).plot(kind='barh')
plt.xlabel('Feature Importance')
plt.ylabel('Features')
plt.title(' Feature Importances Plot')
plt.show()

"""In summary, if the goal is prediction accuracy and the problem is classification (such as predicting classes like ratings), the decision tree classifier with an accuracy of 54% is comparatively better than the linear regression model, which has limited explanatory power (low R-squared) for the given data.

In linear regression, feature importance is determined by the coefficients assigned to each feature in the linear equation. Features with higher coefficients are considered more important in predicting the target variable.SO, in this situation, 'age' , 'country' and 'year of publication' are important factors to determine the book ratings

In decision tree classification, Decision trees assess feature importance based on how well they split the data to maximize information gain or decrease impurity.'Author', 'Publisher' and 'age'  might be crucial for creating meaningful splits in the data that help distinguish between different rating classes(low/medium/high).

we find in both models, 'age' both plays a crucial role in determing the book rating
"""

# Set the style of the plot
sns.set_style("whitegrid")

# Create a scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=final_merged_table, x='Age_Category', y='Book-Rating')

# Fit a linear regression line to the scatter plot
sns.regplot(data=final_merged_table, x='Age_Category', y='Book-Rating', scatter=False, color='red')

# Set the plot labels and title
plt.xlabel('Age Category')
plt.ylabel('Book Rating')
plt.title('Linear Relationship between Age Category and Book Rating')

# Show the plot
plt.legend(['Regression Line'])
plt.show()

# cuz the regression line slopes upwards from left to right,
# it indicates a positive correlation, suggesting that as age category increases, book ratings also tend to increase.
# As age increases, people are more likely to give books higher ratings