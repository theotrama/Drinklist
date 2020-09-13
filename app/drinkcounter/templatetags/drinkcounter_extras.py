from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from drinkcounter.models import Beverage, Resident

register = template.Library()


@register.filter
def filter_by_resident_and_beverage(consumption, resident_and_beverage):
    """
    Filter the consumptions by resident name to serve it to a template
    :param consumption: QuerySet // of all consumptions
    :param resident_and_beverage: Name of resident and beverage for which should be filtered
    """
    if resident_and_beverage is None:
        return False
    arg_list = [resident_and_beverage.strip() for arg in resident_and_beverage.split(',')]

    try:
        resident = Resident.objects.get(name=name)
        beverage = Beverage.objects.get(name=beverage)
    except ObjectDoesNotExist:
        Http404("This consumption does not exist")

    return consumption.filter(resident=resident).filter(beverage=beverage)
