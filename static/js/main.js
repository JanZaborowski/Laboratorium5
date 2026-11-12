document.addEventListener('DOMContentLoaded', () => {
    const loadBtn = document.getElementById('loadDataBtn');
    const clearBtn = document.getElementById('clearBtn');
    const filterStatus = document.getElementById('filterStatus');
    const filterReading = document.getElementById('filterReading');
    const filterGenre = document.getElementById('filterGenre');
    const sortOrder = document.getElementById('sortOrder');
    const limitResults = document.getElementById('limitResults');
    const manhwaContainer = document.getElementById('manhwaContainer');
    const loadingStatus = document.getElementById('loadingStatus');
    const messageBox = document.getElementById('messageBox');
    const statsBar = document.getElementById('statsBar');
    const resultsCount = document.getElementById('resultsCount');
    const activeApiUrl = document.getElementById('activeApiUrl');
    const rawApiLink = document.getElementById('rawApiLink');

    function buildApiUrl() {
        const url = new URL('/api/manhwa/', window.location.origin);

        if (filterStatus.value !== 'all') {
            url.searchParams.set('status', filterStatus.value);
        }
        if (filterReading.value !== 'all') {
            url.searchParams.set('reading_status', filterReading.value);
        }
        if (filterGenre.value !== 'all') {
            url.searchParams.set('genre', filterGenre.value);
        }
        if (sortOrder.value && sortOrder.value !== '-rating') {
            url.searchParams.set('sort', sortOrder.value);
        }
        if (limitResults.value !== 'all') {
            url.searchParams.set('limit', limitResults.value);
        }

        return url;
    }

    function updateUrlDisplay() {
        const targetUrl = buildApiUrl();
        const displayPath = targetUrl.pathname + targetUrl.search;
        activeApiUrl.textContent = displayPath;
        rawApiLink.href = displayPath;
        rawApiLink.textContent = `Endpoint JSON (${displayPath})`;
    }

    async function loadManhwaData() {
        const apiUrl = buildApiUrl();
        updateUrlDisplay();

        loadingStatus.style.display = 'flex';
        messageBox.style.display = 'none';
        messageBox.className = 'status-box';
        statsBar.style.display = 'none';
        manhwaContainer.replaceChildren();

        try {
            const response = await fetch(apiUrl.toString(), {
                method: 'GET',
                headers: {
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`Błąd HTTP: ${response.status}`);
            }

            const data = await response.json();
            const items = data.items || [];

            if (items.length === 0) {
                showEmptyState();
                return;
            }

            renderManhwaCards(items);
            statsBar.style.display = 'flex';
            resultsCount.textContent = `Wyświetlono pozycji: ${items.length}`;
        } catch (error) {
            showErrorState(error.message);
        } finally {
            loadingStatus.style.display = 'none';
        }
    }

    function renderManhwaCards(items) {
        manhwaContainer.replaceChildren();

        items.forEach(item => {
            const card = document.createElement('article');
            card.className = 'manhwa-card';

            const topDiv = document.createElement('div');
            topDiv.className = 'card-top';

            const tagsDiv = document.createElement('div');
            tagsDiv.className = 'card-tags';

            const genreTag = document.createElement('span');
            genreTag.className = 'tag tag-genre';
            genreTag.textContent = item.genre || 'Inny';
            tagsDiv.appendChild(genreTag);

            if (item.publisher) {
                const pubTag = document.createElement('span');
                pubTag.className = 'tag tag-publisher';
                pubTag.textContent = item.publisher;
                tagsDiv.appendChild(pubTag);
            }

            const statusTag = document.createElement('span');
            if (item.is_completed) {
                statusTag.className = 'tag tag-completed';
                statusTag.textContent = 'Zakończona';
            } else {
                statusTag.className = 'tag tag-ongoing';
                statusTag.textContent = 'W trakcie';
            }
            tagsDiv.appendChild(statusTag);

            if (item.reading_status_display) {
                const readTag = document.createElement('span');
                readTag.className = 'tag tag-reading';
                readTag.textContent = item.reading_status_display;
                tagsDiv.appendChild(readTag);
            }

            topDiv.appendChild(tagsDiv);

            const titleEl = document.createElement('h3');
            titleEl.className = 'card-title';
            titleEl.textContent = item.title;
            topDiv.appendChild(titleEl);

            const authorEl = document.createElement('p');
            authorEl.className = 'card-author';
            authorEl.textContent = `Autor: ${item.author || 'Nieznany'}`;
            topDiv.appendChild(authorEl);

            card.appendChild(topDiv);

            const descEl = document.createElement('p');
            descEl.className = 'card-desc';
            descEl.textContent = item.description || '';
            card.appendChild(descEl);

            if (item.notes) {
                const notesEl = document.createElement('p');
                notesEl.className = 'card-notes';
                notesEl.textContent = `Notatka: ${item.notes}`;
                card.appendChild(notesEl);
            }

            const footerDiv = document.createElement('div');
            footerDiv.className = 'card-footer';

            const ratingDiv = document.createElement('div');
            ratingDiv.className = 'card-rating';
            ratingDiv.textContent = `Ocena: ${item.rating}/10`;
            footerDiv.appendChild(ratingDiv);

            const chaptersDiv = document.createElement('div');
            chaptersDiv.className = 'card-chapters';
            chaptersDiv.textContent = `${item.chapters_count} rozdz.`;
            footerDiv.appendChild(chaptersDiv);

            card.appendChild(footerDiv);
            manhwaContainer.appendChild(card);
        });
    }

    function showEmptyState() {
        messageBox.className = 'status-box empty-box';
        messageBox.style.display = 'flex';
        messageBox.textContent = 'Brak rekordów spełniających wybrane kryteria.';
    }

    function showErrorState(errorMessage) {
        messageBox.className = 'status-box error-box';
        messageBox.style.display = 'flex';
        messageBox.textContent = `Błąd podczas pobierania danych: ${errorMessage}`;
    }

    function resetFilters() {
        filterStatus.value = 'all';
        filterReading.value = 'all';
        filterGenre.value = 'all';
        sortOrder.value = '-rating';
        limitResults.value = 'all';
        updateUrlDisplay();
        loadManhwaData();
    }

    loadBtn.addEventListener('click', loadManhwaData);
    clearBtn.addEventListener('click', resetFilters);
    [filterStatus, filterReading, filterGenre, sortOrder, limitResults].forEach(el => {
        el.addEventListener('change', () => {
            updateUrlDisplay();
            loadManhwaData();
        });
    });

    updateUrlDisplay();
    loadManhwaData();
});
