import numpy as np
import pickle


pt = pickle.load(open('pt.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))
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
    pass


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
    pass