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

def test(request):
    with connection.cursor() as cursor:
        sql = '''
            SELECT product_id, product_width_cm, product_length_cm, product_height_cm  
            FROM olist.products 
            WHERE   product_width_cm is not null AND 
                    product_length_cm is not null AND 
                    product_height_cm is not null
        '''
        cursor.execute(sql)
        products = cursor.fetchall()
    recommended = knn(products)
    return HttpResponse(recommended)

