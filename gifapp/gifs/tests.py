from django.test import TestCase
from django.contrib.auth.models import User

from .models import GifToUser, GifToUserCategory


class GifToUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', password='hello')
        GifToUser.objects.create(gif_url="hey.com/1234", user=self.user)
        GifToUser.objects.create(gif_url="hey.com/2345", user=self.user)

        self.catUser = User.objects.create_user(
            username='cat-tester', password='hello')
        gtuPuppy = GifToUser.objects.create(
            gif_url="hey.com/puppy", user=self.catUser)
        gtuBear = GifToUser.objects.create(
            gif_url="hey.com/bear", user=self.catUser)

        GifToUserCategory.objects.create(
            gif_to_user=gtuPuppy, category="furry")
        GifToUserCategory.objects.create(gif_to_user=gtuPuppy, category="pet")

        GifToUserCategory.objects.create(gif_to_user=gtuBear, category="furry")

    def test_get_user_gifs_for_category_all(self):
        gifs_with_cats = GifToUser.get_user_gifs_for_category(self.user)
        self.assertEqual(len(gifs_with_cats), 2)
        gif, cats = gifs_with_cats[0]
        self.assertEqual(len(cats), 0)

        gifs_with_cats = GifToUser.get_user_gifs_for_category(self.catUser)
        self.assertEqual(len(gifs_with_cats), 2)

    def test_get_user_gifs_for_category_filter(self):
        gifs_with_cats = GifToUser.get_user_gifs_for_category(
            self.user, 'furry')
        self.assertEqual(len(gifs_with_cats), 0)

        gifs_with_cats = GifToUser.get_user_gifs_for_category(
            self.catUser, 'furry')
        self.assertEqual(len(gifs_with_cats), 2)

        gifs_with_cats = GifToUser.get_user_gifs_for_category(
            self.catUser, 'pet')
        self.assertEqual(len(gifs_with_cats), 1)

    def test_get_user_categories(self):
        cats = GifToUserCategory.get_user_categories(self.user)
        self.assertEqual(len(cats), 0)

        cats = GifToUserCategory.get_user_categories(self.catUser)
        self.assertEqual(len(cats), 2)
