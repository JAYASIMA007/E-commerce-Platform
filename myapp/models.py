from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATE_CHOICES = (
   ("AN","Andaman and Nicobar Islands"),
   ("AP","Andhra Pradesh"),
   ("AR","Arunachal Pradesh"),
   ("AS","Assam"),
   ("BR","Bihar"),
   ("CG","Chhattisgarh"),
   ("CH","Chandigarh"),
   ("DN","Dadra and Nagar Haveli"),
   ("DD","Daman and Diu"),
   ("DL","Delhi"),
   ("GA","Goa"),
   ("GJ","Gujarat"),
   ("HR","Haryana"),
   ("HP","Himachal Pradesh"),
   ("JK","Jammu and Kashmir"),
   ("JH","Jharkhand"),
   ("KA","Karnataka"),
   ("KL","Kerala"),
   ("LA","Ladakh"),
   ("LD","Lakshadweep"),
   ("MP","Madhya Pradesh"),
   ("MH","Maharashtra"),
   ("MN","Manipur"),
   ("ML","Meghalaya"),
   ("MZ","Mizoram"),
   ("NL","Nagaland"),
   ("OD","Odisha"),
   ("PB","Punjab"),
   ("PY","Pondicherry"),
   ("RJ","Rajasthan"),
   ("SK","Sikkim"),
   ("TN","Tamil Nadu"),
   ("TS","Telangana"),
   ("TR","Tripura"),
   ("UP","Uttar Pradesh"),
   ("UK","Uttarakhand"),
   ("WB","West Bengal")
)

class Customer(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=70)
  locality = models.CharField(max_length=100)
  city = models.CharField(max_length=100)
  zipcode = models.PositiveIntegerField()
  state = models.CharField(choices=STATE_CHOICES, max_length=50)
  
  def __str__(self):
    return str(self.id)
    
CATEGORY_CHOICE = (
  ('MTW', 'Men Top Wear'),
  ('FTW', 'Female Top Wear'),
  ('MBW', 'Men Bottom Wear'),
  ('FBW', 'Female Bottom Wear'),
  ('M', 'Mobile'),
  ('L', 'Laptop'),
  )
  
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices = CATEGORY_CHOICE, max_length=100)
    product_image = models.ImageField(upload_to='productimg')
    
    def __str__(self):
      return str(self.id)
      
class Cart(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)
  
  def __str__(self):
    return str(self.id)
    
  @property
  def total_cost(self):
    return self.quantity * self.product.discounted_price
    
STATUS_CHOICE = (
  ('Accepted', 'Accepted'),
  ('Packed', 'Packed'),
  ('Shipped', 'Shipped'),
  ('Delivered', 'Delivered'),
  ('Cancel', 'Cancel'),
  )
  
class PlacedOrder(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)
  ordered_date = models.DateTimeField(auto_now_add=True)
  status = models.CharField(choices=STATUS_CHOICE, default='Pending', max_length=20)
  
  @property
  def total_cost(self):
    return self.quantity * self.discounted_price