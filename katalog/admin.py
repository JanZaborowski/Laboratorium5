from django.contrib import admin
from .models import Manhwa


@admin.register(Manhwa)
class ManhwaAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'genre',
        'publisher',
        'reading_status',
        'chapters_count',
        'rating',
        'is_completed',
        'release_date',
    )
    list_editable = ('reading_status', 'rating', 'chapters_count', 'is_completed')
    list_filter = ('reading_status', 'is_completed', 'genre', 'publisher', 'rating')
    search_fields = ('title', 'author', 'genre', 'publisher', 'description', 'notes')
    ordering = ('-rating', 'title')
