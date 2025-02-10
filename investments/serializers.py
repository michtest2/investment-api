from rest_framework import serializers
from .models import InvestmentPlan, Investment


class InvestmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPlan
        fields = "__all__"  # Includes all fields from the model
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )  # Prevent updates on these fields


class InvestmentSerializer(serializers.ModelSerializer):
    plan = serializers.StringRelatedField()

    class Meta:
        model = Investment
        fields = "__all__"  # Includes all fields from the model
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )  # Prevent updates on these fields
