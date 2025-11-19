from rest_framework import serializers
from .models import DonationMoney, DonationGoods

class DonationMoneySerializer(serializers.ModelSerializer):
    display_name = serializers.ReadOnlyField()
    crisis_title = serializers.ReadOnlyField(source='crisis_post.title')
    
    class Meta:
        model = DonationMoney
        fields = [
            "id",
            "crisis_post",
            "crisis_title",
            "display_name",
            "amount",
            "payment_method",
            "transaction_id",
            "message",
            "is_anonymous",
            "donated_at"
        ]
        read_only_fields = ["donor", "donated_at", "display_name"]


class DonationMoneyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationMoney
        fields = [
            "crisis_post",
            "donor_name",
            "donor_email",
            "donor_phone",
            "amount",
            "payment_method",
            "transaction_id",
            "message",
            "is_anonymous"
        ]
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value
    
    def validate_crisis_post(self, value):
        if value.status != 'approved':
            raise serializers.ValidationError("You can only donate to approved crisis posts.")
        return value
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['donor'] = request.user
        return super().create(validated_data)


class DonationGoodsSerializer(serializers.ModelSerializer):
    display_name = serializers.ReadOnlyField()
    crisis_title = serializers.ReadOnlyField(source='crisis_post.title')
    
    class Meta:
        model = DonationGoods
        fields = [
            "id",
            "crisis_post",
            "crisis_title",
            "display_name",
            "item_description",
            "quantity",
            "delivery_method",
            "message",
            "is_anonymous",
            "donated_at"
        ]
        read_only_fields = ["donor", "donated_at", "display_name"]


class DonationGoodsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationGoods
        fields = [
            "crisis_post",
            "donor_name",
            "donor_email",
            "donor_phone",
            "item_description",
            "quantity",
            "delivery_method",
            "message",
            "is_anonymous"
        ]
    
    def validate_crisis_post(self, value):
        if value.status != 'approved':
            raise serializers.ValidationError("You can only donate to approved crisis posts.")
        return value
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['donor'] = request.user
        return super().create(validated_data)


class DonationSummarySerializer(serializers.Serializer):
    """Summary of donations for a crisis post"""
    total_money = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_donors_money = serializers.IntegerField()
    total_goods_donations = serializers.IntegerField()
    money_donations = DonationMoneySerializer(many=True)
    goods_donations = DonationGoodsSerializer(many=True)