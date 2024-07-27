import pandas as pd
import numpy as np
import math
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from flask import Flask, request, jsonify
from flask_cors import CORS

nltk.download('stopwords')
nltk.download('punkt')

file_path = 'New Places in Jakarta Clean.csv'
data = pd.read_csv(file_path)

data['combined_info'] = data['Description'] + ' ' + data['Ambience'].str.replace(',', ' ')

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preprocess_text(text):
    words = word_tokenize(text.lower())
    filtered_words = [stemmer.stem(word) for word in words if word not in stop_words]
    return ' '.join(filtered_words)

data['processed_info'] = data['combined_info'].apply(preprocess_text)

sentences = data['processed_info'].apply(lambda x: x.split())
model = Word2Vec(sentences=sentences, vector_size=100, window=5, min_count=1, workers=4)

def get_average_word2vec(sentence, model):
    words = sentence.split()
    word_vecs = [model.wv[word] for word in words if word in model.wv]
    if len(word_vecs) == 0:
        return np.zeros(model.vector_size)
    return np.mean(word_vecs, axis=0)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lat2 - lon1)
    a = (math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

user_lat = -6.311272
user_lon = 106.793541

def calculate_distance(row):
    return haversine(user_lat, user_lon, row['Latitude'], row['Longitude'])

data['Distance'] = data.apply(calculate_distance, axis=1)

def recommend_place_with_word2vec(user_input, data, top_n=10):
    user_input_vec = get_average_word2vec(preprocess_text(user_input), model)

    def get_word2vec_similarity(row):
        combined_vec = get_average_word2vec(row['processed_info'], model)
        return cosine_similarity([user_input_vec], [combined_vec])[0][0]

    data['Similarities'] = data.apply(get_word2vec_similarity, axis=1)

    recommendations = data.sort_values(by=['Similarities', 'Distance'], ascending=[False, True]).head(top_n)
    return recommendations[['Name', 'Location', 'Description', 'Ambience', 'Distance', 'Similarities']].to_dict(orient='records')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/request', methods=['POST'])
def handle_request():
    request_data = request.get_json()
    text = request_data.get('text')
    recommendations = recommend_place_with_word2vec(text, data)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
