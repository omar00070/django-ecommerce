from django import template
from core.models import Order

register = template.Library()


@register.filter
def cart_counter(user):
	if user.is_authenticated:
		qs = Order.objects.filter(user=user, ordered=False)
		if qs.exists():
			cart_count = qs[0].items.count()
			return cart_count
	return 0