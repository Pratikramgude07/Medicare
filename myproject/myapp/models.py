from django.db import models



# Create your models here.

class product(models.Model):
    SUBCAT=((1,"Personal care"),(2,"Health food and drinks"),(3,"Beauty"),(4,"Skin care"),(5,"Home care"),(6,"Must have"),(7,"Health condition"),(8,"Sexsual wellness"))
    CAT=((1,"New launch"),(2,"Tranding Near you"),(3,"Frequentally use"))
    pname=models.CharField(max_length=50,verbose_name="product name")
    old_price=models.FloatField()
    price=models.FloatField()
    category=models.IntegerField(choices=CAT,verbose_name="categeory")
    sub_category=models.IntegerField(choices=SUBCAT,verbose_name="sub_categeory")
    description=models.CharField(max_length=300,verbose_name="details")
    is_active=models.BooleanField(default=True,verbose_name="is_available")
    pimage=models.ImageField(upload_to='image')

    def __str__(self):
        return self.pname

class Cart(models.Model):
    userid=models.ForeignKey('auth.user',on_delete=models.CASCADE,db_column='userid')
    pid=models.ForeignKey('product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.CharField(max_length=50)
    user_id=models.ForeignKey("auth.user",on_delete=models.CASCADE,db_column="user_id")
    p_id=models.ForeignKey("product",on_delete=models.CASCADE,db_column="p_id")
    qty=models.IntegerField(default=1)
    amt=models.FloatField()
