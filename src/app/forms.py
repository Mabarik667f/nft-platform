import datetime

from django import forms
from django.core.exceptions import ValidationError


class CreateNFTForm(forms.Form):
    name = forms.CharField(label='Название')
    describe = forms.CharField(label='Описание')
    path_to_image = forms.FileField(label='Изображение')
    price = forms.IntegerField(label='Цена за единицу')
    amount = forms.IntegerField(label='Количество')
    collection = forms.ChoiceField(label="Элемент коллекции", choices=[])

    def __init__(self, *args, **kwargs):
        collections = kwargs.pop('collections', None)
        super(CreateNFTForm, self).__init__(*args, **kwargs)
        if collections:
            self.fields['collection'].choices = [('0', 'Нет')] + collections


class CreateCollectionForm(forms.Form):
    name = forms.CharField(label='Название')
    describe = forms.CharField(label='Описание')


class StartAuctionForm(forms.Form):
    date_end = forms.DateTimeField(label='Дата окончания', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    start_price = forms.IntegerField(label='Начальная ставка')
    max_price = forms.IntegerField(label='Максимальная ставка')
    collection = forms.ChoiceField(label='Коллекция', choices=[])

    def __init__(self, *args, **kwargs):
        collections_choices = kwargs.pop('collections_choices', None)
        super(StartAuctionForm, self).__init__(*args, **kwargs)
        if collections_choices:
            self.fields['collection'].choices = collections_choices

    def clean_data_end(self):
        date_end = self.cleaned_data['date_end']
        if date_end < datetime.datetime.now():
            raise ValidationError("Дата окончания должна быть больше или равна текущей дате")
        return date_end


class BidAuctionForm(forms.Form):
    bid = forms.IntegerField(label='Ставка')


class SellNFTForm(forms.Form):
    price = forms.IntegerField(label='Цена')
    amount = forms.IntegerField(label='Количество')


class ActivateReferralCodeForm(forms.Form):
    ref_code = forms.CharField()