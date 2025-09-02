import datetime
from uuid import UUID, uuid4

from porsche.core.django.db.models.base import get_object
from porsche.core.restframework import PorscheAPITestCase
from porsche.models import Company


class TestPorscheModel(PorscheAPITestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test Company")

    def test_create_model(self):
        """Test basic model creation and field validation"""
        self.assertIsInstance(self.company.uid, UUID)
        self.assertFalse(self.company.deleted)
        self.assertIsInstance(self.company.uid, UUID)
        self.assertIsInstance(self.company.create_time, datetime.datetime)
        self.assertIsInstance(self.company.update_time, datetime.datetime)

    def test_update_model(self):
        """Test basic model update"""
        create_time, update_time = self.company.create_time, self.company.update_time
        self.company.name = "New Name"
        self.company.save()
        self.assertEqual(self.company.name, "New Name")
        self.assertEqual(self.company.create_time, create_time)
        self.assertNotEqual(self.company.update_time, update_time)

    def test_soft_delete(self):
        """Test soft delete functionality"""
        self.company.delete(soft=True)
        self.assertTrue(self.company.deleted)

        # Object should still exist in database
        company = Company._objects.get(id=self.company.id)
        self.assertTrue(company.deleted)
        with self.assertRaises(Company.DoesNotExist):
            Company.objects.get(id=self.company.id)

    def test_hard_delete(self):
        """Test hard delete functionality"""
        self.company.delete(soft=False)

        # Object should be removed from database
        with self.assertRaises(Company.DoesNotExist):
            Company._objects.get(id=self.company.id)

    def test_get_object(self):
        """Test get_object utility function"""
        # Test existing object
        company = get_object(Company, name="Test Company")
        self.assertEqual(company, self.company)
        company = get_object(Company, uid=self.company.uid)
        self.assertEqual(company, self.company)
        company = get_object(Company, uid=uuid4())
        self.assertIsNone(company)

        # Test non-existing object
        company = get_object(Company, name="Non Existing")
        self.assertIsNone(company)

        # Test raise_exception
        with self.assertRaises(Company.DoesNotExist):
            get_object(Company, raise_exception=True, name="Non Existing")
