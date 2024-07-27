from django.contrib import admin

# Register your models here.
from .models import product

class Productadmin(admin.ModelAdmin):
    list_display=['id','pname','old_price','price','category','sub_category','description','is_active','pimage']


admin.site.register(product,Productadmin)