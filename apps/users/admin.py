from django.contrib import admin
from .models import DefaultUser, Seller, ContentMaker


admin.site.register(DefaultUser)
admin.site.register(Seller)
admin.site.register(ContentMaker)
