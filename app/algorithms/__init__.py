from sklearn.neighbors import NearestNeighbors
import numpy
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


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


def market_basket(sales):

    # df = pd.io.parsers.read_csv("olist_order_items_dataset.csv")
    df = pd.DataFrame(sales, columns=["order_id","product_id"])

    df['amount'] = 1
    # df = df[:100]
    # print(df.values.size)
    #
    # print(df.head())

    basket = (df
              .groupby(['order_id', 'product_id'])['amount']
              .sum().unstack().reset_index().fillna(0)
              .set_index('order_id'))

    basket_sets = basket.head()
    print('basket_sets')
    print(basket_sets)

    frequent_itemsets = apriori(basket_sets, min_support=0.07, use_colnames=True)
    print('frequent itemsets')
    print(frequent_itemsets.head())

    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    print('rules')
    print(rules)

    filtered = rules[(rules['lift'] >= 6) &
          (rules['confidence'] >= 0.8)]
    print('filtered')
    print(filtered)
    # 6c90c0f6c2d89eb816b9e205b9d6a36a

    # print(basket['6c90c0f6c2d89eb816b9e205b9d6a36a'].sum())
    # print(basket['6c90c0f6c2d89eb816b9e205b9d6a36a'])
    return basket_sets
