main_menu = [{'url': 'home', 'title': 'Главная'},
             {'url': 'auctions', 'title': 'Аукционы'},
             {'url': 'nft-market', 'title': 'NFT'},
             {'url': 'profile', 'title': 'Профиль'},]

profile_menu = [{'url': 'show-nft', 'title': 'Одиночные NFT'},
                {'url': 'show-collections', 'title': 'Коллекции'},
                {'url': 'gift-nft', 'title': 'Подарить NFT'}]


def get_main_context(request):
    return {'main_menu': main_menu, 'profile_menu': profile_menu}
