from random import randrange

from django.test import TestCase
from django.urls import reverse

from drinkcounter.forms import create_resident_choice_values
from drinkcounter.models import Beverage, Consumption, Resident


def create_resident(room_number, name='Dummy', moved_out=False):
    """
    Create an internal resident that belongs to the kitchen
    :param name: Name of the resident
    """
    return Resident.objects.create(room_number=room_number, name=name, moved_out=moved_out)


def create_consumption():
    """
    Create a consumption in the database
    """
    resident = Resident.objects.create(room_number=000, name='Dummy')
    beverage = Beverage.objects.create(name='Almduder', price=1.0)
    return Consumption.objects.create(resident=resident, beverage=beverage)


class ResidentOverviewViewTests(TestCase):

    def test_resident_is_internal(self):
        """
        If resident_external is empty and resident_internal's length is 2
        this test will pass
        """
        create_resident(room_number=235)
        create_resident(room_number=248)
        response = self.client.get(reverse('drinkcounter:OverviewView'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['resident_external'], [])
        self.assertEqual(len(response.context['resident_internal']), 2)

    def test_resident_is_external(self):
        """
        If resident_internal is empty and resident_external's length is 2
        this test will pass
        """
        create_resident(room_number=234)
        create_resident(room_number=249)
        response = self.client.get(reverse('drinkcounter:OverviewView'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['resident_internal'], [])
        self.assertEqual(len(response.context['resident_external']), 2)


class ResidentAddBeverageViewTests(TestCase):

    def test_resident_choice_form(self):
        """
        Check that the resident choice field is populated with the correct residents in the right order
        """
        response = self.client.get(reverse('drinkcounter:AddBeverageView'))
        self.assertEqual(response.status_code, 200)
        pass

    def test_create_resident_choice_values(self):
        """
        Test that the PrimaryKeys match the Residents
        """
        # Create a couple of residents
        create_resident(room_number=235, name='Jonas')
        create_resident(room_number=248, name='Nico')
        create_resident(room_number=233)
        create_resident(room_number=249, name='Test')
        create_resident(room_number=246, name='Simon', moved_out=True)
        residents = create_resident_choice_values()

        # Split resident to keep only the name

        for resident in residents:
            resident_pk = resident[0]
            resident_name_room = resident[1]
            r = Resident.objects.get(id=resident_pk)
            resident_name_room = resident_name_room.split(" ", 1)
            self.assertEqual(r.name, resident_name_room[0])

    def test_correct_number_of_beverages_added(self):
        """
        Test that the correct number of beverages gets added to the DB
        """
        create_consumption()
        rand_len = randrange(0, 20)
        for i in range(1, rand_len):
            create_consumption()
        c = Consumption.objects.all()
        self.assertEqual(rand_len, len(c))
