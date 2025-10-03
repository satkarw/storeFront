from rest_framework import serializers
from store.models import Product, Collection, Review

from decimal import Decimal


class CollectionSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Collection
        fields = ['id','title','product_count']
    
    product_count = serializers.IntegerField(read_only = True)
    # product_count = serializers.SerializerMethodField(method_name = 'count_products')
        
    # def count_products(self,collection):
    #     return 
    
    
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title', 'slug', 'inventory','unit_price','collection','price_with_tax']
        
        # fields = '__all__'  #shows all field automatically 
    
    
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # unit_price = serializers.DecimalField(max_digits=6,decimal_places=2)
    
    price_with_tax = serializers.SerializerMethodField(method_name = 'calculate_tax')
    # collection  = serializers.PrimaryKeyRelatedField(
    #     queryset = Collection.objects.all()
    # )
    # # collection = serializers.StringRelatedField()
    # # collection = CollectionSerializer()
    
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name = 'collection-detail',
        
    # )

    def calculate_tax(self, product):
        return product.unit_price * Decimal(1.1)
    
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product
    
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get("unit_price")
    #     instance.save()
    #     return instance
    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','name','description','time','product_id']
    
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id = product_id,**validated_data)