from porsche.core.restframework import PorscheAPITestCase, PorscheModelSerializer
from porsche.models import Company


class TestSerializer(PorscheAPITestCase):

    def test_porsche_model_serializer(self):
        # 创建测试数据
        company1 = Company.objects.create(name="company1")

        class Serializer(PorscheModelSerializer):
            class Meta:
                model = Company
                fields = ["name"]

        serializer = Serializer(instance=company1, data={"name": "company2"})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(company1.name, "company2")
