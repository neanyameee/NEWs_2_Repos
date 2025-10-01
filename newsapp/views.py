from django.shortcuts import render, redirect
from django.utils import translation
from django.utils.translation import gettext as _
from .forms import NewsPreferencesForm
import json
from datetime import datetime

NEWS_DATA = {
    'ru': {
        'politics': [
            {'id': 1, 'title': 'Важные политические изменения', 'content': 'Описание политических событий...',
             'date': '2025-09-15'},
            {'id': 2, 'title': 'Международные переговоры', 'content': 'Подробности международных соглашений...',
             'date': '2025-09-19'},
        ],
        'technology': [
            {'id': 3, 'title': 'Новый технологический прорыв', 'content': 'Инновации в сфере технологий...',
             'date': '2025-09-18'},
            {'id': 4, 'title': 'Запуск нового продукта', 'content': 'Представление нового гаджета...',
             'date': '2025-09-18'},
        ],
        'sports': [
            {'id': 5, 'title': 'Результаты спортивных соревнований', 'content': 'Итоги последних матчей...',
             'date': '2025-09-22'},
            {'id': 6, 'title': 'Подготовка к чемпионату', 'content': 'Новости о предстоящих событиях...',
             'date': '2025-09-22'},
        ],
        'entertainment': [
            {'id': 7, 'title': 'Премьеры фильмов', 'content': 'Обзор новых кинопремьер...', 'date': '2025-09-23'},
            {'id': 8, 'title': 'Концерты и мероприятия', 'content': 'Анонсы культурных событий...',
             'date': '2025-09-24'},
        ],
        'science': [
            {'id': 9, 'title': 'Научные открытия', 'content': 'Последние исследования ученых...', 'date': '2025-09-24'},
            {'id': 10, 'title': 'Космические миссии', 'content': 'Новости космонавтики...', 'date': '2025-09-24'},
        ]
    },
    'en': {
        'politics': [
            {'id': 1, 'title': 'Important Political Changes', 'content': 'Description of political events...',
             'date': '2025-09-15'},
            {'id': 2, 'title': 'International Negotiations', 'content': 'Details of international agreements...',
             'date': '2025-09-19'},
        ],
        'technology': [
            {'id': 3, 'title': 'New Technological Breakthrough', 'content': 'Innovations in technology...',
             'date': '2025-09-15'},
            {'id': 4, 'title': 'New Product Launch', 'content': 'Presentation of new gadget...', 'date': '2025-09-18'},
        ],
        'sports': [
            {'id': 5, 'title': 'Sports Competition Results', 'content': 'Results of recent matches...',
             'date': '2025-09-22'},
            {'id': 6, 'title': 'Championship Preparation', 'content': 'News about upcoming events...',
             'date': '2025-09-22'},
        ],
        'entertainment': [
            {'id': 7, 'title': 'Movie Premieres', 'content': 'Review of new film releases...', 'date': '2025-09-23'},
            {'id': 8, 'title': 'Concerts and Events', 'content': 'Announcements of cultural events...',
             'date': '2025-09-24'},
        ],
        'science': [
            {'id': 9, 'title': 'Scientific Discoveries', 'content': 'Latest research from scientists...',
             'date': '2025-09-24'},
            {'id': 10, 'title': 'Space Missions', 'content': 'Space exploration news...', 'date': '2025-09-24'},
        ]
    }
}


def get_user_preferences(request):
    preferences = {
        'categories': request.COOKIES.get('news_categories', '["technology", "science"]'),
        'theme': request.COOKIES.get('theme', 'light'),
        'language': request.COOKIES.get('language', 'ru'),
        'email_notifications': request.COOKIES.get('email_notifications', 'false'),
        'news_per_page': request.COOKIES.get('news_per_page', '10'),
    }
    print(preferences)
    try:
        preferences['categories'] = json.loads(preferences['categories'])
    except:
        preferences['categories'] = ['technology', 'science']
    print(preferences)

    return preferences


def update_visit_history(request, page_name):
    history = request.COOKIES.get('visit_history', '[]')
    try:
        history_list = json.loads(history)
    except:
        history_list = []

    current_visit = {
        'page': page_name,
        'timestamp': datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
        'url': request.path
    }

    history_list.insert(0, current_visit)
    history_list = history_list[:5]

    return history_list


def index(request):
    preferences = get_user_preferences(request)
    visit_history = update_visit_history(request, _('Главная страница'))

    language = preferences['language']
    translation.activate(language)

    filtered_news = []

    for category in preferences['categories']:
        if category in NEWS_DATA.get(language, {}):
            filtered_news.extend(NEWS_DATA[language][category])

    filtered_news.sort(key=lambda x: x['date'], reverse=True)

    response = render(request, 'newsapp/index.html', {
        'news': filtered_news,
        'preferences': preferences,
        'visit_history': visit_history,
    })

    response.set_cookie('visit_history', json.dumps(visit_history), max_age=30 * 24 * 60 * 60)
    response.set_cookie('theme', preferences['theme'], max_age=30 * 24 * 60 * 60)
    response.set_cookie('language', preferences['language'], max_age=30 * 24 * 60 * 60)

    response.set_cookie('django_language', language)

    return response


def preferences(request):
    preferences = get_user_preferences(request)
    visit_history = update_visit_history(request, _('Настройки'))

    if request.method == 'POST':
        form = NewsPreferencesForm(request.POST)
        if form.is_valid():
            response = redirect('index')

            categories = json.dumps(form.cleaned_data['categories'])
            response.set_cookie('news_categories', categories, max_age=30 * 24 * 60 * 60)
            response.set_cookie('theme', form.cleaned_data['theme'], max_age=30 * 24 * 60 * 60)
            response.set_cookie('language', form.cleaned_data['language'], max_age=30 * 24 * 60 * 60)
            response.set_cookie('email_notifications',
                                str(form.cleaned_data['email_notifications']).lower(),
                                max_age=30 * 24 * 60 * 60)
            response.set_cookie('news_per_page',
                                str(form.cleaned_data['news_per_page']),
                                max_age=30 * 24 * 60 * 60)

            response.set_cookie('visit_history', json.dumps(visit_history), max_age=30 * 24 * 60 * 60)

            return response
    else:
        form = NewsPreferencesForm(initial={
            'categories': preferences['categories'],
            'theme': preferences['theme'],
            'language': preferences['language'],
            'email_notifications': preferences['email_notifications'] == 'true',
            'news_per_page': int(preferences['news_per_page']),
        })

    response = render(request, 'newsapp/preferences.html', {
        'form': form,
        'preferences': preferences,
        'visit_history': visit_history,
    })

    response.set_cookie('visit_history', json.dumps(visit_history), max_age=30 * 24 * 60 * 60)
    return response


def set_theme(request, theme):
    response = redirect(request.META.get('HTTP_REFERER', 'index'))
    response.set_cookie('theme', theme, max_age=30 * 24 * 60 * 60)
    return response


def set_language(request, language):
    response = redirect(request.META.get('HTTP_REFERER', 'index'))
    response.set_cookie('language', language, max_age=30 * 24 * 60 * 60)
    return response