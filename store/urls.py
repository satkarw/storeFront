from django.urls import path,include
from . import views
from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_nested import routers


router = DefaultRouter()
router.register('products',views.ProductViewSet, basename='products')
router.register('collections',views.CollectionViewSet)


products_router = routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews')

urlpatterns = [
    path('',include(router.urls)),
    path('',include(products_router.urls))
]


''' 

# Remove top-level reviews route
# router.register('reviews', views.ReviewViewSet)  # <-- removed

# Nested router for product reviews
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
]



'''
