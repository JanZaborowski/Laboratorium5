# Katalog Manhw i Komiksów (Laboratorium 5)

Aplikacja w Django przechowująca katalog manhw i komiksów, rozbudowana o nowe pola modelu, migracje oraz operacje ORM udostępniane przez endpoint JSON.

## Uruchomienie lokalne

```bash
python manage.py migrate
python manage.py runserver
```

- Strona główna: `http://127.0.0.1:8000/`
- Endpoint API: `http://127.0.0.1:8000/api/manhwa/`
- Panel administracyjny: `http://127.0.0.1:8000/admin/`
