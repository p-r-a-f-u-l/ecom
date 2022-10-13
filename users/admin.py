from django.contrib import admin

from .models import Address, CardDetails, CartDetails, FavDetails

# @admin.register(ProfileInfo)
# class ProfileConfig(admin.ModelAdmin):
#     list_display = ['username', 'uid', "created_on", "updated_on"]

admin.site.register(CartDetails)

admin.site.register(FavDetails)

@admin.register(Address)
class AddressConfig(admin.ModelAdmin):
    list_display = [
        "name",
        "address",
        "pincode",
        "country",
        "city",
    ]
    list_filter = [
        "name",
        "address",
        "pincode",
        "country",
        "city",
        "phone_number",
    ]


@admin.register(CardDetails)
class CardInfo(admin.ModelAdmin):
    list_display = [
        'card_number',
        'holder_name',
        'expire_date',
    ]
    list_filter = [
        'card_number',
        'holder_name',
        'expire_date',
    ]

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
