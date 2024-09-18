import time
import streamlit as st
import pandas as pd
from bertopic import BERTopic
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Download NLTK resources if not already present
# nltk.download('stopwords')
# nltk.download('punkt')
nltk.download('all')
# To make the app full width
st.set_page_config(layout="wide")

# Title of the app
st.title("Topic Taco 🌮: Bite-Sized Insights from Your CSV!")
        # The text you want to display
# Define the title text
#message = "Topic Taco 🌮: Bite-Sized Insights from Your CSV!"

# Create an empty container for the title
#title_container = st.empty()

# Simulate typing effect for the title
#for i in range(len(message) + 1):
#    title_container.markdown(f"# {message[:i]}")
#    time.sleep(0.05)  # Adjust the speed of the typing effect

# After the typing effect completes, you can display additional elements in your app
#st.write("Welcome to the BERTopic modeling application. Please upload your CSV file to get started.")
            
# Define preprocessing function
def preprocess_text(text, stop_words=None, bigram_mod=None, trigram_mod=None):
    if stop_words is None:
        stop_words = set(stopwords.words('english'))
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text)
    
    # Tokenize text into individual words
    tokens = word_tokenize(text)
    
    # Remove stop words
    filtered_tokens = [token for token in tokens if token not in stop_words]
    
    # Apply bigram and trigram models
    if bigram_mod:
        filtered_tokens = bigram_mod[filtered_tokens]
    if trigram_mod:
        filtered_tokens = trigram_mod[filtered_tokens]
    
    # Stem words
    stemmer = SnowballStemmer('english')
    stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
    
    # Optionally, remove short words
    min_word_length = 1
    long_tokens = [token for token in stemmed_tokens if len(token) >= min_word_length]
    
    # Join the tokens back into a single string
    processed_text = ' '.join(long_tokens)
    
    return processed_text

# Sidebar widgets
st.sidebar.header("Welcome to the BERTopic modeling application. Please upload your CSV file to get started.")
# File uploader widget
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Convert the file to a dataframe
    df = pd.read_csv(uploaded_file)
    
    # Sidebar selections
    st.sidebar.write("Data Summary:")
    st.sidebar.write(df.describe())  # Example: Show summary statistics
    
    # Allow user to specify the number of articles to analyze
    max_articles = len(df)
    num_articles = st.sidebar.slider(
        "Select the number of articles to analyze:",
        min_value=1,
        max_value=max_articles,
        value=min(100, max_articles)  # Default to 100 or max available rows
    )

    # Check for a column with text data
    text_column = st.sidebar.selectbox("Select the text column for topic modeling:", df.columns)
    
    # Dropdown menu for different types of visualizations
    viz_type = st.sidebar.selectbox("Select visualization type:", ["Word Cloud", "Topic Distribution", "Top Words per Topic"])

    # Add buttons to trigger and stop the analysis
    if st.sidebar.button("Run Analysis"):
        st.session_state['run_analysis'] = True
        st.session_state['stop_analysis'] = False

    if st.sidebar.button("Clear Results"):
        st.session_state['stop_analysis'] = True

    if st.session_state.get('run_analysis') and not st.session_state.get('stop_analysis'):
        if text_column:
            # Extract and preprocess text data
            documents = df[text_column].dropna().tolist()[:num_articles]
            stop_words = set(stopwords.words('english'))

            # The text you want to display
            message = "Preprocessing the text data...."

            # Create an empty container
            typing_effect = st.empty()

            # Simulate typing effect
            for i in range(len(message) + 1):
                typing_effect.text(message[:i])
                time.sleep(0.05)  # Adjust the speed of the typing effect

            preprocessed_documents = [preprocess_text(doc, stop_words) for doc in documents]
            bar = st.progress(50)
            time.sleep(3)
            bar.progress(100)
            # Apply BERTopic
            message = "Applying BERTopic model....."

            # Create an empty container
            typing_effect = st.empty()

            # Simulate typing effect
            for i in range(len(message) + 1):
                typing_effect.text(message[:i])
                time.sleep(0.05)  # Adjust the speed of the typing effect
            model = BERTopic()
            topics, probs = model.fit_transform(preprocessed_documents)
            with st.spinner(text="In progress"):
                time.sleep(3)
                st.success("Done")
            # Display the topics
            st.write("Topics Found:")
            topics_df = pd.DataFrame(model.get_topic_info())
            st.dataframe(topics_df)
            
            # Display Word Cloud
            if viz_type == "Word Cloud":
                st.write("Generating Word Cloud...")
                text = ' '.join(preprocessed_documents)
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
                plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                st.pyplot(plt)
            
            # Display Topic Distribution
            elif viz_type == "Topic Distribution":
                st.write("Visualizing Topic Distribution...")
                topic_freq = pd.Series(topics).value_counts().reset_index()
                topic_freq.columns = ['Topic', 'Frequency']
                fig = px.bar(topic_freq, x='Topic', y='Frequency', title='Topic Distribution')
                st.plotly_chart(fig)
            
            # Display Top Words per Topic
            elif viz_type == "Top Words per Topic":
                st.write("Visualizing Top Words per Topic...")
                topics = model.get_topics()
                top_words = {}
                for topic_num, words in topics.items():
                    top_words[topic_num] = ', '.join([word for word, _ in words[:10]])
                topic_df = pd.DataFrame(list(top_words.items()), columns=['Topic', 'Top Words'])
                fig = go.Figure(data=[go.Table(
                    header=dict(values=['Topic', 'Top Words']),
                    cells=dict(values=[topic_df['Topic'], topic_df['Top Words']])
                )])
                st.plotly_chart(fig)
else:
    st.sidebar.warning("Please upload a CSV file.")
