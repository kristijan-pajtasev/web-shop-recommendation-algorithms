from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from .algorithms import knn

# def my_custom_sql(self):
#     with connection.cursor() as cursor:
#         cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
#         cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
#         row = cursor.fetchone()
#
#     return row
# Create your views here.

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

