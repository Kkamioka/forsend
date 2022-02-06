from ..models import Cart
from django.utils.deprecation import MiddlewareMixin

class MiddlewareMyself(MiddlewareMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('--init--')

    def process_request(self, request):
        print('--process_request--')
        nowcart = request.session.get('cart', False)
        print(nowcart)
        if  nowcart == False:
            cart = Cart()
            cart.save()
            request.session['cart'] = cart.id

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        print('--process_view--')

    def process_response(self, request, response):
        print('--process_response')
        return response
