import cv2
from scipy.spatial import cKDTree
import numpy as np
import pickle

def query_word(query, kdtree_path, page_map_path, top_n=10):
    kdtree = pickle.load(kdtree_path)
    page_map = pickle.load(page_map_path)

    distances, q_indices = kdtree.query(query, k = top_n)
    #print(distances)

    q_retrieval = list()
    for index in q_indices:
        word_images = list()
        for each in index:
            word_images.append(page_map[each])

        q_retrieval.append(word_images)

    return q_retrieval


if __name__ == "__main__":
    ann_file = "s_ann_file.txt"
    data_path = "data/small_set/"
    features_path = "features/feats.npy"

    features = np.load(features_path)
    ann_reader = open(ann_file, 'r')
    page_to_word = dict()
    word_matrix = list()

    counter = 0
    for line in ann_reader:
        img_name = line.strip().split(',')[0]
        word_matrix.append(features[counter]) 
        page_to_word[counter] = img_name

        counter += 1   

    kdtree = cKDTree(word_matrix)

    results = query_word(word_matrix[0:30], kdtree, page_to_word)

    queries = [page_to_word[i] for i in range(0, 30)]

    visualize_output(queries, results, data_path)
    pdb.set_trace()


  
    
    
