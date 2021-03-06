
from .models import Order
"""Utils to handle sessions"""


def get_order_session(request):
    """We try to get the order by the id"""
    order_id = request.session.get('order_id', None)
    if order_id is None:
        order = Order()
        order.save()
        request.session['order_id'] = order.id

    else:
        try:
            order = Order.objects.get(id=order_id, ordered=False)
        except Order.DoesNotExist:
            order = Order()
            order.save()
            request.session['order_id'] = order.id

    if request.user.is_authenticated and order.user is None:
        order.user = request.user
        order.save()
    return order
