from porsche.core.exceptions import PorscheException
from porsche.core.restframework import PorscheAPITestCase


class TestPorscheException(PorscheAPITestCase):
    def test_porsche_exception(self):
        error_string = "PorscheResponse"
        error = PorscheException(error_string)
        self.assertEqual(error.detail, error_string)
        self.assertEqual(str(error), error_string)
        self.assertEqual(PorscheException().detail, PorscheException.default_detail)
