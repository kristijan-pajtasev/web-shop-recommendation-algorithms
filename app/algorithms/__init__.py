from sklearn.neighbors import NearestNeighbors
import numpy
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.preprocessing import StandardScaler

def knn(products, product):
    dataset = numpy.array(products)[:, -3:]
    target = numpy.array(products)[:, 0:1]

    index = list(target.flatten()).index(product[0])

    model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=5, n_jobs=-1)

    standard_scaler = StandardScaler()
    dataset = standard_scaler.fit_transform(dataset)

    model.fit(dataset)

    target = dataset[index]
    predicted = model.kneighbors(numpy.array([target]), n_neighbors=5 + 1)

    recommended = []
    for id in list(predicted[1][0]):
        recommended.append(products[id][0])

    return recommended


def market_basket(sales, product_ids):

    # df = pd.io.parsers.read_csv("olist_order_items_dataset.csv")
    df = pd.DataFrame(sales, columns=["order_id","product_id"])

    df['amount'] = 1

    basket = (df
              .groupby(['order_id', 'product_id'])['amount']
              .sum().unstack().reset_index().fillna(0)
              .set_index('order_id'))

    basket_sets = basket.head()
    print('basket_sets')
    print(basket_sets)

    frequent_itemsets = apriori(basket, min_support=0.07, use_colnames=True)
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

    print("ANTECEDENTS")
    print(rules['antecedents'])
    # target = rules[(rules['antecedents'] == {product_ids[0]})]
    target = rules[(rules['antecedents'] == set(product_ids))]
    print('target')
    print(target)

    consequents = target.sort_values(by=['confidence'], ascending=False)['consequents']

    results = []
    for recommended in consequents.values:
        results.append(list(recommended))
    return results
