from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, OrderItem, Order, BillingAddress, Payment, Banner
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm
import stripe


stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'



class HomeView(ListView):
	model = Item
	template_name = 'home.html'	
	paginate_by = 3


class ProductDetail(DetailView):
	model = Item
	template_name = 'product.html'


@login_required
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
			messages.warning(request, 'One item has been added from your cart')
			return redirect('core:order-summery')
		else:
			order.items.add(order_item)
			messages.warning(request, 'One item has been added from your cart')
	else:
		order = Order.objects.create(user=request.user)
		order.items.add(order_item)
		messages.warning(request, 'One item has been added from your cart')
	return redirect('core:order-summery')


@login_required
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
			messages.warning(request, 'One item has been removed from your cart')
			return redirect('core:order-summery')
		else:
			messages.warning(request, 'This item does not exist in your cart')			
	else:
		messages.warning(request, "You don't have an acive order")			
	return checkoutt('core:product-detail', slug=slug)


@login_required
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
				messages.warning(request, 'One item has been removed from your cart')
				return redirect('core:order-summery')
			else:
				order.items.remove(order_item)
				messages.warning(request, 'One item has been removed from your cart')
				return redirect('core:order-summery')
				
		else:
			messages.warning(request, 'This item does not exist in your cart')			
			pass
	else:
		messages.warning(request, "You don't have an acive order")			
		pass
	return redirect('core:product-detail', slug=slug)


class OrderSummery(LoginRequiredMixin, View):
	def get(self, *args, **kwargs):
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			context = {
				'object': order
			}
			return render(self.request, 'order_summery.html', context)
		except ObjectDoesNotExist:
			messages.warning(self.request, "You dont have an active order")
			return redirect('/')


class CheckoutView(View):
	def get(self, *args, **kwargs):
		form = CheckoutForm()
		context = {
		'form':form
		}
		return render(self.request, 'checkout.html', context)
	
	def post(self, *args, **kwargs):
		form = CheckoutForm(self.request.POST or None)
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			if form.is_valid():
				address = form.cleaned_data.get("address")
				appartment_address = form.cleaned_data.get("appartment_address")
				country = form.cleaned_data.get("country")
				zip = form.cleaned_data.get("zip")
				# same_shipping_address = form.cleaned_data.get("same_shipping_address")
				# save_info = form.cleaned_data.get("save_info")
				payment_options = form.cleaned_data.get("payment_options")
				billing_address= BillingAddress(
				user=self.request.user,
				address=address,
				appartment_address=appartment_address,
				country=country,
				zip=zip	
				)
				billing_address.save()
				order.billing_address=billing_address
				order.save(	)

				return redirect('core:payment', payment_options=payment_options.lower())
			
			messages.warning(self.request, 'the form is invalid')		
			return redirect('core:checkout')
		
		except ObjectDoesNotExist:
			messages.warning(self.request, "You dont have an active order")
			return redirect('/')


class PaymentView(View):
	def get(self, *args, **kwargs):
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
		except ObjectDoesNotExist:
			messages.warning(self.request, "You dont have an active order")
			return redirect('/')

		context = {
			'object': order
		}
		return render(self.request, 'payment.html', context)

	def post(self, *args, **kwargs):
		order = Order.objects.get(user=self.request.user, ordered=False)
		amount = int(100 * order.total_price()) #cents
		token = self.request.POST.get('stripeToken')
		try:
			charge = stripe.Charge.create(
			  amount=amount,
			  currency="usd",
	  		  source=token
			)

			# create the payment
			payment = Payment()
			payment.stripe_charge_id = charge['id']
			payment.amount = order.total_price()
			payment.user = self.request.user
			payment.save()
	
			# assign the payment to the order
			order.ordered = True
			order.payment = payment
			order.save()

			messages.success(self.request, "The payment was successful")
			return redirect("/")
		
		except stripe.error.CardError as e:
			messages.warning(self.request, 'CardErorr')
			return redirect('/')

		except stripe.error.RateLimitError as e:
			messages.warning(self.request, 'RateLimitError')
			return redirect('/')

		except stripe.error.InvalidRequestError as e:
			messages.warning(self.request, 'InvalidRequestError')
			return redirect('/')

		except stripe.error.AuthenticationError as e:
			messages.warning(self.request, 'AuthenticationError')
			return redirect('/')

		except stripe.error.APIConnectionError as e:
			messages.warning(self.request, 'Netword Error')
			return redirect('/')

		except stripe.error.StripeError as e:
			messages.warning(self.request, 'Stripe Error')
			return redirect('/')

		except Exception as e:
			messages.warning(self.request, 'a very serious error has occured, we have been notified')
			return redirect('/')
