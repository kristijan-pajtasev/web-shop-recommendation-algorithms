from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from .algorithms import knn, market_basket


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

        sql_product = '''select product_id, product_width_cm, product_length_cm, product_height_cm 
                        from olist.products where product_id = %s'''
        cursor.execute(sql_product, [product_id])
        product = cursor.fetchone()
    recommended = knn(products, product)
    return HttpResponse(recommended)

def basket(request, order_id):
    print("ORDER ID %s" % order_id)

    with connection.cursor() as cursor:
        sql_all = '''
            select O.order_id, O.product_id 
            from olist.orders as O 
            INNER JOIN (
                select distinct order_id 
                from olist.orders 
                where product_id=%s
            ) as OD 
            ON O.order_id = OD.order_id
            group by O.order_id, O.product_id;
        '''
        cursor.execute(sql_all, ['e95ee6822b66ac6058e2e4aff656071a'])
        orders = cursor.fetchall()
        results = market_basket(orders)

    return HttpResponse(results)

