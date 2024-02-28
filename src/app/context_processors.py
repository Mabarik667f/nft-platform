main_menu = [{'url': 'home', 'title': 'Главная'},
             {'url': 'auctions', 'title': 'Аукционы'},
             {'url': 'nft-market', 'title': 'NFT'},
             {'url': 'users:profile', 'title': 'Профиль'},]

profile_menu = [{'url': 'show-nft', 'title': 'Одиночные NFT'},
                 {'url': 'show-collections', 'title': 'Коллекции'}]


def get_main_context(request):
    return {'main_menu': main_menu, 'profile_menu': profile_menu}
