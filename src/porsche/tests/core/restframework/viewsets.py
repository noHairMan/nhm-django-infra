from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from porsche.api.endpoints import HealthCheckView
from porsche.core.restframework import (
    PorscheModelSerializer,
    PorscheModelViewSet,
    PorscheSerializer,
)
from porsche.core.restframework.exceptions import PorscheServerException
from porsche.core.restframework.response import PorscheResponse
from porsche.core.restframework.test import PorscheAPITestCase
from porsche.core.restframework.validators import PorscheUniqueTogetherValidator
from porsche.models import Tag
from porsche.models.enums import BusinessCode, ViewAction


class TagSerializer(PorscheModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class TagCreateSerializer(PorscheModelSerializer):
    category = serializers.ChoiceField(choices=Tag.Category.choices)

    class Meta:
        model = Tag
        fields = ["name", "category"]
        validators = [
            PorscheUniqueTogetherValidator(
                queryset=Tag.objects.all(),
                fields=["name", "category"],
            ),
        ]

    def create(self, validated_data):
        ret = super().create(validated_data)
        raise ValidationError("test transaction")
        return ret

    def update(self, instance, validated_data):
        ret = super().update(instance, validated_data)
        raise ValidationError("test transaction")
        return ret


TagUpdateSerializer = TagCreateSerializer


class TagListSerializer(PorscheModelSerializer):
    class Meta:
        model = Tag
        fields = ["uid", "name", "category"]


class TagRetrieveSerializer(PorscheModelSerializer):
    class Meta:
        model = Tag
        fields = ["uid", "name", "category"]


class TagViewSet(PorscheModelViewSet):
    queryset = Tag.objects.all()
    create_serializer_class = TagCreateSerializer
    list_serializer_class = TagListSerializer
    retrieve_serializer_class = TagRetrieveSerializer
    update_serializer_class = TagUpdateSerializer


class TestPorscheModelViewSet(PorscheAPITestCase):

    def setUp(self):
        self.view = TagViewSet()
        self.data = {"name": "Test Tag", "category": Tag.Category.COMPANY}

    def test_metadata(self):
        self.view.action = ViewAction.METADATA
        serializer_class = self.view.get_serializer_class()
        self.assertEqual(serializer_class, PorscheSerializer)

    def test_list(self):
        self.view.action = ViewAction.LIST
        serializer_class = self.view.get_serializer_class()
        self.assertEqual(serializer_class, TagListSerializer)

    def test_retrieve(self):
        self.view.action = ViewAction.RETRIEVE
        serializer_class = self.view.get_serializer_class()
        self.assertEqual(serializer_class, TagRetrieveSerializer)

    def test_create(self):
        self.view.action = ViewAction.CREATE
        serializer_class = self.view.get_serializer_class()
        self.assertEqual(serializer_class, TagCreateSerializer)

        serializer = serializer_class(data=self.data)
        serializer.is_valid(raise_exception=True)
        with self.assertRaises(ValidationError):
            self.view.perform_create(serializer)
        self.assertFalse(Tag.objects.filter(name=self.data["name"]).exists())

    def test_update(self):
        self.view.action = ViewAction.UPDATE
        serializer_class = self.view.get_serializer_class()
        self.assertEqual(serializer_class, TagUpdateSerializer)

        instance = Tag.objects.create(**self.data)
        serializer = serializer_class(instance, data=self.data | {"name": "New Name"})
        serializer.is_valid(raise_exception=True)
        with self.assertRaises(ValidationError):
            self.view.perform_update(serializer)
        self.assertFalse(Tag.objects.filter(name="New Name").exists())

    def test_destroy(self):
        self.view.action = ViewAction.DESTROY
        serializer_class = self.view.get_serializer_class()
        self.assertEqual(serializer_class, PorscheSerializer)

        instance = Tag.objects.create(**self.data)
        original_delete = instance.delete

        def mock_delete_error():
            original_delete()
            raise PorscheServerException

        instance.delete = mock_delete_error
        with self.assertRaises(PorscheServerException):
            self.view.perform_destroy(instance)
        self.assertTrue(Tag.objects.filter(name=self.data["name"]).exists())

    def test_no_serializer_class(self):
        self.view.action = ViewAction.METADATA
        self.view.serializer_class = None
        with self.assertRaises(PorscheServerException):
            self.view.get_serializer_class()

    def test_finalize_response(self):
        request = self.request_factory.get("/api/health/")
        view = HealthCheckView()
        porsche_request = view.initialize_request(request)
        view.initial(porsche_request)

        porsche_response = PorscheResponse(data={"foo": "bar"}, code=BusinessCode.BAD_REQUEST)
        final_response = view.finalize_response(porsche_request, porsche_response)
        self.assertIsInstance(final_response, PorscheResponse)

        response = Response(data={"foo": "bar"})
        final_response = view.finalize_response(porsche_request, response)
        self.assertIsInstance(final_response, PorscheResponse)
        self.assertEqual(final_response.business_code, BusinessCode.SUCCESS)
