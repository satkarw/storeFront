from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from django.db.models import Count
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Collection,OrderItem,Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from rest_framework import status

#class based view imports
# from rest_framework.views import APIView
# from rest_framework.mixins import ListModelMixin, CreateModelMixin
# from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView

from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter

from rest_framework.filters import SearchFilter, OrderingFilter

# from rest_framework.pagination import PageNumberPagination
from .pagination import DefaultPagination

class ProductViewSet(ModelViewSet):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends =[DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title','description']
    ordering_fields = ['unit_price','last_update']
    def get_serializer_context(self):
        return {'request':self.request}
    
    def destroy(self,request,*args,**kwargs):   
        # product = get_object_or_404(Product,pk=pk)  
        if OrderItem.objects.filter(product_id = kwargs['pk']).count()  > 0:
            
            return Response({'error':'Product cannot be deleted '})
        
        return super().destroy(request,*args,**kwargs)
    

class CollectionViewSet(ModelViewSet):
    
    queryset = Collection.objects.annotate(product_count = Count('products')).all()
    serializer_class = CollectionSerializer
    
    def get_serializer_context(self):
        return {'request':self.request}


    def destroy(self, request, *args, **kwargs):
        # collection = self.get_object()
        
        if Product.objects.filter(collection = kwargs['pk']).count() > 0:
            return Response({'error':'collection has associated products'},status=status.HTTP_400_BAD_REQUEST)
            
        
        return super().destroy(request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk']) 
    
    serializer_class = ReviewSerializer 
    
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    
    def destroy(self, request, *args, **kwargs): 
        return super().destroy(request, *args, **kwargs)
    