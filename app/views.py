from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from .algorithms import knn, market_basket, customer_market_basket
from django.http import JsonResponse


def similar(request, product_id):
    print("PRODUCT ID %s" % product_id)

    with connection.cursor() as cursor:
        sql_all = '''
            SELECT product_id, product_width_cm, product_length_cm, product_height_cm  
            FROM olist.products 
            WHERE   product_width_cm is not null AND 
                    product_length_cm is not null AND 
                    product_height_cm is not null
        '''
        cursor.execute(sql_all)
        products = cursor.fetchall()
        product = [p for p in products if p[0] == product_id][0]
    recommended = knn(products, product)
    response = {}
    print(recommended)

    response['ids'] = list([p for p in recommended if p != product_id][:5])
    return JsonResponse(response)

GET_BASKET_SQL = "SELECT product_id FROM olist.shopping_cart WHERE customer_id=%s"

def basket(request, customer_id):
    print("CUSTOMER ID %s" % customer_id)

    with connection.cursor() as cursor:
        cursor.execute(GET_BASKET_SQL, [customer_id])
        products = cursor.fetchall()
        if len(products) == 0:
            return JsonResponse({"recommended": []})

        print("PRODUCTS FROM CART:")
        print(products)
        print(str(list(map(lambda x: x[0], products))).replace("[", "").replace("]", ""))
        product_ids = list(map(lambda x: x[0], products))
        product_ids_string = str(product_ids).replace("[", "").replace("]", "")

        sql_param = '''
            select O.order_id, O.product_id 
            from olist.orders as O 
            INNER JOIN (
                select distinct order_id 
                from olist.orders 
                where product_id IN (%s)
            ) as OD 
            ON O.order_id = OD.order_id
            group by O.order_id, O.product_id;
        ''' % product_ids_string
        print("sql", sql_param)
        print("product_ids", product_ids)
        print("product_ids_string", product_ids_string)

        cursor.execute(sql_param)
        orders = cursor.fetchall()
        print("orders", orders)
        results = market_basket(orders, product_ids)
        print("results", results)
    res = {}
    res['recommended'] = []
    for result in results:
        for product_id in result:
            if product_id not in res['recommended']:
                res['recommended'].append(product_id)
    return JsonResponse(res)
    return JsonResponse(response)

GET_CUSTOMER_BASKET_SQL = "SELECT product_id FROM olist.customer_product WHERE customer_id=%s"

def customer_basket(request, customer_id):
    print("CUSTOMER ID %s" % customer_id)

    with connection.cursor() as cursor:
        cursor.execute(GET_BASKET_SQL, [customer_id])
        products = cursor.fetchall()
        if len(products) == 0:
            return JsonResponse({"recommended": []})

        print("PRODUCTS FROM CART:")
        print(products)
        print(str(list(map(lambda x: x[0], products))).replace("[", "").replace("]", ""))
        product_ids = list(map(lambda x: x[0], products))
        product_ids_string = str(product_ids).replace("[", "").replace("]", "")

        sql_param = '''
            select O.customer_id, O.product_id 
            from olist.customer_product as O 
            INNER JOIN (
                select distinct customer_id 
                from olist.customer_product 
                where product_id IN (%s)
            ) as OD 
            ON O.customer_id = OD.customer_id
            group by O.customer_id, O.product_id;
        ''' % product_ids_string
        print("sql", sql_param)
        print("product_ids", product_ids)
        print("product_ids_string", product_ids_string)

        cursor.execute(sql_param)
        orders = cursor.fetchall()
        print("orders", orders)
        results = customer_market_basket(orders, product_ids)
        print("results", results)
    res = {}
    res['recommended'] = []
    for result in results:
        for product_id in result:
            if product_id not in res['recommended']:
                res['recommended'].append(product_id)
    return JsonResponse(res)

