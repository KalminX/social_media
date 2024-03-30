from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='password')
        self.user2 = User.objects.create_user(
            username='user2', password='password')

    def test_profile_creation(self):
        self.assertEqual(Profile.objects.count(), 2)

    def test_profile_follows(self):
        self.user1.profile.follows.add(self.user2.profile)
        self.assertIn(self.user2.profile, self.user1.profile.follows.all())

    def test_profile_str(self):
        self.assertEqual(str(self.user1.profile), 'user1')


class ProfileCreationTest(TestCase):
    def test_profile_created(self):
        user = User.objects.create_user(username='user3', password='password')
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.first().user, user)


class ProfileUpdateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user4', password='password')
        self.profile = self.user.profile

    def test_profile_update(self):
        self.user.username = 'new_username'
        self.user.save()
        self.assertEqual(self.profile.user.username, 'new_username')


class ProfileDeletionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user5', password='password')

    def test_profile_deletion(self):
        self.user.delete()
        self.assertEqual(Profile.objects.count(), 0)


class ProfileFollowTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='password')
        self.user2 = User.objects.create_user(
            username='user2', password='password')

    def test_profile_follow(self):
        self.user1.profile.follows.add(self.user2.profile)
        self.assertIn(self.user2.profile, self.user1.profile.follows.all())

    def test_profile_unfollow(self):
        self.user1.profile.follows.add(self.user2.profile)
        self.user1.profile.follows.remove(self.user2.profile)
        self.assertNotIn(self.user2.profile, self.user1.profile.follows.all())


class ProfileSelfFollowTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='password')

    def test_profile_self_follow(self):
        self.user1.profile.follows.add(self.user1.profile)
        self.assertNotIn(self.user1.profile, self.user1.profile.follows.all())


class ProfileMultipleFollowTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='password')
        self.user2 = User.objects.create_user(
            username='user2', password='password')

    def test_profile_multiple_follow(self):
        self.user1.profile.follows.add(self.user2.profile)
        self.user1.profile.follows.add(self.user2.profile)
        self.assertEqual(self.user1.profile.follows.count(), 1)


class ProfileFollowNonExistentUserTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='password')

    def test_profile_follow_non_existent_user(self):
        with self.assertRaises(ObjectDoesNotExist):
            non_existent_user = User.objects.get(username='non_existent_user')
            self.user1.profile.follows.add(non_existent_user.profile)


class ProfileUnfollowNotFollowedUserTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='password')
        self.user2 = User.objects.create_user(
            username='user2', password='password')

    def test_profile_unfollow_not_followed_user(self):
        self.user1.profile.follows.remove(self.user2.profile)
        self.assertNotIn(self.user2.profile, self.user1.profile.follows.all())
