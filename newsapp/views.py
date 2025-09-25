from django.shortcuts import render, redirect
from django.utils import translation
from django.http import HttpResponse
from django.utils.translation import gettext as _
from .forms import NewsPreferencesForm
import json
from datetime import datetime, timedelta

# Mock data for news
NEWS_DATA = {
    'ru': {
        'politics': [
            {'id': 1, 'title': 'Важные политические изменения', 'content': 'Описание политических событий...',
             'date': '2024-01-15'},
            {'id': 2, 'title': 'Международные переговоры', 'content': 'Подробности международных соглашений...',
             'date': '2024-01-14'},
        ],
        'technology': [
            {'id': 3, 'title': 'Новый технологический прорыв', 'content': 'Инновации в сфере технологий...',
             'date': '2024-01-15'},
            {'id': 4, 'title': 'Запуск нового продукта', 'content': 'Представление нового гаджета...',
             'date': '2024-01-13'},
        ],
        'sports': [
            {'id': 5, 'title': 'Результаты спортивных соревнований', 'content': 'Итоги последних матчей...',
             'date': '2024-01-15'},
            {'id': 6, 'title': 'Подготовка к чемпионату', 'content': 'Новости о предстоящих событиях...',
             'date': '2024-01-12'},
        ],
        'entertainment': [
            {'id': 7, 'title': 'Премьеры фильмов', 'content': 'Обзор новых кинопремьер...', 'date': '2024-01-14'},
            {'id': 8, 'title': 'Концерты и мероприятия', 'content': 'Анонсы культурных событий...',
             'date': '2024-01-11'},
        ],
        'science': [
            {'id': 9, 'title': 'Научные открытия', 'content': 'Последние исследования ученых...', 'date': '2024-01-15'},
            {'id': 10, 'title': 'Космические миссии', 'content': 'Новости космонавтики...', 'date': '2024-01-10'},
        ]
    },
    'en': {
        'politics': [
            {'id': 1, 'title': 'Important Political Changes', 'content': 'Description of political events...',
             'date': '2024-01-15'},
            {'id': 2, 'title': 'International Negotiations', 'content': 'Details of international agreements...',
             'date': '2024-01-14'},
        ],
        'technology': [
            {'id': 3, 'title': 'New Technological Breakthrough', 'content': 'Innovations in technology...',
             'date': '2024-01-15'},
            {'id': 4, 'title': 'New Product Launch', 'content': 'Presentation of new gadget...', 'date': '2024-01-13'},
        ],
        'sports': [
            {'id': 5, 'title': 'Sports Competition Results', 'content': 'Results of recent matches...',
             'date': '2024-01-15'},
            {'id': 6, 'title': 'Championship Preparation', 'content': 'News about upcoming events...',
             'date': '2024-01-12'},
        ],
        'entertainment': [
            {'id': 7, 'title': 'Movie Premieres', 'content': 'Review of new film releases...', 'date': '2024-01-14'},
            {'id': 8, 'title': 'Concerts and Events', 'content': 'Announcements of cultural events...',
             'date': '2024-01-11'},
        ],
        'science': [
            {'id': 9, 'title': 'Scientific Discoveries', 'content': 'Latest research from scientists...',
             'date': '2024-01-15'},
            {'id': 10, 'title': 'Space Missions', 'content': 'Space exploration news...', 'date': '2024-01-10'},
        ]
    }
}


def get_user_preferences(request):
    """Get user preferences from cookies"""
    preferences = {
        'categories': request.COOKIES.get('news_categories', '["technology", "science"]'),
        'theme': request.COOKIES.get('theme', 'light'),
        'language': request.COOKIES.get('language', 'ru'),
        'email_notifications': request.COOKIES.get('email_notifications', 'false'),
        'news_per_page': request.COOKIES.get('news_per_page', '10'),
    }

    # Parse JSON categories
    try:
        preferences['categories'] = json.loads(preferences['categories'])
    except:
        preferences['categories'] = ['technology', 'science']

    return preferences


def update_visit_history(request, page_name):
    """Update visit history cookie"""
    history = request.COOKIES.get('visit_history', '[]')
    try:
        history_list = json.loads(history)
    except:
        history_list = []

    # Add current page with timestamp
    current_visit = {
        'page': page_name,
        'timestamp': datetime.now().isoformat(),
        'url': request.path
    }

    # Keep only last 5 visits
    history_list.insert(0, current_visit)
    history_list = history_list[:5]

    return history_list


def index(request):
    """Main news page"""
    preferences = get_user_preferences(request)
    visit_history = update_visit_history(request, _('Главная страница'))

    # Set language
    translation.activate(preferences['language'])
    request.session['_language'] = preferences['language']

    # Filter news based on user preferences
    filtered_news = []
    language = preferences['language']

    for category in preferences['categories']:
        if category in NEWS_DATA.get(language, {}):
            filtered_news.extend(NEWS_DATA[language][category])

    # Sort by date
    filtered_news.sort(key=lambda x: x['date'], reverse=True)

    response = render(request, 'newsapp/index.html', {  # Изменен путь
        'news': filtered_news,
        'preferences': preferences,
        'visit_history': visit_history,
    })

    # Set cookies
    response.set_cookie('visit_history', json.dumps(visit_history), max_age=30 * 24 * 60 * 60)
    response.set_cookie('theme', preferences['theme'], max_age=30 * 24 * 60 * 60)
    response.set_cookie('language', preferences['language'], max_age=30 * 24 * 60 * 60)

    return response


def preferences(request):
    """News preferences page"""
    preferences = get_user_preferences(request)
    visit_history = update_visit_history(request, _('Настройки'))

    if request.method == 'POST':
        form = NewsPreferencesForm(request.POST)
        if form.is_valid():
            # Save preferences to cookies
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

            # Update visit history cookie
            response.set_cookie('visit_history', json.dumps(visit_history), max_age=30 * 24 * 60 * 60)

            return response
    else:
        # Prepopulate form with current preferences
        form = NewsPreferencesForm(initial={
            'categories': preferences['categories'],
            'theme': preferences['theme'],
            'language': preferences['language'],
            'email_notifications': preferences['email_notifications'] == 'true',
            'news_per_page': int(preferences['news_per_page']),
        })

    response = render(request, 'newsapp/preferences.html', {  # Изменен путь
        'form': form,
        'preferences': preferences,
        'visit_history': visit_history,
    })

    response.set_cookie('visit_history', json.dumps(visit_history), max_age=30 * 24 * 60 * 60)
    return response


def set_theme(request, theme):
    """Quick theme switcher"""
    response = redirect(request.META.get('HTTP_REFERER', 'index'))
    response.set_cookie('theme', theme, max_age=30 * 24 * 60 * 60)
    return response


def set_language(request, language):
    """Quick language switcher"""
    response = redirect(request.META.get('HTTP_REFERER', 'index'))
    response.set_cookie('language', language, max_age=30 * 24 * 60 * 60)
    return response