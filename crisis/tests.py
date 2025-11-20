from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from crisis.models import CrisisPost, PostSection

User = get_user_model()


class CrisisPostTests(APITestCase):

    def setUp(self):
        # Users
        self.user = User.objects.create_user(
            username="user1", email="u1@test.com", password="pass123"
        )
        self.other_user = User.objects.create_user(
            username="user2", email="u2@test.com", password="pass123"
        )
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="pass123"
        )

        # Auth URLs
        self.list_url = reverse("crisispost-list")

        # Sample post
        self.post = CrisisPost.objects.create(
            title="Flood in District X",
            description="Heavy flooding...",
            post_type="district",
            location="District X",
            owner=self.user,
            status="approved"
        )

    # ------------------------------
    # Create Post
    # ------------------------------
    def test_user_can_create_crisis_post(self):
        self.client.login(username="user1", password="pass123")

        data = {
            "title": "Cyclone approaching",
            "description": "Stay safe...",
            "post_type": "national",
            "location": "Bangladesh"
        }

        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CrisisPost.objects.count(), 2)
        self.assertEqual(CrisisPost.objects.last().owner, self.user)

    # ------------------------------
    # Anonymous cannot create
    # ------------------------------
    def test_anonymous_cannot_create_post(self):
        data = {
            "title": "Test",
            "description": "Test",
            "post_type": "national"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ------------------------------
    # List shows only approved posts to normal users
    # ------------------------------
    def test_list_only_shows_approved_posts(self):
        # Create a pending post
        CrisisPost.objects.create(
            title="Pending Post",
            description="Not approved yet",
            post_type="district",
            owner=self.other_user,
            status="pending"
        )

        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 1)  # Only approved post is visible

    # ------------------------------
    # Admin sees ALL posts
    # ------------------------------
    def test_admin_sees_all_posts(self):
        self.client.login(username="admin", password="pass123")
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), CrisisPost.objects.count())

    # ------------------------------
    # Owner can update post
    # ------------------------------
    def test_owner_can_update_post(self):
        self.client.login(username="user1", password="pass123")
        url = reverse("crisispost-detail", args=[self.post.id])

        response = self.client.patch(url, {"title": "Updated Title"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Title")

    # ------------------------------
    # Non-owner cannot update post
    # ------------------------------
    def test_non_owner_cannot_update_post(self):
        self.client.login(username="user2", password="pass123")
        url = reverse("crisispost-detail", args=[self.post.id])

        response = self.client.patch(url, {"title": "Hacked"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ------------------------------
    # Admin Approve Action
    # ------------------------------
    def test_admin_can_approve_post(self):
        self.client.login(username="admin", password="pass123")

        # Create a pending post
        pending_post = CrisisPost.objects.create(
            title="To Approve",
            description="Pending...",
            post_type="district",
            owner=self.user,
            status="pending"
        )

        url = reverse("crisispost-approve", args=[pending_post.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pending_post.refresh_from_db()
        self.assertEqual(pending_post.status, "approved")

    # ------------------------------
    # Admin Reject Action
    # ------------------------------
    def test_admin_can_reject_post(self):
        self.client.login(username="admin", password="pass123")

        pending_post = CrisisPost.objects.create(
            title="To Reject",
            description="Pending...",
            post_type="district",
            owner=self.user,
            status="pending"
        )

        url = reverse("crisispost-reject", args=[pending_post.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pending_post.refresh_from_db()
        self.assertEqual(pending_post.status, "rejected")

    # ------------------------------
    # my_posts endpoint
    # ------------------------------
    def test_my_posts_lists_only_user_posts(self):
        self.client.login(username="user1", password="pass123")

        url = reverse("crisispost-my-posts")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), CrisisPost.objects.filter(owner=self.user).count())

    # ------------------------------
    # PostSection creation + serializer test
    # ------------------------------
    def test_post_has_sections(self):
        section = PostSection.objects.create(
            post=self.post,
            section_type="updates",
            content="Update 1",
            created_by=self.user
        )

        url = reverse("crisispost-detail", args=[self.post.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["sections"]), 1)
        self.assertEqual(response.data["sections"][0]["section_type"], "updates")
        self.assertEqual(response.data["sections"][0]["creator_name"], "user1")
