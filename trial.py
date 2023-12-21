import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import kdtree
dimensions = 70
num_vectors = 1000000

# Generate a random sample of points in a 70-dimensional space
data = np.random.rand(num_vectors, dimensions)

def distance(v1, v2 ) :
        return 1 - cosine_similarity([v1], [v2])[0][0]

class VectorIndexingSystemKDTree:
    def __init__(self, vectors):
        self.vectors = vectors
        self.kd_tree = kdtree.create(self.vectors)

    def retrieve_similar_vectors(self, query_vector, top_k=3 ):
        return self.kd_tree.search_knn(query_vector, top_k,distance)
    
data = data.tolist()

def distance(v1, v2 ) :
        return 1 - cosine_similarity([v1], [v2])[0][0]

class VectorIndexingSystemKDTree:
    def __init__(self, vectors):
        self.vectors = vectors
        self.kd_tree = kdtree.create(self.vectors)

    def retrieve_similar_vectors(self, query_vector, top_k=10 ):
        return self.kd_tree.search_knn(query_vector, top_k,distance)
    
def get_distance(vector1, vector2):
    return cosine_similarity([vector1], [vector2])[0][0]

query_vector = np.random.rand(3)  # Replace with your actual query vector
query_vector = query_vector.tolist()
print(query_vector)

def distance(v1, v2 ) :
        return 1 - cosine_similarity([v1], [v2])[0][0]

class VectorIndexingSystemKDTree:
    def __init__(self, vectors):
        self.vectors = vectors
        self.kd_tree = kdtree.create(self.vectors)

    def retrieve_similar_vectors(self, query_vector, top_k=10 ):
        return self.kd_tree.search_knn(query_vector, top_k,distance)
    
# Create an instance of the indexing system with some vectors
vectors_in_database = data  # Replace with your actual vectors
indexing_system = VectorIndexingSystemKDTree(vectors_in_database)
#print(indexing_system.kd_tree.height())

# for i in indexing_system.kd_tree.my_dict:
#     print(i)
print(indexing_system.kd_tree.my_dict)


# top_k_results = indexing_system.retrieve_similar_vectors(query_vector, top_k=3)

# # print(get_distance(top_k_results[0].data, query_vector))
# # Print the results
# print(f"Top {len(top_k_results)} Similar Vectors:")
# for similarity in top_k_results:
#     print(get_distance(similarity[0].data, query_vector))

# mx = float('-inf')
# for x in indexing_system.kd_tree.preorder():
#     mx = max(x.idA, mx)

# print(mx)