from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import User, Item, Order, Refund
from .forms import UserCreateForm, OrderCreateForm, RefundCreateForm


class MyLoginRequiredMixin(LoginRequiredMixin):
    """Check if user is superuser"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class LoginFormView(LoginView):
    """"Login form"""
    http_method_names = ['get', 'post']
    template_name = 'login.html'

    def get_success_url(self):
        url = '/catalog/'
        return url


class CreateUserView(CreateView):
    """Sign up form"""
    form_class = UserCreateForm
    template_name = 'signup.html'
    http_method_names = ['get', 'post']
    success_url = '/catalog/'


class OrderCreateView(CreateView, LoginRequiredMixin):
    """Order submit"""
    form_class = OrderCreateForm
    success_url = '/orderlist/'
    template_name = 'item_list.html'
    http_method_names = ['get', 'post']
    login_url = '/login/'

    def form_valid(self, form):
        order = form.save(commit=False)
        item_id = self.request.POST.get('item_id')
        item = Item.objects.get(id=item_id)
        order.item = item

        if self.request.user.is_authenticated:
            """"Check if user is logged in"""
            order.user = self.request.user
            if item.amount_available >= order.amount:
                """Check if there is enough items available"""
                if order.user.funds >= order.count_total_price:
                    """Check is user has enough funds"""
                    order.user.funds -= order.count_total_price
                    order.item.amount_available -= order.amount
                    order.user.save()
                    order.item.save()
                    order.save()
                    return super().form_valid(form=form)
                messages.error(self.request, 'Top Up your Funds')
                return HttpResponseRedirect('/catalog/')
            messages.error(self.request, 'Sorry, try to specify less amount')
            return HttpResponseRedirect('/catalog/')
        return HttpResponseRedirect('/login')

    def get_success_url(self):
        url = '/orderlist/'
        return url


class ItemList(ListView):
    """Products list"""
    template_name = 'item_list.html'
    model = Item
    queryset = Item.objects.all()
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({'form': OrderCreateForm})
        return context


class UserLogoutView(LogoutView, LoginRequiredMixin):
    """"Logout"""
    next_page = '/catalog/'
    redirect_field_name = 'next'
    login_url = '/login/'


class RefundCreateView(CreateView, MyLoginRequiredMixin):
    """Refund submitting"""
    model = Refund
    success_url = '/orderlist/'
    http_method_names = ['get', 'post']
    fields = []
    queryset = Refund.objects.all()
    login_url = '/login/'

    def form_valid(self, form):
        refund = form.save(commit=False)
        order_id = self.request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        refund.order = order
        order_time = refund.order.create_date
        refund_request_time = timezone.now()
        if refund_request_time < order_time + timedelta(minutes=3):
            """"Check if item is suitable for refund"""
            refund.save()
            messages.info(self.request, 'Refund request submitted')
            return super().form_valid(form=form)
        messages.error(self.request, 'Grace period ended')
        return HttpResponseRedirect(self.success_url)


class OrderListView(ListView, LoginRequiredMixin):
    """Submitted orders list"""
    template_name = 'order_list.html'
    model = Order
    queryset = Order.objects.all()
    paginate_by = 10
    login_url = '/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({'form': RefundCreateForm})
        return context

    def get_queryset(self):
        """Filter orders by user"""
        return Order.objects.filter(user=self.request.user)


class RefundListView(MyLoginRequiredMixin, ListView):
    """Refunds list"""
    model = Refund
    paginate_by = 10
    template_name = 'refund_list.html'
    queryset = Refund.objects.all()
    login_url = '/login/'


class ItemUpdateView(UpdateView, MyLoginRequiredMixin):
    """Edit existing item"""
    model = Item
    template_name = 'edit_item.html'
    success_url = '/catalog/'
    fields = ['name', 'description', 'price', 'amount_available']
    login_url = '/login/'


class AddItemView(CreateView, MyLoginRequiredMixin):
    """Create new item"""
    model = Item
    template_name = 'edit_item.html'
    success_url = '/catalog/'
    fields = ['name', 'description', 'price', 'amount_available']


class ManageRefundView(DeleteView, MyLoginRequiredMixin):
    """Approval or reject of refund requests"""
    model = Refund
    success_url = '/refunds/'
    login_url = '/login/'

    def delete(self, request, *args, **kwargs):
        refund = self.get_object()
        order = refund.order
        item = order.item
        user = order.user
        if request.POST.get('action') == 'approve':
            user.funds += order.count_total_price
            item.amount_available += order.amount
            user.save()
            item.save()
            order.delete()
        refund.delete()
        return HttpResponseRedirect(self.success_url)
