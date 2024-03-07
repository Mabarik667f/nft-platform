from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic.edit import FormMixin

from .contract_functions import ContractMethods
from .forms import CreateNFTForm, CreateCollectionForm, StartAuctionForm, BidAuctionForm, \
    ActivateReferralCodeForm, SellNFTForm

'''
Много копирования, можно создать миксины и вынести логику, но
в данном проекте это не имеет смысла
'''


class MainView(View):
    template_name = 'app/index.html'

    def get(self, request):
        return render(request, self.template_name)


class NFTMarketView(View):
    """Все nft на продаже"""
    template_name = 'app/nft.html'

    def get(self, request):
        context = {'nft_items': None}
        address = request.session.get('address', None)
        if address is not None:
            nft_items = ContractMethods(address).get_all_nft()
            context['nft_items'] = nft_items
        return render(request, template_name=self.template_name, context=context)


class AuctionsView(View):
    """Все активные аукционы"""
    template_name = 'app/auctions.html'

    def get(self, request):
        context = {'auction_items': None}
        address = request.session.get('address', None)
        if address is not None:
            auction_items = ContractMethods(address).get_all_auctions()
            context['auction_items'] = auction_items
        return render(request, template_name=self.template_name, context=context)


class NFTSellView(FormMixin, View):
    """Продажа nft"""
    form_class = SellNFTForm
    success_url = 'profile'
    template_name = 'app/sell.html'

    def get(self, request, nft_id):
        form = SellNFTForm()
        context = {'form': form,
                   'nft': None}
        address = request.session.get('address', None)
        if address is not None:
            nft = ContractMethods(address).get_single_nft(nft_id)
            context['nft'] = nft
        return render(request, self.template_name, context=context)

    def post(self, request, nft_id):
        form = SellNFTForm(request.POST)
        address = request.session.get('address', None)
        if form.is_valid() and address is not None:
            ContractMethods(address).sell_nft(form, nft_id)
            return redirect(self.success_url)
        return render(request, self.template_name, context={'form': form})


class NFTBuyView(FormMixin, View):
    """Покупка nft"""

    template_name = 'app/nft.html'
    success_url = 'profile'

    def get(self, request, nft_id):
        address = request.session.get('address', None)
        if address is not None:
            ContractMethods(address).buy_nft(nft_id)
            return redirect(self.success_url)
        return render(request, self.template_name)


class AuctionDetailsView(FormMixin, View):
    """Описание аукциона"""
    template_name = 'app/auction-details.html'
    success_url = 'profile'
    form_class = BidAuctionForm

    def get(self, request, auction_id):
        form = BidAuctionForm()
        context = {'form': form}
        address = request.session.get('address', None)
        context['auction'] = ContractMethods(address).get_auction_data(auction_id)
        return render(request, self.template_name, context)

    def post(self, request, auction_id):
        form = BidAuctionForm(request.POST)
        address = request.session.get('address', None)
        if form.is_valid() and address is not None:
            ContractMethods(address).bid_auction(form, auction_id)
            return redirect(self.success_url)
        return render(request, self.template_name, context={'form': form})


class ShowNFTView(View):
    """Просмотр NFT"""
    template_name = 'app/show-nft.html'

    def get(self, request):
        context = {'nft_items': None}
        address = request.session.get('address', None)
        if address is not None:
            nft_items = ContractMethods(address).get_all_nft_on_owner()
            print(nft_items)
            context['nft_items'] = nft_items
        return render(request, template_name=self.template_name, context=context)


class ShowCollectionsView(View):
    """Просмотр коллекций"""
    template_name = 'app/show-collections.html'

    def get(self, request):
        context = {'nft_collections': None}
        address = request.session.get('address')
        if address is not None:

            nft_collections = ContractMethods(address).get_collections()
            context['nft_collections'] = nft_collections

        return render(request, template_name=self.template_name, context=context)


class CreateNFTView(FormMixin, View):
    """Создание nft"""
    template_name = 'app/create-nft.html'
    form_class = CreateNFTForm
    success_url = 'profile'

    def get(self, request):
        address = request.session.get('address', None)
        if address is not None:
            form = CreateNFTForm(collections=ContractMethods(address).get_collections_for_form())
            return render(request, self.template_name, context={'form': form})
        return render(request, self.template_name)

    def post(self, request):
        address = request.session.get('address', None)
        form = CreateNFTForm(request.POST, request.FILES, collections=ContractMethods(address).get_collections_for_form())
        if form.is_valid():
            ContractMethods(address).create_nft(form)
            return redirect(self.success_url)

        return render(request, self.template_name, context={'form': form})


class CreateCollectionView(FormMixin, View):
    """Создание коллекции"""
    template_name = 'app/create-collection.html'
    form_class = CreateCollectionForm
    success_url = 'profile'

    def get(self, request):
        form = CreateCollectionForm()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = CreateCollectionForm(request.POST)

        address = request.session.get('address', None)
        if form.is_valid() and address is not None:

            ContractMethods(address).create_nft_collection(form)
            return redirect(self.success_url)
        return render(request, self.template_name, context={'form': form})


class StartAuctionView(FormMixin, View):
    """Начало"""
    template_name = 'app/start-auction.html'
    success_url = 'auctions'
    form_class = StartAuctionForm

    def get(self, request):
        address = request.session.get('address', None)
        if address is not None:
            form = StartAuctionForm(collections_choices=ContractMethods(address).get_all_collections())
            return render(request, self.template_name, context={'form': form})
        return render(request, self.template_name)

    def post(self, request):
        address = request.session.get('address', None)
        form = StartAuctionForm(request.POST, collections_choices=ContractMethods(address).get_all_collections())
        if form.is_valid() and address is not None:
            ContractMethods(address).start_auction(form)
            return redirect(self.success_url)
        return render(request, self.template_name, context={'form': form})


class EndAuctionView(View):
    """Окончание"""
    template_name = 'app/auction-details.html'
    success_url = 'profile'

    def get(self, request, auction_id):
        address = request.session.get('address', None)
        if address is not None:
            ContractMethods(address).end_auction(auction_id)
            return redirect(self.success_url)
        return render(request, self.template_name)


class UserProfileView(FormMixin, View):
    template_name = 'app/profile.html'
    form_class = ActivateReferralCodeForm
    success_url = 'profile'

    def get(self, request):
        context = {'token_balance': None}
        address = request.session.get('address', None)
        form = ActivateReferralCodeForm()
        context['form'] = form
        if address is not None:
            token_balance, ref_code = ContractMethods(address).get_user_data()
            context['token_balance'] = token_balance
            context['ref_code'] = ref_code
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        address = request.session.get('address', None)
        context = {'token_balance': None}
        if address is not None:
            form = ActivateReferralCodeForm(request.POST)
            if form.is_valid():
                ContractMethods(address).activate_code(form)
                token_balance, ref_code = ContractMethods(address).get_user_data()
                context['token_balance'] = token_balance
                context['ref_code'] = ref_code
                return redirect(self.success_url)
        return render(request, self.template_name, context=context)


class SetSessionView(View):

    def get(self, request, address):
        adr = request.session.get('address', None)
        if adr is not None and adr != address:
            request.session.delete()
        if request.session.get('address', None) is None:
            request.session['address'] = address
            request.session.create()
        return HttpResponse(status=200)
