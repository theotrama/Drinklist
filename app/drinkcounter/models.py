from django.db import models


class Resident(models.Model):
    """
    Store resident's information
    """
    class Meta:
        verbose_name = 'Resident'
        verbose_name_plural = 'Residents'

    room_number = models.IntegerField()
    name = models.CharField(max_length=50)
    moved_out = models.BooleanField(default=False)
    credit = models.DecimalField(default=0, decimal_places=2, max_digits=1000)

    def __str__(self):
        return self.name

    def is_internal(self):
        """
        Check if a resident is internal (part of the kitchen) or external (not part of the kitchen)
        :return Boolean: True if internal; False if external
        """
        return 235 <= self.room_number <= 248

    def calculate_consumption_per_resident(self):
        """
        Calculate how much each beverages each resident consumes
        """
        return Consumption.objects.filter(resident=self).count()

    def get_current_credit(self):

        """
        Return the current credit of the resident
        :return Float: Credit
        """
        credit = 0
        beverages = Beverage.objects.all()
        for beverage in beverages:
            beverage.price
            drinks_consumed = Consumption.objects.filter(resident=self, beverage=beverage.id).count()
            credit -= beverage.price * drinks_consumed
        return round(credit, 2)

    consumption_count = property(calculate_consumption_per_resident)

    def update_credit(self, amount, beverage=None, consumption=True):
        """
        Update resident's credit
        :param amount: Amount by which the credit should be decreased/increased
        :param beverage: Beverage object
        :param consumption: If true then decrease (consumption), if false then increase (payment)
        """
        if consumption:
            self.credit -= amount * beverage.price
        else:
            self.credit += amount
        self.save()


class Beverage(models.Model):
    """
    Store beverage names and prices
    """
    class Meta:
        verbose_name = 'Beverage'
        verbose_name_plural = 'Beverages'

    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name

    def calculateConsumptionPerBeverage(self):
        """
        Calculate how much each beverage is consumed
        """
        return Consumption.objects.filter(beverage=self).count()

    consumption_count = property(calculateConsumptionPerBeverage)


class Consumption(models.Model):
    """
    Store consumptions and link them to the beverage and the resident
    """
    class Meta:
        verbose_name = 'Consumption'
        verbose_name_plural = 'Consumptions'

    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    beverage = models.ForeignKey(Beverage, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Return beverage's name
        return self.beverage.name


class Payment(models.Model):
    """
    Store payments
    """
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    amount = models.FloatField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
