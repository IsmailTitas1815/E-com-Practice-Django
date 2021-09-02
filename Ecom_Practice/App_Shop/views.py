from django.shortcuts import render
from django.views.generic import ListView, DetailView

from App_Shop.models import Product
# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin


class Home(ListView):
    template_name = 'App_Shop/home.html'
    model = Product
    context_object_name = "products"


class ProductDetails(LoginRequiredMixin, DetailView):
    template_name = "App_Shop/product_details.html"
    model = Product
    context_object_name = "product"
