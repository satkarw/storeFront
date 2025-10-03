# This code snippet is a part of a Django project where models are being registered with the Django
# admin site. Let's break down the code:
from django.contrib import admin
from .  import models
from django.db.models import Count 
from django.urls import reverse
from django.utils.html import format_html,urlencode
from django.db.models import F

# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    
    def lookups(self, request, model_admin):
        return [
            ('<10','Low')
        ]
    def queryset(self, request, queryset):
        
        if self.value() == '<10':
            return queryset.filter(inventory__lt = 10)
        


    
    
    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # fields = ['title','slugs'] #this edits the form
    # exclude = [] #remove some fields
    # readonly
    
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug':['title']
    }
    
    actions = ['clear_inventory', 'update_inventory']
    list_display = ['title','unit_price','inventory_status','collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection','last_update',InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title']
    
    def collection_title(self,product):
        return product.collection.title
    
    #computed fields
    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'Low'
        else:
            return 'OK'
        
    @admin.action(description='Clear Inventory')
    def clear_inventory(self,request,queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} Products were successfully updated'
        )
    
    @admin.action(description='Update Inventory')
    def update_inventory(self,request, queryset):
        updated_count = queryset.update(inventory=100)
        self.message_user(
            request,
            f'{updated_count} Products were successfully updated' 
        )
        

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership']
    list_editable = ['membership']
    search_fields = ['first_name__istartswith','last_name__istartswith']

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    search_fields = ['title']
    
    @admin.display(ordering='products_count')
    def products_count(self,collection):
        
        url =( reverse('admin:store_product_changelist') 
            + '?'
            + urlencode({
                'collection_id':str(collection.id)
            }))
        
        return format_html('<a href="{}">{}</a>',url,collection.products_count)
        
            
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count = Count('product')
        )

# admin.site.register(models.Product, ProductAdmin)


class OrderItemInline(admin.TabularInline): #or StackedInline
    model = models.OrderItem
    
    autocomplete_fields = ['product']
    extra = 0
    min_num=1
    max_num = 10
    


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    # search_fields = ['customer']
    list_display = ['id', 'placed_at_formatted', 'customer', 'product_list']
    list_select_related = ['customer']
    autocomplete_fields = ['customer']
    
    inlines = [OrderItemInline]

    @admin.display(description="Placed At", ordering="placed_at")
    def placed_at_formatted(self, order):
        return order.placed_at.strftime("%Y/%m/%d %H:%M")

    def product_list(self, order):
        return ", ".join([item.product.title for item in order.orderitem_set.all()])
    

@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','product','quantity','amount']
    list_select_related =['product','order']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(amount_value = F('quantity') * F('unit_price'))
    
    @admin.display(description='Amount',ordering='amount_value')
    def amount(self,order_item):
        return order_item.quantity * order_item.unit_price
        