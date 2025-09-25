from django import forms


class NewsPreferencesForm(forms.Form):
    CATEGORY_CHOICES = [
        ('politics', 'Политика'),
        ('technology', 'Технологии'),
        ('sports', 'Спорт'),
        ('entertainment', 'Развлечения'),
        ('science', 'Наука'),
    ]

    THEME_CHOICES = [
        ('light', 'Светлая'),
        ('dark', 'Темная'),
    ]

    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('en', 'English'),
    ]

    categories = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Интересующие категории'
    )

    theme = forms.ChoiceField(
        choices=THEME_CHOICES,
        widget=forms.RadioSelect,
        label='Тема оформления'
    )

    language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        widget=forms.RadioSelect,
        label='Язык интерфейса'
    )

    email_notifications = forms.BooleanField(
        required=False,
        label='Email уведомления'
    )

    news_per_page = forms.IntegerField(
        min_value=5,
        max_value=50,
        initial=10,
        label='Новостей на странице'
    )