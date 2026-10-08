
from products.models import Product
from products.serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from django.views.decorators.cache import cache_page
from django.core.cache import cache
from datetime import timedelta


@api_view(['GET'])
def FunctionBasedProductListView(request):
    cached_products = cache.get('products')
    if cached_products:
        # cache hit
        return Response(cached_products, status=status.HTTP_200_OK)
    else:
        # cache miss
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        cache.set(
            'products',
            serializer.data,
            timedelta(minutes=10).total_seconds() # TTL
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def FunctionBasedProductDetailView(request, id):
    cached_product = cache.get(f'products-{id}')
    if cached_product:
        print("get data from cache")
        return Response(cached_product, status=status.HTTP_200_OK)
    
    print("get data from db")
    
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)
    cache.set(
        f'products-{id}',
        serializer.data,
        timedelta(minutes=10).total_seconds()
    )
    return Response(serializer.data, status=status.HTTP_200_OK)
