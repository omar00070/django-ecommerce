from django.db import models
from django.conf import settings
from django.shortcuts import reverse


CATEGORY_CHOICE = (
	('S', 'Shirt'),
	('SW','Sports Wear'),
	('OW','Outwear')
)

LABEL_CHOICE = (
	('P', 'primary'),
	('S', 'secondary'),
	('D', 'danger')

)


class Item(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	price =  models.DecimalField(max_digits=10, decimal_places=2)
	discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	category = models.CharField(choices=CATEGORY_CHOICE, max_length=2)
	label = models.CharField(choices=LABEL_CHOICE, max_length=2)
	slug = models.SlugField(max_length=100)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('core:product-detail', kwargs={
			'slug': self.slug
		})

	def get_add_to_cart_url(self):
		return reverse('core:add-to-cart', kwargs={
			'slug': self.slug
			})
	def get_remove_from_cart_url(self):
		return reverse('core:remove-from-cart', kwargs={
			'slug':self.slug
			})



class OrderItem(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
	on_delete=models.CASCADE) 
	ordered = models.BooleanField(default=False)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return F'{self.quantity} of {self.item.title}'

	def total_price(self):
		if self.item.discount_price:
			return self.item.discount_price * self.quantity
		return self.item.price * self.quantity

	def saving_price(self):
		saving = self.item.price * self.quantity - self.item.discount_price * self.quantity
		return saving

class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, 
							on_delete=models.CASCADE)
	items = models.ManyToManyField(OrderItem)
	ordered = models.BooleanField(default=False)

	def total_price(self):
		total = 0
		for item in self.items.all():
			total += item.total_price()
		return total


	def __str__(self):
		return self.user.username


class BillingAddress(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, 
							on_delete=models.CASCADE)
	