from datetime import date
from django.test import TestCase
from django.urls import reverse
from .models import Manhwa


class ManhwaModelAndOrmTests(TestCase):
    def setUp(self):
        self.m1 = Manhwa.objects.create(
            title="Solo Leveling",
            author="Chugong",
            genre="Akcja",
            publisher="KakaoPage",
            reading_status="ukonczone",
            description="Opis 1",
            notes="Notatka 1",
            chapters_count=179,
            rating=10,
            is_completed=True,
            release_date=date(2018, 3, 4),
        )
        self.m2 = Manhwa.objects.create(
            title="Tower of God",
            author="SIU",
            genre="Fantasy",
            publisher="Naver Webtoon",
            reading_status="wstrzymane",
            description="Opis 2",
            notes="Notatka 2",
            chapters_count=615,
            rating=9,
            is_completed=False,
            release_date=date(2010, 6, 30),
        )
        self.m3 = Manhwa.objects.create(
            title="Eleceed",
            author="Son Jaeho",
            genre="Akcja",
            publisher="Naver Webtoon",
            reading_status="czytane",
            description="Opis 3",
            notes="Notatka 3",
            chapters_count=290,
            rating=10,
            is_completed=False,
            release_date=date(2018, 10, 2),
        )

    def test_str_representation(self):
        self.assertIn("Solo Leveling", str(self.m1))
        self.assertIn("Przeczytane", str(self.m1))

    def test_api_orm_filter_and_sort(self):
        response = self.client.get(reverse('katalog:api_manhwa_list'), {'status': 'completed'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['items'][0]['title'], "Solo Leveling")
        self.assertEqual(data['items'][0]['publisher'], "KakaoPage")

    def test_api_orm_limit(self):
        response = self.client.get(reverse('katalog:api_manhwa_list'), {'sort': 'title', 'limit': '2'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 2)
        self.assertEqual(data['items'][0]['title'], "Eleceed")

    def test_api_detail_single_record(self):
        response = self.client.get(reverse('katalog:api_manhwa_detail', args=[self.m2.id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['item']['title'], "Tower of God")
