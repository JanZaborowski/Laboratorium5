from django.db import models


class Manhwa(models.Model):
    STATUS_CHOICES = [
        ('czytane', 'W trakcie czytania'),
        ('ukonczone', 'Przeczytane'),
        ('planowane', 'Planowane'),
        ('wstrzymane', 'Wstrzymane'),
    ]

    title = models.CharField(max_length=200, unique=True, verbose_name="Tytuł manhwy")
    author = models.CharField(max_length=150, verbose_name="Autor / Twórca")
    genre = models.CharField(max_length=100, verbose_name="Gatunek")
    publisher = models.CharField(max_length=120, default="KakaoPage", blank=True, verbose_name="Wydawca / Platforma")
    reading_status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="planowane", verbose_name="Status czytania")
    description = models.TextField(verbose_name="Opis fabuły")
    notes = models.TextField(blank=True, null=True, default="", verbose_name="Dodatkowe notatki")
    chapters_count = models.IntegerField(default=1, verbose_name="Liczba rozdziałów")
    rating = models.IntegerField(default=10, verbose_name="Ocena (1-10)")
    is_completed = models.BooleanField(default=False, verbose_name="Czy zakończona?")
    release_date = models.DateField(null=True, blank=True, verbose_name="Data premiery")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data dodania")

    class Meta:
        verbose_name = "Manhwa / Komiks"
        verbose_name_plural = "Manhwy / Komiksy"
        ordering = ['-rating', 'title']

    def __str__(self):
        pub_state = "Zakończona" if self.is_completed else "W trakcie"
        return f"{self.title} ({self.genre}) - {self.author} [{pub_state}, {self.get_reading_status_display()}]"
