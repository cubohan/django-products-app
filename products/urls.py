from django.conf.urls import url

from views import ProductListView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^', login_required(ProductListView.as_view()), name='product-list'),
]
