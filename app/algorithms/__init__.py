from sklearn.neighbors import NearestNeighbors
import numpy
import pandas
import math


def knn(products):
    dataset = numpy.array(products)[:, -3:]
    model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=5, n_jobs=-1)

    model.fit(dataset)

    predicted = model.kneighbors(numpy.array([[16.0, 10.0, 14.0]]), n_neighbors = 5 + 1)

    recommended = []
    for id in list(predicted[1][0]):
        recommended.append(products[id][0])

    return recommended


