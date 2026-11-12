from django.shortcuts import render
from django.http import JsonResponse
from .models import Manhwa


def serialize_manhwa(item):
    return {
        'id': item.id,
        'title': item.title,
        'author': item.author,
        'genre': item.genre,
        'publisher': item.publisher,
        'reading_status': item.reading_status,
        'reading_status_display': item.get_reading_status_display(),
        'chapters_count': item.chapters_count,
        'rating': item.rating,
        'is_completed': item.is_completed,
        'release_date': item.release_date.strftime('%Y-%m-%d') if item.release_date else None,
        'description': item.description,
        'notes': item.notes or '',
    }


def index(request):
    # 1. pobranie wszystkich rekordow z sortowaniem (order_by)
    items = Manhwa.objects.all().order_by('title')

    # 2. filtrowanie wedlug wybranego pola (filter)
    completed_items = Manhwa.objects.filter(is_completed=True)
    reading_items = Manhwa.objects.filter(reading_status='czytane')

    # 3. ograniczenie wynikow ([:N]) oraz pobranie pojedynczego rekordu (first)
    latest_items = Manhwa.objects.order_by('-id')[:5]
    top_item = Manhwa.objects.order_by('-rating', '-chapters_count').first()

    return render(request, 'katalog/index.html', {
        'total_manhwa': items.count(),
        'completed_count': completed_items.count(),
        'reading_count': reading_items.count(),
        'latest_items': latest_items,
        'top_item': top_item,
    })


def api_manhwa_list(request):
    # pobranie wszystkich rekordow z sortowaniem domyslnym
    queryset = Manhwa.objects.all().order_by('-rating', 'title')

    # filtrowanie wedlug statusu zakonczenia serii
    status_param = request.GET.get('status')
    if status_param == 'completed':
        queryset = queryset.filter(is_completed=True)
    elif status_param == 'ongoing':
        queryset = queryset.filter(is_completed=False)

    # filtrowanie wedlug statusu czytania
    reading_param = request.GET.get('reading_status')
    if reading_param and reading_param != 'all':
        queryset = queryset.filter(reading_status=reading_param)

    # filtrowanie wedlug gatunku
    genre_param = request.GET.get('genre')
    if genre_param and genre_param != 'all':
        queryset = queryset.filter(genre=genre_param)

    # filtrowanie wedlug wydawcy
    publisher_param = request.GET.get('publisher')
    if publisher_param and publisher_param != 'all':
        queryset = queryset.filter(publisher=publisher_param)

    # sortowanie po stronie ORM
    sort_param = request.GET.get('sort', '-rating')
    allowed_sorts = {
        'title': ('title',),
        '-title': ('-title',),
        '-rating': ('-rating', 'title'),
        '-chapters': ('-chapters_count', 'title'),
        '-id': ('-id',),
        'release_date': ('release_date',),
    }
    if sort_param in allowed_sorts:
        queryset = queryset.order_by(*allowed_sorts[sort_param])

    # ograniczenie liczby wynikow ([:N])
    limit_param = request.GET.get('limit')
    if limit_param and limit_param.isdigit():
        limit_val = int(limit_param)
        if limit_val > 0:
            queryset = queryset[:limit_val]

    items = [serialize_manhwa(item) for item in queryset]

    return JsonResponse({
        'items': items,
        'count': len(items),
    })


def api_manhwa_detail(request, pk):
    try:
        # pobranie pojedynczego rekordu przez get()
        item = Manhwa.objects.get(pk=pk)
        return JsonResponse({'item': serialize_manhwa(item)})
    except Manhwa.DoesNotExist:
        return JsonResponse({'error': 'Nie znaleziono rekordu o podanym ID.'}, status=404)
