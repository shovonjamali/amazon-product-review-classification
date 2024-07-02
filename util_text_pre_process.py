import pandas as pd
import string
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

def create_count_table(table_df, df, product_category):
    # Calculate value counts
    value_counts = df['overall'].value_counts().reset_index()
    value_counts.columns = ['Value', 'Count']

    # Create a DataFrame with all possible values as columns
    table_data = {str(value): value_counts[value_counts['Value'] == value]['Count'].values[0] if value in value_counts['Value'].values else 0
                  for value in sorted(df['overall'].unique(), reverse=True)}

    # Add a total count column
    table_data['Total'] = sum(table_data.values())

    # Add a column for the product category
    table_data['Product'] = product_category

    # Concatenate the new data frame with the existing one
    table_df = pd.concat([pd.DataFrame([table_data]), table_df], ignore_index=True)

    # Rearrange columns
    table_df = table_df[['Product', 'Total'] + [col for col in table_df if col not in ['Product', 'Total']]]

    return table_df


def remove_duplicate_reviews(df, subset_column='reviewText'):
    # Count the number of duplicate reviews before removal
    initial_duplicates = df.duplicated(subset=subset_column).sum()

    # Convert the specified column to lowercase
    df[subset_column] = df[subset_column].str.lower()

    # Remove duplicates based on the specified column
    df_no_duplicates = df.drop_duplicates(subset=subset_column)

    # Count the number of duplicate reviews after removal
    removed_duplicates = initial_duplicates - df_no_duplicates.duplicated(subset=subset_column).sum()

    return df_no_duplicates, removed_duplicates


def detect_missing_values(df):
    # Check if there are any missing values
    has_missing_values = df.isnull().any().any()

    # Calculate the total number of missing values
    total_missing_values = df.isnull().sum().sum()

    return has_missing_values, total_missing_values


def remove_rows_with_missing_values(df, *columns):
    # Remove rows with any null values in the specified columns
    cleaned_df = df.dropna(subset=columns)

    return cleaned_df

def remove_stopwords(text):
  """
  Remove stopwords while performing the following tasks:
      - Text Classification
          - Spam Filtering
          - Language Classification
          - Genre Classification
      - Caption Generation
      - Auto-Tag Generation
  Avoid Stopword removal:
      - Machine Translation
      - Language Modeling
      - Text Summarization
      - Question-Answering problems
  """
  # Create a set of stop words
  stop_words = set(stopwords.words('english'))

  # Split the sentence into individual words
  words = word_tokenize(text.lower())
  # words = sentence.split()

  # Use a list comprehension to remove stop words
  filtered_words = [word for word in words if word not in stop_words]

  # Join the filtered words back into a sentence
  return ' '.join(filtered_words)

def lemmatize_text(text):
  word_list = []
  lemmatizer = WordNetLemmatizer()
  sentences = sent_tokenize(text)
  for sentence in sentences:
    words = word_tokenize(sentence)
    for word in words:
      word_list.append(lemmatizer.lemmatize(word))

  return ' '.join(word_list)

def clean_text(text):
    # Create a dictionary to map special characters to an empty string
    special_character_mapping = {special_char: '' for special_char in string.punctuation}

    # Add a mapping for space to space, as it won't be removed
    special_character_mapping[' '] = ' '

    # Create a translation table using str.maketrans with the dictionary
    translation_table = str.maketrans(special_character_mapping)

    # Apply the translation table to remove special characters
    text_no_special_chars = text.translate(translation_table)

    # Split the text into a list of words
    words = text_no_special_chars.split()

    # Join the words back into a string with space-separated words
    cleaned_text = ' '.join([word for word in words])

    # Convert the text to lowercase
    cleaned_text_lower = cleaned_text.lower()

    return cleaned_text_lower