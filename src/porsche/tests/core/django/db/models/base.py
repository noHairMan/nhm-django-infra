import datetime
from uuid import UUID

from porsche.core.restframework import PorscheAPITestCase
from porsche.models import Company


class TestPorscheModel(PorscheAPITestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test Company")

    def test_model_creation(self):
        self.assertIsInstance(self.company.uid, UUID)
        self.assertIsInstance(self.company.create_time, datetime.datetime)
        self.assertIsInstance(self.company.update_time, datetime.datetime)
        self.assertFalse(self.company.deleted)

    def test_soft_delete(self):
        self.company.delete(soft=True)
        company = Company.objects.get(uid=self.company.uid)
        self.assertTrue(company.deleted)

    def test_hard_delete(self):
        self.company.delete(soft=False)
        with self.assertRaises(Company.DoesNotExist):
            Company.objects.get(uid=self.company.uid)

    # def test_related_objects_soft_delete(self):
    #     self.company.delete(soft=True)
    #     employee = TestEmployeeModel.objects.get(uid=self.employee.uid)
    #     self.assertTrue(employee.deleted)
