from porsche.core.restframework import PorscheAPITestCase
from porsche.models.company import Company
from porsche.models.enums import BusinessCode


class TestCompanyEndpointTestCase(PorscheAPITestCase):
    def test_search_company(self):
        company = Company.objects.create(name="Test Company")
        response = self.client.get(f"/api/company/{company.uid}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["code"], BusinessCode.SUCCESS)

        self._search_company("sd", company, False)
        self._search_company("Test", company, True)
        self._search_company("test", company, True)

    def _search_company(self, name: str, company: Company, exists: bool = False):
        response = self.client.get(f"/api/company/", query_params={"search": name})
        self.assertEqual(response.status_code, 200)
        results = response.json()
        if exists:
            self.assertEqual(results["data"]["count"], 1)
            self.assertEqual(results["data"]["results"][0]["name"], company.name)
        else:
            self.assertEqual(results["data"]["count"], 0)

    def test_order_company(self):
        company_a = Company(name="A Company")
        company_z = Company(name="Z Company")
        Company.objects.bulk_create(
            [
                company_a,
                company_z,
            ],
        )

        self._order_company("name", company_a)
        self._order_company("-name", company_z)

    def _order_company(self, order: str, company: Company):
        response = self.client.get(f"/api/company/", query_params={"ordering": order, "size": 1})
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEqual(results["data"]["count"], 2)
        self.assertEqual(results["data"]["results"][0]["name"], company.name)
