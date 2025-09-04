from porsche.core.restframework import PorscheAPITestCase
from porsche.core.restframework.response import PorscheResponse
from porsche.models.enums import BusinessCode


class TestPorscheResponse(PorscheAPITestCase):
    def test_response(self):
        self.assertEqual(
            PorscheResponse(BusinessCode.SUCCESS).business_code,
            PorscheResponse(BusinessCode.SUCCESS.value).business_code,
        )
