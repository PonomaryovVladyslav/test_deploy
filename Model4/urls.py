"""Model4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import LoginFormView, CreateUserView, ItemList, UserLogoutView, OrderCreateView, \
    OrderListView, RefundCreateView, ItemUpdateView, AddItemView, \
    ManageRefundView, RefundListView

urlpatterns = [
    path('', ItemList.as_view(), name='item_list'),
    path('admin/', admin.site.urls),
    path('login/', LoginFormView.as_view(), name='login'),
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('catalog/', ItemList.as_view(), name='item_list'),
    path('logout/', UserLogoutView.as_view(), name='item_list'),
    path('buy/', OrderCreateView.as_view(), name='buy'),
    path('orderlist/', OrderListView.as_view(), name='orders'),
    path('refund/', RefundCreateView.as_view(), name='refund'),
    path('edit/<int:pk>/', ItemUpdateView.as_view(), name='edit'),
    path('add/', AddItemView.as_view(), name='add'),
    path('refunds/', RefundListView.as_view(), name='refunds'),
    path('approve/<int:pk>/', ManageRefundView.as_view(), name='refund_approval')
]
