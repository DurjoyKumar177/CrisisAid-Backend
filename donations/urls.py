from django.urls import path
from .views import (
    CreateMoneyDonationView,
    CreateGoodsDonationView,
    CrisisMoneyDonationsView,
    CrisisGoodsDonationsView,
    CrisisDonationSummaryView,
    MyDonationsView
)

urlpatterns = [
    # Create donations
    path("money/create/", CreateMoneyDonationView.as_view(), name="create_money_donation"),
    path("goods/create/", CreateGoodsDonationView.as_view(), name="create_goods_donation"),
    
    # View donations for a crisis
    path("crisis/<int:crisis_id>/money/", CrisisMoneyDonationsView.as_view(), name="crisis_money_donations"),
    path("crisis/<int:crisis_id>/goods/", CrisisGoodsDonationsView.as_view(), name="crisis_goods_donations"),
    path("crisis/<int:crisis_id>/summary/", CrisisDonationSummaryView.as_view(), name="crisis_donation_summary"),
    
    # My donations
    path("my-donations/", MyDonationsView.as_view(), name="my_donations"),
]