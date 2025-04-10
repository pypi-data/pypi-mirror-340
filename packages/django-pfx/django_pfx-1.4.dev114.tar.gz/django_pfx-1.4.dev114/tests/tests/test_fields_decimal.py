from decimal import Decimal

from django.db import connection, models
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import include, path

from pfx.pfxcore import register_views
from pfx.pfxcore.decorator import rest_view
from pfx.pfxcore.fields import DecimalField
from pfx.pfxcore.models import JSONReprMixin
from pfx.pfxcore.test import APIClient, TestAssertMixin
from pfx.pfxcore.views import RestView
from tests.views import FakeViewMixin


class TestDecimalModel(JSONReprMixin, models.Model):
    decimal = DecimalField(
        max_digits=10, decimal_places=5, json_decimal_places=2)

    class Meta:
        verbose_name = "TestModel"
        verbose_name_plural = "TestModels"
        ordering = ['pk']


@rest_view("/test-decimal-model")
class DecimalModelRestView(FakeViewMixin, RestView):
    default_public = True
    model = TestDecimalModel
    fields = ['decimal']


urlpatterns = [
    path('api/', include(register_views(DecimalModelRestView))),
    path('api/', include('pfx.pfxcore.urls'))
]


@override_settings(ROOT_URLCONF=__name__)
class TestFieldsDecimal(TestAssertMixin, TestCase):

    def setUp(self):
        self.client = APIClient(default_locale='en')

    @classmethod
    def setUpTestData(cls):
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(TestDecimalModel)

    def test_decimal(self):
        t = TestDecimalModel.objects.create(decimal=3.14)
        t.save()
        t.refresh_from_db()
        self.assertEqual(t.decimal, Decimal('3.14000'))

        response = self.client.get(f'/api/test-decimal-model/{t.pk}')
        self.assertRC(response, 200)
        self.assertJE(response, 'decimal', "3.14")
