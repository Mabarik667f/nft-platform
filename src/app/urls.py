from django.urls import path
from .views import *

urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('gift-nft/', UserProfileView.as_view(), name='gift-nft'),
    path('set-session/<str:address>/', SetSessionView.as_view(), name='set-session'),

    path('nft-market/', NFTMarketView.as_view(), name='nft-market'),

    path('nft-sell/<int:nft_id>/', NFTSellView.as_view(), name='nft-sell'),
    path('nft-buy/<int:nft_id>/', NFTBuyView.as_view(), name='nft-buy'),

    path('auctions/', AuctionsView.as_view(), name='auctions'),
    path('auction-details/<int:auction_id>/', AuctionDetailsView.as_view(), name='auction-details'),

    path('show-nft/', ShowNFTView.as_view(), name='show-nft'),
    path('show-collections/', ShowCollectionsView.as_view(), name='show-collections'),

    path('create-nft/', CreateNFTView.as_view(), name="create-nft"),
    path('create-collection/', CreateCollectionView.as_view(), name='create-collection'),

    path('start-auction/', StartAuctionView.as_view(), name='start-auction'),
    path('end-auction/<int:auction_id>/', EndAuctionView.as_view(), name='end-auction'),

]