from django import forms

from drinkcounter.models import Beverage, Payment, Resident


# Todo - write functions that returns all resident
# It should order the residents and return first our kitchen's residents
# Then it should return all other residents sorted by room_number


def create_resident_choice_values():
    """
    Prepare two tuples:
    1) resident_choice_pks:     Tuple with PrimaryKeys of each model
    2) resident_choice_values:  Tuple with "resident + room_number" that serves as output of the ModelChoiceField:

    There are three "types" of residents:
    1) resident_internal that:  Internal residents who still live in the dorm
    2) resident_internal_mvd:   Internal residents that moved out
    3) resident_external:       External residents
    :return resident_form: List of two tuples
    """
    # Get separate external and internal residents
    resident_internal = Resident.objects.filter(room_number__range=(235, 248), moved_out=False)
    resident_internal = resident_internal.order_by('room_number').values('id', 'name', 'room_number')

    resident_internal_mvd = Resident.objects.filter(room_number__range=(235, 248), moved_out=True)
    resident_internal_mvd = resident_internal_mvd.order_by('room_number').values('id', 'name', 'room_number')

    resident_external = Resident.objects.exclude(room_number__range=(235, 248))
    resident_external = resident_external.order_by('room_number').values('id', 'name', 'room_number')

    # Create empty list
    resident_choice_pks = list()
    resident_choice_values = list()

    for resident in resident_internal:
        element = resident['name'] + ' ' + str(resident['room_number'])
        resident_choice_pks.append(resident['id'])
        resident_choice_values.append(element)

    for resident in resident_internal_mvd:
        element = resident['name'] + ' (ex) ' + str(resident['room_number'])
        resident_choice_pks.append(resident['id'])
        resident_choice_values.append(element)

    for resident in resident_external:
        element = resident['name'] + ' ' + str(resident['room_number'])
        resident_choice_pks.append(resident['id'])
        resident_choice_values.append(element)

    # Zip the two lists together
    # https://stackoverflow.com/questions/2407398/how-to-merge-lists-into-a-list-of-tuples
    resident_form = list(zip(resident_choice_pks, resident_choice_values))

    return resident_form


class AddConsumptionForm(forms.Form):
    """
    Form to add a consumption to the database
    :param amount: Integer field
    :param resident: Choice field that shows resident names in the correct order
    :param beverage: Object but shows beverage name as string
    """
    amount = forms.IntegerField(label='Menge', initial=1, min_value=1, max_value=20, widget=forms.TextInput(attrs={'placeholder': 'Menge'}))
    resident = forms.ChoiceField(label='Bewohner', choices=[])
    beverage = forms.ModelChoiceField(label='Getränk', queryset=Beverage.objects.all(), empty_label=None)

    # Reload resident dropdown list every time the form is rendered
    # https://www.codementor.io/tips/7714213398/django-form-choices-loaded-from-database-are-not-updated
    def __init__(self, *args, **kwargs):
        super(AddConsumptionForm, self).__init__(*args, **kwargs)
        self.fields['resident'] = forms.ChoiceField(choices=create_resident_choice_values())


class AddResidentForm(forms.Form):
    """
    Form to add a resident to the database
    :param resident: Integer field but shows resident name as strings
    :param beverage: Object but shows beverage name as string
    """
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'placeholder': 'Isi'}))
    room = forms.IntegerField(label='Zimmernummer', widget=forms.TextInput(attrs={'placeholder': '244'}))


class MakePaymentForm(forms.Form):
    """
    Form to add a payment to the database
    :param amount: Integer field
    :param resident: Choice field that shows resident names in the correct order
    :param beverage: Object but shows beverage name as string
    """
    resident = forms.ChoiceField(label='Bewohner', choices=[])
    amount = forms.FloatField(label='Einzahlbetrag', widget=forms.NumberInput(attrs={'placeholder': '20 €'}))

    # Reload resident dropdown list every time the form is rendered
    # https://www.codementor.io/tips/7714213398/django-form-choices-loaded-from-database-are-not-updated
    def __init__(self, *args, **kwargs):
        super(MakePaymentForm, self).__init__(*args, **kwargs)
        self.fields['resident'] = forms.ChoiceField(choices=create_resident_choice_values())
