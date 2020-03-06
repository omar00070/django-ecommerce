from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView, View


def pruducts(request):
	context = {
		"items": Item.objects.all()
	}
	return render(request, 'core/home-page.html', context)


class HomeView(ListView):
	model = Item
	template_name = 'core/home.html'	



class ProductDetail(DetailView):
	model = Item
	template_name = 'core/product.html'



def add_to_cart(request, slug):
	item = get_object_or_404(Item, slug=slug)
	order_item, created = OrderItem.objects.get_or_create(
		item=item,
		user=request.user,
		ordered=False
		)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# we have to check if the item exists in the order
		if order.items.filter(item__slug=item.slug).exists():
			order_item.quantity += 1
			order_item.save()
		else:
			order.items.add(order_item)
	else:
		order = Order.objects.create(user=request.user)
		order.items.add(order_item)

	return redirect('core:product-detail', slug=slug)


def remove_from_cart(request, slug):
	item = get_object_or_404(Item, slug=slug)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# we have to check if the item exists in the order
		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(
										item=item,
										user=request.user,
										ordered=False
										)[0]
		
			order.items.remove(order_item)
				
		else:
			return redirect('core:product-detail', slug=slug)
			pass
	else:
		return redirect('core:product-detail', slug=slug)
		pass
	return redirect('core:product-detail', slug=slug)


def remove_single_item_from_cart(request, slug):
	item = get_object_or_404(Item, slug=slug)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# we have to check if the item exists in the order
		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(
										item=item,
										user=request.user,
										ordered=False
										)[0]
			if order_item.quantity > 1:	
				order_item.quantity -= 1
				order_item.save()
			else:
				order.items.remove(order_item)
				
		else:
			#message that the item is not in the order
			pass
	else:
		# message that the user has no active order
		pass
	return redirect('core:product-detail', slug=slug)


class OrderSummery(View):
	def get(self, *args, **kwargs):
		order = Order.objects.get(user=self.request.user, ordered=False)
		context = {
			'object': order
		}
		return render(self.request, 'core/order_summery.html', context)

