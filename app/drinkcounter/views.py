from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from drinkcounter.models import Beverage, Consumption, Payment, Resident
from .forms import AddConsumptionForm, AddResidentForm, MakePaymentForm


class OverviewView(TemplateView):
    template_name = 'drinkcounter/overview.html'

    def get(self, request):
        """
        Query all residents from the database and split them into resident_internal and resident_external as dicts
        """
        try:
            # Get internal residents of kitchen
            resident_internal = Resident.objects.filter(room_number__range=(235, 248), moved_out=False)
            resident_internal = resident_internal.order_by('room_number')

            # Get internal residents of kitchen that moved out
            resident_internal_mvd = Resident.objects.filter(room_number__range=(235, 248), moved_out=True)
            resident_internal_mvd = resident_internal_mvd.order_by('room_number')

            # Get external residents (residents of other kitchens)
            resident_external = Resident.objects.exclude(room_number__range=(235, 248))
            resident_external = resident_external.order_by('room_number')

            # Get other objects
            beverage = Beverage.objects.all()
            consumption = Consumption.objects.all()

        except ObjectDoesNotExist:
            raise Http404("This resident does not exist")

        context = {
            'resident_internal': resident_internal,
            'resident_internal_mvd': resident_internal_mvd,
            'resident_external': resident_external,
            'consumption': consumption,
            'beverage': beverage,
        }

        return render(request, self.template_name, context=context)


class DetailedView(TemplateView):
    template_name = 'drinkcounter/details.html'

    def get(self, request, resident_id):
        resident = get_object_or_404(Resident, pk=resident_id)
        beverages = Beverage.objects.all()
        consumption = Consumption.objects.filter(resident=resident)

        # Store filtered consumption in dict to make it accessible in the view
        # key: beverage name
        # value: beverage count
        filtered_consumption = dict()
        for beverage in beverages:
            consumption_count = consumption.filter(beverage=beverage.id).count()
            filtered_consumption[beverage.name] = consumption_count

        context = {
            'resident': resident,
            'filtered_consumption': filtered_consumption,
            'credit': resident.credit,
        }

        return render(request, self.template_name, context=context)


class AddBeverageView(TemplateView):
    template_name = 'drinkcounter/add-beverage.html'
    form_class = AddConsumptionForm

    def get(self, request):
        """
        Render the form.
        To make the service most convenient we need to order the residents in the resident dropdown list.
        We need to display the Residents in the following order:
        1) Internal residents
        2) Internal residents that have moved out
        2) External residents
        """
        form = self.form_class()

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Save how many beverages where consumed
        """
        # create a form instance and populate it with data from the request:
        form = self.form_class(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # Be careful with different variable types due to the specified form
            form_data = form.cleaned_data
            amount = form_data['amount']
            resident_id = form_data['resident']
            beverage = form_data['beverage']

            request.session['amount'] = amount
            request.session['resident_id'] = resident_id
            request.session['beverage_id'] = beverage.id

            # Get resident and beverage objects with appropriate PK
            resident = Resident.objects.get(id=resident_id)
            beverage = Beverage.objects.get(id=beverage.id)

            resident.update_credit(amount, beverage, True)

            saved_ids = list()
            # Create consumption object
            for i in range(amount):
                c = Consumption(resident=resident, beverage=beverage)
                c.save()
                saved_ids.append(c.id)

            # Serialize all the Consumption objects and pass them to the session
            consumption_data = serializers.serialize('json', Consumption.objects.filter(id__range=[saved_ids[0], saved_ids[-1]]))
            request.session['consumption_data'] = consumption_data

            # Todo - Save to database
            # redirect to a new URL:
            return redirect('drinkcounter:SuccessView')

        return render(request, self.template_name, {'form': form})


class SuccessView(TemplateView):
    template_name = 'drinkcounter/success.html'

    def get(self, request):
        """
        Render success page. This page includes
            * Who added the beverage
            * The type of beverage
            * The amount of beverages added
        """

        try:
            amount = request.session.get('amount', None)
            resident_id = request.session.get('resident_id', None)
            beverage_id = request.session.get('beverage_id', None)
        except KeyError:
            pass

        # Get resident and beverage objects with appropriate PK
        resident = Resident.objects.get(id=int(resident_id))
        beverage = Beverage.objects.get(id=(beverage_id))

        context = {'amount': amount, 'resident': resident, 'beverage': beverage}

        return render(request, self.template_name, context=context)

    def post(self, request):
        """
        Delete previously added entries.
        Render undo page.
        """
        try:
            consumption_data = request.session.get('consumption_data', None)
        except KeyError:
            pass
        # Deserialize Consumption objects
        for obj in serializers.deserialize('json', consumption_data):
            # https://stackoverflow.com/questions/43120293/get-primary-key-of-a-deserialized-object-in-django
            Consumption.objects.filter(id=obj.object.id).delete()

        return redirect('drinkcounter:UndoView')


class UndoView(TemplateView):
    template_name = 'drinkcounter/undo.html'

    def get(self, request):
        """
        Show a message that previous entry was deleted.
        """
        return render(request, self.template_name)


class AddResidentView(TemplateView):
    template_name = 'drinkcounter/add-resident.html'
    form_class = AddResidentForm

    def get(self, request):
        """
        Render the form to add a resident to the database
        """
        form = self.form_class()

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Save how many beverages where consumed
        """
        form = self.form_class()
        # create a form instance and populate it with data from the request:
        form = self.form_class(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # Be careful with different variable types due to the specified form
            form_data = form.cleaned_data
            name = form_data['name']
            room = form_data['room']

            # Get Resident or create him/her
            obj, created = Resident.objects.get_or_create(
                name=name,
                room_number=int(room),
            )

            request.session['name'] = name
            request.session['room'] = room
            request.session['created'] = created

            return redirect('drinkcounter:ResidentCreationInfoView')

        return render(request, self.template_name, {'form': form})


class ResidentCreationInfoView(TemplateView):
    template_name = 'drinkcounter/resident-creation-info.html'

    def get(self, request):
        """
        Show status of Resident creation.
            --> Warning if Resident already exists
            --> Success if Resident was added successfully
        """

        name = request.session.get('name', None)
        room = request.session.get('room', None)
        created = request.session.get('created', None)

        context = {
            'name': name,
            'room': room,
            'created': created,
        }

        return render(request, self.template_name, context=context)


class MakePaymentView(TemplateView):
    """
    View to pay into the beverage cash register
    """
    template_name = 'drinkcounter/payment.html'
    form_class = MakePaymentForm

    def get(self, request):
        """
        Show form for making payments
        """
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Add the payment to the database
        """
        form = self.form_class()
        # create a form instance and populate it with data from the request:
        form = self.form_class(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # Be careful with different variable types due to the specified form
            form_data = form.cleaned_data
            amount = form_data['amount']
            resident_id = form_data['resident']

            try:
                resident = Resident.objects.get(id=resident_id)
            except ObjectDoesNotExist:
                raise Http404("This resident does not exist")

            # Add payment to the database and update credit
            payment = Payment(resident=resident, amount=amount)
            payment.save()
            resident.update_credit(int(amount), consumption=False)

            request.session['amount'] = amount
            request.session['resident_id'] = resident_id
            request.session['payment_id'] = payment.id

        return redirect('drinkcounter:MakePaymentSuccessView')


class MakePaymentSuccessView(TemplateView):
    template_name = 'drinkcounter/payment-success.html'

    def get(self, request):
        """
        Show form for making payments
        """
        try:
            amount = request.session.get('amount', None)
            resident_id = request.session.get('resident_id', None)
        except KeyError:
            pass

        # Get resident and beverage objects with appropriate PK
        resident = Resident.objects.get(id=int(resident_id))

        context = {
            'amount': amount,
            'resident': resident
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        """
        Delete previously added entries.
        Render payment-undo page.
        """
        try:
            payment_id = request.session.get('payment_id', None)
        except KeyError:
            pass

        Payment.objects.filter(id=int(payment_id)).delete()

        return redirect('drinkcounter:PaymentUndoView')


class PaymentUndoView(TemplateView):
    template_name = 'drinkcounter/payment-undo.html'

    def get(self, request):
        """
        Show a message that previous entry was deleted.
        """
        return render(request, self.template_name)


class BeveragePriceView(TemplateView):
    """
    Show the prices of all beverages
    """
    template_name = 'drinkcounter/beverage-prices.html'

    def get(self, request):
        """
        Show prices
        """
        beverages = Beverage.objects.all()

        context = {
            'beverages': beverages,
        }
        return render(request, self.template_name, context=context)
