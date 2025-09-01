import datetime
from uuid import UUID

from django.test import TestCase


class TestPorscheModel(TestCase):
    def setUp(self):
        self.company = TestCompanyModel.objects.create(name="Test Company")
        self.employee = TestEmployeeModel.objects.create(name="Test Employee", company=self.company)

    def test_model_creation(self):
        self.assertIsInstance(self.company.uid, UUID)
        self.assertIsInstance(self.company.create_time, datetime.datetime)
        self.assertIsInstance(self.company.update_time, datetime.datetime)
        self.assertFalse(self.company.deleted)

    def test_soft_delete(self):
        self.company.delete(soft=True)
        company = TestCompanyModel.objects.get(uid=self.company.uid)
        self.assertTrue(company.deleted)

    def test_hard_delete(self):
        self.company.delete(soft=False)
        with self.assertRaises(TestCompanyModel.DoesNotExist):
            TestCompanyModel.objects.get(uid=self.company.uid)

    def test_related_objects_soft_delete(self):
        self.company.delete(soft=True)
        employee = TestEmployeeModel.objects.get(uid=self.employee.uid)
        self.assertTrue(employee.deleted)
