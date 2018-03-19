from django import forms
from django.conf import settings

import requests


class DictionaryForm(forms.Form):
    word = forms.CharField(max_length=100)

    def search(self):
        result = {}
        word = self.cleaned_data['word']
        url = f'https://od-api.oxforddictionaries.com/api/v1/entries/en/{word}'
        headers = {
            'app_id': settings.OXFORD_APP_ID,
            'app_key': settings.OXFORD_APP_KEY
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            result = response.json()
            result['success'] = True
        else:
            result['success'] = False

            if response.status_code == 404:
                result['message'] = f'No entry found for {word}'
            else:
                result['message'] = 'The Oxford API is not available at the moment. Please try again later.'

        return result
