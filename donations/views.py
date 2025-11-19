from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count
from .models import DonationMoney, DonationGoods
from crisis.models import CrisisPost
from .serializers import (
    DonationMoneySerializer,
    DonationMoneyCreateSerializer,
    DonationGoodsSerializer,
    DonationGoodsCreateSerializer,
    DonationSummarySerializer
)


# Create Money Donation (Authenticated or Anonymous)
class CreateMoneyDonationView(generics.CreateAPIView):
    serializer_class = DonationMoneyCreateSerializer
    permission_classes = [permissions.AllowAny]  # Allow anonymous donations
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            "success": "Thank you for your donation!",
            "data": DonationMoneySerializer(serializer.instance, context={"request": request}).data
        }, status=status.HTTP_201_CREATED)


# Create Goods Donation
class CreateGoodsDonationView(generics.CreateAPIView):
    serializer_class = DonationGoodsCreateSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            "success": "Thank you for your donation!",
            "data": DonationGoodsSerializer(serializer.instance, context={"request": request}).data
        }, status=status.HTTP_201_CREATED)


# List Money Donations for a Crisis
class CrisisMoneyDonationsView(generics.ListAPIView):
    serializer_class = DonationMoneySerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        crisis_id = self.kwargs.get('crisis_id')
        return DonationMoney.objects.filter(crisis_post_id=crisis_id)


# List Goods Donations for a Crisis
class CrisisGoodsDonationsView(generics.ListAPIView):
    serializer_class = DonationGoodsSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        crisis_id = self.kwargs.get('crisis_id')
        return DonationGoods.objects.filter(crisis_post_id=crisis_id)


# Get Donation Summary for a Crisis
class CrisisDonationSummaryView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, crisis_id):
        crisis_post = get_object_or_404(CrisisPost, id=crisis_id)
        
        # Calculate totals
        money_donations = DonationMoney.objects.filter(crisis_post=crisis_post)
        goods_donations = DonationGoods.objects.filter(crisis_post=crisis_post)
        
        total_money = money_donations.aggregate(total=Sum('amount'))['total'] or 0
        total_donors_money = money_donations.count()
        total_goods_donations = goods_donations.count()
        
        data = {
            "crisis_id": crisis_id,
            "crisis_title": crisis_post.title,
            "total_money": float(total_money),
            "total_donors_money": total_donors_money,
            "total_goods_donations": total_goods_donations,
            "money_donations": DonationMoneySerializer(money_donations, many=True).data,
            "goods_donations": DonationGoodsSerializer(goods_donations, many=True).data,
        }
        
        return Response(data)


# My Donations (for logged-in users)
class MyDonationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        money_donations = DonationMoney.objects.filter(donor=request.user)
        goods_donations = DonationGoods.objects.filter(donor=request.user)
        
        data = {
            "money_donations": DonationMoneySerializer(money_donations, many=True).data,
            "goods_donations": DonationGoodsSerializer(goods_donations, many=True).data,
            "total_money_donated": float(money_donations.aggregate(total=Sum('amount'))['total'] or 0),
            "total_donations_count": money_donations.count() + goods_donations.count()
        }
        
        return Response(data)