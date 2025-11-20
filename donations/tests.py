# donations/tests/test_donations_api.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from crisis.models import CrisisPost
from donations.models import DonationMoney, DonationGoods
from decimal import Decimal

User = get_user_model()

class DonationsAPITestCase(APITestCase):
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username="donor", email="donor@example.com", password="password123")
        self.other_user = User.objects.create_user(username="other", email="other@example.com", password="password123")

        # Create an approved crisis post
        self.crisis = CrisisPost.objects.create(
            title="Test Crisis",
            description="A test crisis",
            post_type="individual",
            owner=self.user,
            status="approved"
        )

        # Clients
        self.client = APIClient()
        self.auth_client = APIClient()
        self.auth_client.login(username="donor", password="password123")  # session auth
        # If token auth used, set credentials accordingly.

    def test_create_money_donation_anonymous(self):
        url = reverse("create_money_donation")
        payload = {
            "crisis_post": self.crisis.id,
            "donor_name": "Anonymous Donor",
            "donor_email": "anon@example.com",
            "amount": "250.00",
            "payment_method": "bkash",
            "is_anonymous": True
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data["data"]
        self.assertEqual(Decimal(str(data["amount"])), Decimal("250.00"))
        self.assertEqual(data["is_anonymous"], True)
        self.assertEqual(data["crisis_post"], self.crisis.id)

    def test_create_money_donation_authenticated(self):
        url = reverse("create_money_donation")
        payload = {
            "crisis_post": self.crisis.id,
            "amount": "500.50",
            "payment_method": "bank",
            "message": "Keep going",
            "is_anonymous": False
        }
        # Authenticate using force_authenticate or login
        self.auth_client.force_authenticate(user=self.user)
        response = self.auth_client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data["data"]
        self.assertEqual(Decimal(str(data["amount"])), Decimal("500.50"))
        # Donor should be set (user)
        donation = DonationMoney.objects.get(id=data["id"])
        self.assertEqual(donation.donor, self.user)

    def test_create_money_donation_negative_amount(self):
        url = reverse("create_money_donation")
        payload = {
            "crisis_post": self.crisis.id,
            "amount": "-10.00",
            "payment_method": "bkash"
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_donate_to_unapproved_crisis_should_fail(self):
        # create a pending crisis
        pending = CrisisPost.objects.create(
            title="Pending Crisis",
            description="Not open",
            post_type="individual",
            owner=self.user,
            status="pending"
        )
        url = reverse("create_money_donation")
        payload = {"crisis_post": pending.id, "amount": "100.00", "payment_method": "bkash"}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_goods_donation(self):
        url = reverse("create_goods_donation")
        payload = {
            "crisis_post": self.crisis.id,
            "donor_name": "Goods Donor",
            "item_description": "10 blankets, 5 bags of rice",
            "quantity": "15",
            "delivery_method": "Self-delivery",
            "is_anonymous": False
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data["data"]
        goods = DonationGoods.objects.get(id=data["id"])
        self.assertEqual(goods.crisis_post, self.crisis)
        self.assertIn("blankets", goods.item_description)

    def test_list_crisis_money_donations(self):
        # create sample donations
        DonationMoney.objects.create(crisis_post=self.crisis, donor=self.user, amount=100.00, payment_method="bkash")
        DonationMoney.objects.create(crisis_post=self.crisis, donor=None, donor_name="Guest", amount=50.00, payment_method="nagad", is_anonymous=True)

        url = reverse("crisis_money_donations", kwargs={"crisis_id": self.crisis.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_crisis_donation_summary(self):
        DonationMoney.objects.create(crisis_post=self.crisis, donor=self.user, amount=100.00, payment_method="bkash")
        DonationMoney.objects.create(crisis_post=self.crisis, donor=self.other_user, amount=200.00, payment_method="bank")
        DonationGoods.objects.create(crisis_post=self.crisis, donor=self.user, item_description="5 blankets", quantity="5")

        url = reverse("crisis_donation_summary", kwargs={"crisis_id": self.crisis.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_money", response.data)
        self.assertEqual(float(response.data["total_money"]), 300.0)
        self.assertEqual(response.data["total_goods_donations"], 1)

    def test_my_donations_requires_authentication(self):
        url = reverse("my_donations")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Now authenticated
        self.auth_client.force_authenticate(user=self.user)
        response = self.auth_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
