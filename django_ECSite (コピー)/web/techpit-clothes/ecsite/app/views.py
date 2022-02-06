import stripe
import json

from django.conf import settings
from django.shortcuts import render, redirect
from django.views import generic
from .models import Product, line_items, Cart
from .forms import CreateForm
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse


# Create your views here.
class IndexView(generic.ListView):

    model = Product
    template_name = 'product/index.html'

class ShowView(generic.DetailView):

    model = Product
    template_name = 'product/show.html'

class CreateView(generic.CreateView):

    model = line_items
    form_class =  CreateForm
    template_name = 'product/create.html'

    def form_valid(self, form):
        #print("######")
        #print(self.request.POST)
        cart_id = self.request.session.get('cart', False)
        line_item = line_items.objects.filter(cart_id=cart_id, product_id=self.request.POST.get(id)).first()
        print("%%%%%%")
        print(line_item)
        if line_item != None:
            #print("---1----")
            line_item.quantity = self.request.POST['quantity']
            line_item.save()
        else:
            #print("---2----")
            product_id = self.request.POST.get('id')
            #print(product_id)
            cart = Cart.objects.get(pk=cart_id)
            product = Product.objects.get(pk=product_id)
            line_item = line_items()
            #print(line_item)
            line_item.cart_id = cart
            line_item.product_id = product
            line_item.quantity = self.request.POST['quantity']
            line_item.save()
            
        #print(line_item)

        return redirect('cart')

class CartView(generic.ListView):

    model = Product
    template_name = 'product/cart.html'

    def __init__(self): # 初期化： インスタンス作成時に自動的に呼ばれる
        self.line_items = []
        self.total_price = 0

    def get_context_data(self):
        ctx = super().get_context_data()

        ctx['line_items'] = self.line_items
        ctx['total_price'] = self.total_price
        ctx['publicKey'] = settings.STRIPE_PUBLIC_KEY

        return ctx

    def get_queryset(self):
        #print("@@@@")
        cart_id = self.request.session.get('cart', False)
        #print(cart_id)
        self.line_items =  line_items.objects.filter(cart_id=cart_id)
        #print(lineitems)
        for lineitem in self.line_items:
            #print(lineitem.product_id_id)
            product =  Product.objects.get(pk=lineitem.product_id_id)
            #print(product.price)
            #print(product.price * lineitem.quantity)
            self.total_price = self.total_price + product.price * lineitem.quantity
            print("/////")
            print(lineitem.product_id_id)
        #print("=total_price=")
        #print(total_price)

class DeleteView(generic.DeleteView):

    model = line_items
    template_name = 'product/cart.html'
    success_url = reverse_lazy('cart')


def create_checkout_session(request):
    print("$$$$$$")
    cart_id = request.session.get('cart', False)
    #stripe.api_key = settings.STRIPE_PUBLIC_KEY
    #stripe.api_key = 'sk_test_51KHkHTHcCd0AoNuOQgGsQV3eOFoNu8IOnn2p3eU3FNRdFjskINtd7oWtFlF9kamOp0JIwwpXGF71zo5aYRhTYAKK00sZhrX4sa'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    items = line_items.objects.filter(cart_id=cart_id)
    print(items)

    if len(items) <= 0:
        return redirect('cart')
        
    put_items = []
    for item in items:
        put_item = {
            'price_data': {
                'currency': 'jpy',
                'unit_amount': item.product_id.price,
                'product_data': {
                    'name': item.product_id.name,
                    'images': ['https://imgur.com/t/clean_your_desk/BrzDe46'],
                },
            },
            'quantity': item.quantity,
            #'name': item.product_id.name,
            #'description': item.product_id.description,
            #'amount': item.product_id.price,
            #'quantity': item.quantity,
            #'currency': 'jpy',
        }
        put_items.append(put_item)

    print(put_items)


    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items = put_items,
        #line_items=[
        #    {
        #        'price_data': {
        #            'currency': 'jpy',
        #            'unit_amount': 2000,
        #            'product_data': {
        #                'name': 'Stubborn Attachments',
        #                'images': ['https://i.imgur.com/EHyR2nP.png'],
        #            },
        #        },
        #        'quantity': 1,
        #    },
        #],     
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')),
        cancel_url=request.build_absolute_uri(reverse('cart')),
    )
    return JsonResponse({'id': checkout_session.id}) 

    ##return render(request, 'product/checkout.html', {
    #    'session': checkout_session, 
    #    'publicKey': settings.STRIPE_PUBLIC_KEY, 
    #    'secretKey': settings.STRIPE_SECRET_KEY
    #})


def success(request):
    cart_id = request.session.get('cart', False)
    items = line_items.objects.filter(cart_id=cart_id)
    for item in items:
        item.delete()

    return render(request, 'product/success.html', {})
