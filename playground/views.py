from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product,Order,Customer,OrderItem,Collection
from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Max, Min, Avg
from django.db import transaction

from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItems, Tag

from django.db import connection
# Create your views here.

def say_hello(request):
    
    # queryset = Product.objects.filter(unit_price__range=(20,50))
    # queryset = Product.objects.all()
    # queryset =  Product.objects.filter(title__icontains = "novel")
    # products =  Product.objects.filter(collection_id_range = (1,2,3))
    
    
    # print("ok",list(queryset))
    # product = Product.objects.filter(pk=1 ).first()
    
    #multiple arguements
    # queryset =  Product.objects.filter(inventory__gt = 100, unit_price__lt = 80) #and operator 
    # queryset = Product.objects.filter(Q(inventory__lt = 100) | ~Q(unit_price__lt = 80))
    # queryset =  Product.objects.filter(inventory =  F('collection_id'))
    # queryset = Product.objects.order_by('unit_price','-title').reverse()
    
    # limiting results
    
    # queryset = Product.objects.all()[:5]
    # queryset = Product.objects.values('id','title','unit_price','inventory')
    
    ''' Exercise:  Select products that have been ordered and sort them by title '''
    # queryset = Product.objects.filter(id__in=Order.objects.filter(payment_status = 'C').values_list('id')).values('id','title','unit_price','inventory')
    queryset = Product.objects.prefetch_related('promotions').select_related('collection')
    orders = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]


    result = Product.objects.aggregate(count=Count('id'),min_price=Min('unit_price'))

    
    
    return render(request, 'hello.html',{'name':'satkar','products':list(queryset),'orders':orders,'result':result})

def another(request):
    
    customer = Customer.objects.annotate(is_new=Value(True))
    res = Product.objects.aggregate(count=Count('id'),min_price=Min('unit_price'))
    full_name = Customer.objects.annotate(full_name = Concat('first_name',Value(' '),'last_name') )
    
    
    #tagssss
    content_type = ContentType.objects.get_for_model(Product) #getting the contenttype id for pproduct model
    queryset = TaggedItems.objects.get_tags_for(Product, 1)
    
    
    return render(request,'another.html',{'res':res, 'customer':list(customer), 'tags':list(queryset)})

# @transaction.atomic() #this decorator will run this whole function as a transaction
def crud(request):
    """Creating a new collection"""
    # collection = Collection()
    # collection.title = 'Video Games'
    # collection.featured_product = Product(pk=1)
    # collection.save()    
    
    """another way"""
    # newCollection = Collection.objects.create(name='a',featured_product_id=1)

    "updating a existing collection"
    # collection = Collection.objects.get(pk=11)
    # # collection.title = "Games"
    # collection.featured_product = None
    # collection.save()
    
    """another way"""
    # Collection.objects.filter(pk=11).update(featured_product=None)

    """ Deleting Objects """
    #for one object
    # collection = Collection(pk=11)
    # collection.delete()
    
    #for a query set
    # Collection.objects.filter(id__gt=500).delete()
    
    """ Atomic Changes """
    #creating transaction
    
    # with transaction.atomic():
        
    #     order =  Order()
    #     order.customer_id = 1
    #     order.save()
        
    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = 1
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()
    
    """ Writing my own sql query """
    # queryset = Product.object.raw('SELECT * FROM store_product')
    
    # with connection.cursor() as cursor:
    #     cursor.execute()
        # cursor.callproc('get_customers',[1,2,'a'])
    
    
    return render(request, 'crud.html')