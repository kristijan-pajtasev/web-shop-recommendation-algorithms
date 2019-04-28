from sklearn.neighbors import NearestNeighbors
import numpy
import pandas
import math


def knn(products, product):
    dataset = numpy.array(products)[:, -3:]
    model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=5, n_jobs=-1)

    model.fit(dataset)

    target = numpy.array(product)[-3:]

    predicted = model.kneighbors(numpy.array([target]), n_neighbors=5 + 1)

    recommended = []
    for id in list(predicted[1][0]):
        recommended.append(products[id][0])

    return recommended


