from .models import Order


def ordersCount(request):
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(user__id=request.user.id, isPaid=False)
            return {
                'orderCount': order.orderItems.count(),
            }
        except Order.DoesNotExist:
            return {
                'orderCount': 0,
            }
    else:
        return {
            'orderCount': 0,
        }
