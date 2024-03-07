from .contract import contract
from eth_utils import to_checksum_address
from web3.exceptions import ContractLogicError
from .services import NFT, NFTOnOwner, Collection, Auction, AllNFTData


class ContractMethods:

    def __init__(self, address):
        self.address = to_checksum_address(address)

    def get_user_data(self):
        token_balance = contract.functions.checkTokenBalance().call({"from": self.address})
        ref_code = contract.functions.getReferralCode(self.address).call({"from": self.address})
        return token_balance, ref_code.hex()

    def activate_code(self, form):
        ref_code = form.cleaned_data['ref_code']
        contract.functions.activateReferralCode(ref_code).call({'from': self.address})

    def get_all_nft(self):
        nft_items = []
        try:
            i = 0
            while True:
                nft_id = contract.functions.nftData(i).call({'from': self.address})
                nft_item = NFTOnOwner(contract.functions.nftForSale(nft_id).call({'from': self.address}))
                nft_data = NFT(contract.functions.allNFT(nft_item.nft_id).call({'from': self.address}),
                               nft_item.nft_id, self.address)
                obj = AllNFTData(nft_item, nft_data)

                if obj.nft_on_owner.on_sale:
                    nft_items.append(obj)

                i += 1
        except (ValueError, ContractLogicError):
            return nft_items

    def get_all_collections(self):
        collections_items = []
        try:
            i = 0
            while True:
                col_id = contract.functions.nftCollection(i).call({'from': self.address})
                col = contract.functions.allCollections(col_id).call({'from': self.address})
                obj = Collection(col, collection_id=col_id)
                obj.nft_ids = contract.functions.getAllNFTIds(i).call({'from': self.address})
                if len(obj.nft_ids) >= 1:
                    collections_items.append((obj.col_id, obj.name))
                i += 1
        except (ValueError, ContractLogicError):
            return collections_items

    def get_all_auctions(self):
        auctions_items = []
        try:
            i = 0
            while True:
                auction_id = contract.functions.auctions(i).call({'from': self.address})
                auction_item = contract.functions.allAuctions(auction_id).call({'from': self.address})
                obj = Auction(auction_item, i, self.address)
                if obj.status:
                    auctions_items.append(obj)
                i += 1
        except (ValueError, ContractLogicError):
            return auctions_items

    def sell_nft(self, form, nft_id):
        data = [
            nft_id,
            form.cleaned_data['amount'],
            form.cleaned_data['price']
        ]
        contract.functions.sellNFT(*data).transact({'from': self.address})

    def buy_nft(self, nft_id):
        contract.functions.buyNFT(nft_id).transact({'from': self.address})

    def get_single_nft(self, nft_id):
        nft = contract.functions.objectsNFTOnOwner(self.address, nft_id).call({'from': self.address})
        nft_on_owner = NFTOnOwner(nft)
        nft_data = contract.functions.allNFT(nft_on_owner.nft_id).call({'from': self.address})
        nft_data_obj = NFT(nft_data, nft_on_owner.nft_id, self.address)
        obj = AllNFTData(nft_on_owner, nft_data_obj)

        return obj

    def get_all_nft_on_owner(self):
        nft_ids = contract.functions.getNFTIdsOnOwner().call({'from': self.address})
        nft_items = []
        for i in nft_ids:
            nft_items.append(self.get_single_nft(i))

        return nft_items

    def get_collections(self):
        collections_ids = contract.functions.getAllCollectionsOnOwner().call({'from': self.address})
        collections_items = []
        for collection in collections_ids:
            obj = Collection(collection=contract.functions.allCollections(collection).call({'from': self.address}),
                             collection_id=collection)
            obj.nft_ids = contract.functions.getAllNFTIds(collection).call({'from': self.address})
            collections_items.append(obj)
        return collections_items

    def get_collections_for_form(self):
        collections_ids = contract.functions.getAllCollectionsOnOwner().call({'from': self.address})
        collections_items = []
        for i in collections_ids:
            collection = contract.functions.allCollections(i).call({'from': self.address})
            obj = Collection(collection, collection_id=i)
            collections_items.append((obj.col_id, obj.name))

        return collections_items

    def get_auction_data(self, auction_id):
        auction_item = contract.functions.allAuctions(auction_id).call({'from': self.address})
        obj = Auction(auction_item, auction_id, self.address)
        return obj

    def create_nft(self, form):
        nft_data = [form.cleaned_data['name'],
                    form.cleaned_data['describe'],
                    # form.cleaned_data['path_to_image'],
                    'ABOBA.png',
                    form.cleaned_data['price'],
                    form.cleaned_data['amount'],
                    int(form.cleaned_data['collection'])]
        contract.functions.createNFT(*nft_data).transact({'from': self.address})

    def create_nft_collection(self, form):
        collection_data = [
            form.cleaned_data['name'],
            form.cleaned_data['describe']
        ]
        contract.functions.cretateNFTCollection(*collection_data).transact({'from': self.address})

    def start_auction(self, form):
        data = [
            int(form.cleaned_data['date_end'].timestamp()),
            form.cleaned_data['start_price'],
            form.cleaned_data['max_price'],
            int(form.cleaned_data['collection'])
        ]
        contract.functions.startAuction(*data).transact({'from': self.address})

    def bid_auction(self, form, auction_id):
        data = [form.cleaned_data['bid'],
                auction_id]
        contract.functions.bid(*data).transact({'from': self.address})

    def end_auction(self, auction_id):
        contract.functions.endAuction(auction_id).transact({'from': self.address})
