from django.test import TestCase
from .models import Material, MaterialType, UnitLookup, Restaurant
from .views import total_amount
from django.test.client import RequestFactory

# Create your tests here.

rf = RequestFactory()


class TotalAmountTests(TestCase):

    def setUp(self):
        rest = Restaurant.objects.create(name='Two Cats')
        lbs = UnitLookup.objects.create(name='pounds')
        lbs.save()
        bacon = MaterialType.objects.create(name='bacon', buy_unit=lbs, sell_unit=lbs, buy_unit_cost=10.50, sell_unit_cost=15.99)
        bacon.save()
        m1 = Material.objects.create(initial_amount=10, current_amount=8.5, prepared_amount=3.3, expiration_date='2019-01-20', material_type=bacon, restaurant=rest)
        m1.save()

    def first_test(self):
        mock_request = rf.request()
        response = total_amount(mock_request, 'bacon')
        self.assertEqual('bacon: 8.50 pounds', response.content.decode('utf-8'))
