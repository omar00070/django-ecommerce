from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField
from PIL import Image

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
	thumbnail = models.ImageField(upload_to='products-images', blank=True, null=True)
	img_1 = models.ImageField(upload_to='products-images', blank=True, null=True)
	img_2 = models.ImageField(upload_to='products-images', blank=True, null=True)
	img_3 = models.ImageField(upload_to='products-images', blank=True, null=True)
	additional_info = models.TextField(blank=True, null=True)
	slug = models.SlugField(max_length=100)
	banner = models.ImageField(upload_to="banner_images", blank=True, null=True)
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

	def save(self, *args, **kwargs):
	 # override the save method to reduce the size of the image  
		super().save(*args, **kwargs)
		img_thumbnail = Image.open(self.thumbnail.path)
		output_size = (309, 550)
		img_thumbnail.thumbnail(output_size)
		img_thumbnail.save(self.thumbnail.path)



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
	billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, null=True, blank=True)
	payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True)
	

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
	address	= models.CharField(max_length=100)
	appartment_address = models.CharField(max_length=100)
	country	= CountryField(multiple=False)
	zip = models.CharField(max_length=100)
	
	def __str__(self):
		return self.user.username

class Payment(models.Model):
	stripe_charge_id = models.CharField(max_length=50)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
	time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user.username} Payment'

class Banner(models.Model):
	image = models.ImageField(upload_to='banner_images', blank=True, null=True)
