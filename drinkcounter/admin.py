from django.contrib import admin

from drinkcounter.models import Beverage, Consumption, Payment, Resident


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'room_number', 'moved_out', 'credit')
    pass


@admin.register(Beverage)
class BeverageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    pass


@admin.register(Consumption)
class ConsumptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'resident', 'beverage', 'timestamp')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'resident', 'amount', 'timestamp')
