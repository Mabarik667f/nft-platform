from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .contract import contract


class MainView(View):
    template_name = 'app/index.html'

    def get(self, request):
        print(contract.functions.nft().call())
        return render(request, self.template_name)


class NFTMarketView(View):
    template_name = 'app/nft.html'


class AuctionsView(View):
    template_name = 'app/auctions.html'


class NFTDetailsView(View):
    template_name = 'app/nft-details.html'


class AuctionDetailsView(View):
    template_name = 'app/auction-details.html'


class ShowNFTView(View):
    template_name = 'app/show-nft.html'


class ShowCollectionsView(View):
    template_name = 'app/show-collections.html'
