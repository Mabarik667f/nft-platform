import datetime
from .contract import contract
from eth_utils import to_checksum_address


class NFT:

    def __init__(self, nft, nft_id, address):
        self.address = to_checksum_address(address)
        self.name = nft[0]
        self.describe = nft[1]
        self.path_to_image = nft[2]
        self.createDate = datetime.datetime.fromtimestamp(nft[3])
        self.amount = nft[4]
        self.nft_id = nft_id
        self.collection_id = self.get_collection(nft[5])

    def get_collection(self, collection_id):
        return contract.functions.allCollections(collection_id).call({'from': self.address})


class NFTOnOwner:

    def __init__(self, nft):
        self.account = nft[0]
        self.nft_id = nft[1]
        self.amount = nft[2]
        self.on_sale = nft[3]
        self.price = nft[4]
        self.objectId = nft[5]


class AllNFTData:

    def __init__(self, nft_on_owner: NFTOnOwner, nft_data: NFT):
        self.nft_on_owner = nft_on_owner
        self.nft_data = nft_data

class Collection:

    def __init__(self, collection, collection_id, nft_ids=None):
        self.col_id = collection_id
        self.name = collection[0]
        self.describe = collection[1]
        self.nft_ids = nft_ids
        self.owner = collection[2]


class Auction:

    def __init__(self, auction, auction_id, address):
        self.collection_id = auction[0]
        self.start_date = datetime.datetime.fromtimestamp(auction[1])
        self.end_date = datetime.datetime.fromtimestamp(auction[2])
        self.start_price = auction[3]
        self.current_price = auction[4]
        self.max_price = auction[5]
        self.future_owner = auction[6]
        self.status = auction[7]
        self.auction_id = auction_id
        self.collection = self.get_collection(address, self.collection_id)

    def get_collection(self, address, collection_id):
        return Collection(contract.functions.allCollections(collection_id).call({'from': address}),
                          collection_id=collection_id)

