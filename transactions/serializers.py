from rest_framework import serializers
from .models import Transaction, Withdrawal, Deposit
from investments.models import InvestmentPlan
from investments.serializers import InvestmentPlanSerializer


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the user's string representation

    class Meta:
        model = Transaction
        fields = "__all__"  # Includes all fields from the model
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )  # Prevent updates on these fields


class WithdrawalSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # transaction = serializers.StringRelatedField()

    class Meta:
        model = Withdrawal
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def get_user(self, obj):
        # Return the user's string representation
        return str(obj.user)

    def create(self, validated_data):
        # Set the user from the request context
        validated_data["user"] = self.context["user"]
        return super().create(validated_data)


class DepositSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # user = serializers.StringRelatedField()  # Display the user's string representation
    # transaction = TransactionSerializer()  # Display the transaction's data
    plan = serializers.SerializerMethodField()

    class Meta:
        model = Deposit
        fields = "__all__"  # Includes all fields from the model
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )  # Prevent updates on these fields

    def get_user(self, obj):
        # Return the user's string representation
        return str(obj.user)

    def create(self, validated_data):
        # Set the user from the request context
        validated_data["user"] = self.context["user"]
        return super().create(validated_data)

    def get_plan(self, obj):
        plan = InvestmentPlan.objects.get(name=self.context["plan_name"])
        obj.plan = plan
        obj.save()
        return InvestmentPlanSerializer(plan).data["name"]
