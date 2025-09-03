import datetime
from uuid import UUID, uuid4

from porsche.core.django.db.models.base import get_object
from porsche.core.restframework import PorscheAPITestCase
from porsche.models import Company, CompanyTag, Tag


class TestPorscheModel(PorscheAPITestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test Company")
        self.tag = Tag.objects.create(name="Test Tag")
        self.company_tag = CompanyTag.objects.create(company=self.company, tag=self.tag)

    def test_create(self):
        self.assertIsInstance(self.company.uid, UUID)
        self.assertFalse(self.company.deleted)
        self.assertIsInstance(self.company.uid, UUID)
        self.assertIsInstance(self.company.create_time, datetime.datetime)
        self.assertIsInstance(self.company.update_time, datetime.datetime)

    def test_update(self):
        create_time, update_time = self.company.create_time, self.company.update_time
        self.company.name = "New Name"
        self.company.save()
        self.assertEqual(self.company.name, "New Name")
        self.assertEqual(self.company.create_time, create_time)
        self.assertNotEqual(self.company.update_time, update_time)

    def test_soft_delete(self):
        print("soft delete", self.company.delete(soft=True))
        self.assertTrue(self.company.deleted)

        company = Company._objects.get(id=self.company.id)
        self.assertTrue(company.deleted)
        with self.assertRaises(Company.DoesNotExist):
            Company.objects.get(id=self.company.id)

    def test_hard_delete(self):
        print("hard delete", self.company.delete(soft=False))
        with self.assertRaises(Company.DoesNotExist):
            Company._objects.get(id=self.company.id)

    def test_get_related_objects(self):
        self.assertIn("company_tag", [obj.name for obj in self.company.get_related_objects()])
        self.assertIn("company_tag", [obj.name for obj in self.tag.get_related_objects()])
        self.assertListEqual(self.company_tag.get_related_objects(), [])


class TestGetObject(PorscheAPITestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test Company")

    def test_get_object(self):
        company = get_object(Company, name="Test Company")
        self.assertEqual(company, self.company)
        company = get_object(Company, uid=self.company.uid)
        self.assertEqual(company, self.company)
        company = get_object(Company, uid=uuid4())
        self.assertIsNone(company)

        company = get_object(Company, name="Non Existing")
        self.assertIsNone(company)

        with self.assertRaises(Company.DoesNotExist):
            get_object(Company, raise_exception=True, name="Non Existing")
