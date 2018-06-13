from django.contrib import admin
from .models import Manufacturer, Car, Article, Author, Person, Group, Membership
# Register your models here.


admin.site.register([Manufacturer, Car, Article, Author, Person, Group, Membership])

