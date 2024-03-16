from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import math
import pickle



app = Flask(__name__)
popular_df = pickle.load(open('popular.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))

# def compute_similarity():
# global pt
# global books

@app.route('/')
def index1():
    return render_template("index.html")


@app.route('/other_page')
def other_page():
    rounded_ratings = [math.ceil(rating) for rating in popular_df['avg_ratings']]

    return render_template('mustread.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=rounded_ratings
                           # rating=list(popular_df['avg-ratings'].values)
     )


@app.route('/lists')
def lists():
    return render_template('list.html',

                           book_name=list(books['Book-Title'].values),
                           author=list(books['Book-Author'].values)
                         )


@app.route('/results')
def results():
    return render_template('recommend.html')


def compute_similarity(pt):
    # Convert pivot table to numpy array
    ratings_matrix = pt.to_numpy()

    # Initialize similarity score matrix
    similarity_score = np.zeros((ratings_matrix.shape[0], ratings_matrix.shape[0]))

    # Iterate over each pair of books
    for i in range(ratings_matrix.shape[0]):
        for j in range(ratings_matrix.shape[0]):
            if i == j:
                continue  # Skip if comparing the same book with itself

            # Get ratings vectors for the two books
            ratings_vec_i = ratings_matrix[i]
            ratings_vec_j = ratings_matrix[j]

            # Compute cosine similarity manually
            dot_product = np.dot(ratings_vec_i, ratings_vec_j)
            norm_vec_i = np.linalg.norm(ratings_vec_i)
            norm_vec_j = np.linalg.norm(ratings_vec_j)
            similarity_score[i, j] = dot_product / (norm_vec_i * norm_vec_j)

    return similarity_score


def recommend(book_name, pt, books, similarity_score):
    # Find index of the input book name in pt
    index = np.where(pt.index == book_name)[0][0]

    # Get indices and similarity scores of similar items
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:13]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return data


@app.route('/recommend', methods=['POST'])
def recommend_books():
    # Get user input from the form
    user_input = request.form.get('user_input')

    # Check if user input is missing or empty
    if not user_input:
        error_message = '**Please provide a valid book name**'
        return render_template('recommend.html', error_message=error_message)

    try:

        similarity_score = compute_similarity(pt)

        recommended_books = recommend(user_input, pt, books, similarity_score)

        if not recommended_books:
            error_message = 'Book not found'
            return render_template('recommend.html', error_message=error_message, user_input=user_input)
        else:
            return render_template('recommend.html', recommended_books=recommended_books, user_input=user_input)
    except IndexError:
        error_message = '**Book not found**'
        return render_template('recommend.html', error_message=error_message, user_input=user_input)

# @app.route('/recommend', methods=['POST'])
# def recommend_books():
#     # Get user input from the form
#     user_input = request.form.get('user_input')
#
#     # Check if user input is missing or empty
#     if not user_input:
#         error_message = 'Please provide a valid book name.'
#         return render_template('recommend.html', error_message=error_message)
#
#     # Compute similarity score
#     similarity_score = compute_similarity(pt)
#
#     # Get recommended books
#     recommended_books = recommend(user_input, pt, books, similarity_score)
#
#     if not recommended_books:
#         error_message = 'Book not found'
#         return render_template('recommend.html', error_message=error_message, user_input=user_input)
#     else:
#         return render_template('recommend.html', recommended_books=recommended_books, user_input=user_input)


# @app.route('/recommend', methods=['POST'])
# def recommend():
#     user_input = request.form.get('user_input')
#
#     try:
#         index = np.where(pt.index == user_input)[0][0]
#     except IndexError:
#         error_message = '**Book not found**'
#         return render_template('recommend.html', error_message=error_message,user_input=user_input)
#
#     # similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:13]
#     #
#     # data = []
#     #
#     # for i in similar_items:
#     #     item = []
#     #     temp_df = books[books['Book-Title'] == pt.index[i[0]]]
#     #     item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
#     #     item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
#     #     item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
#     #
#     #     data.append(item)
#     #
#     # return render_template('recommend.html', data=data, user_input=user_input)
#

@app.route('/autosuggest', methods=['POST'])
def autosuggest():
    query = request.form.get('query', '')

    suggestions = [book_name for book_name in pt.index if query.lower() in book_name.lower()]

    suggestions = suggestions[:5]

    suggestions_string = ', '.join(suggestions)

    return suggestions_string

trend_df = pickle.load(open('trending.pkl','rb'))
@app.route('/trend')
def trend():
    rounded_ratings = [math.ceil(rating) for rating in trend_df['avg-ratings']]

    return render_template('trending.html',
                           book_name=list(trend_df['Book-Title'].values),
                           author=list(trend_df['Book-Author'].values),
                           image=list(trend_df['Image-URL-M'].values),
                           genre=list(trend_df['Genre'].values),
                           des=list(trend_df['Description'].values),
                           votes=list(trend_df['num-ratings'].values),
                           rating=rounded_ratings


     )

f_df = pickle.load(open('f.pkl','rb'))
nf_df = pickle.load(open('nf.pkl','rb'))
s_df = pickle.load(open('s.pkl','rb'))
art_df = pickle.load(open('art.pkl','rb'))
h_df = pickle.load(open('h.pkl','rb'))
poetry_df = pickle.load(open('poetry.pkl','rb'))

@app.route('/f')
def f():
    return render_template('fiction.html',
                           book_name=list(f_df['title'].values),
                           author=list(f_df['author'].values),
                           image=list(f_df['img'].values),
                           des=list(f_df['desc'].values),
                           rating=list(f_df['rating'].values)
                           )
@app.route('/nf')
def nf():
    return render_template('nfiction.html',
                           book_name=list(nf_df['title'].values),
                           author=list(nf_df['author'].values),
                           image=list(nf_df['img'].values),
                           des=list(nf_df['desc'].values),
                           rating=list(nf_df['rating'].values)
                           )
@app.route('/h')
def h():
    return render_template('history.html',
                           book_name=list(h_df['title'].values),
                           author=list(h_df['author'].values),
                           image=list(h_df['img'].values),
                           des=list(h_df['desc'].values),
                           rating=list(h_df['rating'].values)
                           )
@app.route('/s')
def s():
    return render_template('science.html',
                           book_name=list(s_df['title'].values),
                           author=list(s_df['author'].values),
                           image=list(s_df['img'].values),
                           des=list(s_df['desc'].values),
                           rating=list(s_df['rating'].values)
                           )
@app.route('/art')
def art():
    return render_template('art.html',
                           book_name=list(art_df['title'].values),
                           author=list(art_df['author'].values),
                           image=list(art_df['img'].values),
                           des=list(art_df['desc'].values),
                           rating=list(art_df['rating'].values)
                           )
@app.route('/poetry')
def poetry():
    return render_template('poetry.html',
                           book_name=list(poetry_df['title'].values),
                           author=list(poetry_df['author'].values),
                           image=list(poetry_df['img'].values),
                           des=list(poetry_df['desc'].values),
                           rating=list(poetry_df['rating'].values)
                           )

if __name__ == ('__main__'):
        app.run(debug=True)