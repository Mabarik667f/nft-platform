from django.urls import path
from .views import *

urlpatterns = [
    path('', MainView.as_view(), name='home'),

    path('nft-market/', NFTMarketView.as_view(), name='nft-market'),
    path('nft-details/', NFTDetailsView.as_view(), name='nft-details'),

    path('auctions/', AuctionsView.as_view(), name='auctions'),
    path('auction-details/', AuctionDetailsView.as_view(), name='auction-details'),

    path('show-nft/', ShowNFTView.as_view(), name='show-nft'),
    path('show-collections/', ShowCollectionsView.as_view(), name='show-collections'),
]