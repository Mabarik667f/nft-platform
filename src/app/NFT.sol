// SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.20;

import {ERC20} from "../ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";

contract Token is ERC20 {
    address initialOwner;
    uint constant _initial_supply = 100 * (10 ** 18);

    constructor() ERC20("Professional", "PROFI") {
        _mint(msg.sender, _initial_supply);
        initialOwner = msg.sender;
    }

    function approveAuction(address _owner, address _auctionContract, uint256 _amount) public onlyOwner(_owner){
        _approve(initialOwner, _auctionContract, _amount);
    }

    function approveUserOnAuction(address from, address to, uint256 amount) public {
        _approve(from, to, amount);
    }

    modifier onlyOwner(address _owner) {
        require(_owner == initialOwner, "not an Owner!");
        _;
    }
}

contract MyToken is ERC1155{

    address initialOwner;

    constructor(address _initialOwner) ERC1155("") {
        initialOwner = _initialOwner;
    }

    function mint(address _owner, uint256 id, uint256 amount)
        public onlyOwner(_owner)

    {
        _mint(initialOwner, id, amount, "");
    }

    function mintBatch(address _owner, address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data)
        public onlyOwner(_owner)

    {
        _mintBatch(to, ids, amounts, data);
    }

    function approvalForAllAuction(address owner, address operator, bool approved) public{
        _setApprovalForAll(owner, operator, approved);
    }

    modifier onlyOwner(address _owner) {
        require(_owner == initialOwner, "not an Owner!");
        _;
    }

}

contract Auction{

    address public owner;
    address public auctionContract;

    Token public token;
    MyToken public nft;

    struct Auctions {
        uint collectionId;
        uint startTime;
        uint endTime;
        uint startPrice;
        uint currentPrice;
        uint maxPrice;
        address futureOwner;
        bool status;
    }

    struct NFTData {
        string name;
        string describe;
        string pathToImage;
        uint createDate;
        uint amount;
        uint collectionId;
    }

    struct NFTOnOwner {
        address account;
        uint nftId;
        uint amount;
        bool onSale;
        uint price;
        uint objectId;
    }


    struct NFTCollection {
        string name;
        string describe;
        uint[] nftIds;
        address owner;
    }

    struct Users {
        address account;
        uint tokenBalance;
        bytes32 referralCode;
        uint discount;
        bool isActivatedCode;

    }

    mapping(address account => uint256[] nftId) public nftIdsOnOwner; // получение списка nftId NFTOnOwner
    mapping(address account => uint256[] collectionId) public collectionsOnOwner; // добавить uint[]
    mapping(address account => mapping(uint nftId => NFTOnOwner)) public objectsNFTOnOwner; // получаем данные о количестве nft у определенного аккаунта

    mapping(address account => Users) public users;
    mapping(uint256 collectionId => NFTCollection) public allCollections;
    mapping(uint256 nftId => NFTData) public allNFT;
    mapping(uint auctionId => Auctions) public allAuctions;
    mapping(uint256 nftId => NFTOnOwner) public nftForSale;


    uint[] public nftData; // NFTOnOwner
    uint[] public nftCollection;
    uint[] public auctions;

    // создание пользователей в контакте
    constructor(Token _token, MyToken _nft) {
        token = _token;
        nft = _nft;
        owner = msg.sender;
        auctionContract = address(this);
        createUser(owner, 10000000000000000000);

        createNFT(unicode"Герда в профиль", unicode"Скучающая хаски по имени Герда", "husky_nft1.png", 2000, 7, 0);
        createNFT(unicode"Герда на фрилансе", unicode"Герда релизнула новый проект", "husky_nft2.png", 5000, 5, 0);
        createNFT(unicode"Новогодняя Герда", unicode"Герда ждет боя курантов", "husky_nft3.png", 3500, 2, 0);
        createNFT(unicode"Герда в отпуске", unicode"Приехала отдохнуть после тяжелого проекта", "husky_nft4.png", 4000, 6, 0);
        // createNFT(unicode"Герда в профиль", unicode"Скучающая хаски по имени Герда", "husky_nft1.png", 2000, 7, 0);
        // createNFT(unicode"Герда на фрилансе", unicode"Герда релизнула новый проект", "husky_nft2.png", 5000, 5, 0);
        // createNFT(unicode"Новогодняя Герда", unicode"Герда ждет боя курантов", "husky_nft3.png", 3500, 2, 0);
        // createNFT(unicode"Герда в отпуске", unicode"Приехала отдохнуть после тяжелого проекта", "husky_nft4.png", 4000, 6, 0);

    }

    modifier onlyOwner() {
        require(msg.sender == owner, "not an owner!");
        _;
    }

    function checkTokenBalance() public view returns (uint256) {
        return token.balanceOf(msg.sender);
    }

    function getNFTIdsOnOwner() public view returns(uint[] memory){
        return nftIdsOnOwner[msg.sender];

    }

    function getAllCollectionsOnOwner() public view returns(uint[] memory) {
        return collectionsOnOwner[msg.sender];
    }

    function getAllNFTIds(uint collectionId) public view returns(uint[] memory) {
        return allCollections[collectionId].nftIds;
    }

    function createNFT(string memory name, string memory describe, string memory pathToImage, uint price, uint amount, uint collectionId)
        public onlyOwner
    {
        require(token.balanceOf(owner) >= price, "not enough tokens!");
        nft.mint(owner, nftData.length, amount);
        NFTOnOwner memory nftOnOwner = NFTOnOwner(owner, nftData.length, amount, false, price, nftData.length);
        nftData.push(nftData.length); // у владельца
        allNFT[nftData.length - 1] = NFTData(name, describe, pathToImage, block.timestamp, amount, collectionId); // все nft
        nftIdsOnOwner[owner].push(nftData.length - 1); // у владельца
        objectsNFTOnOwner[owner][nftData.length - 1] = nftOnOwner; // у владельца

        if (collectionId != 0) {
            NFTCollection storage collection = allCollections[collectionId];
            collection.nftIds.push(nftData.length - 1);
            allCollections[collectionId] = collection;
        }

    }

    function cretateNFTCollection(string memory name, string memory describe) public onlyOwner {
        if (nftCollection.length == 0) {
            nftCollection.push(0);
        }
        nftCollection.push(nftCollection.length);
        allCollections[nftCollection.length - 1] = NFTCollection(name, describe, new uint[](0), owner);
        collectionsOnOwner[owner].push(nftCollection.length - 1);

    }


    function sellNFT(uint nftId, uint amount, uint price) public{
        NFTOnOwner memory object = objectsNFTOnOwner[msg.sender][nftId];
        if (object.amount > amount) {
            NFTOnOwner memory sellNFTObject = NFTOnOwner(msg.sender, object.nftId, amount, true, price, nftData.length);
            nftForSale[nftData.length] = sellNFTObject;
            objectsNFTOnOwner[msg.sender][nftId].amount -= amount;

        } else {
            object.onSale = true;
            nftForSale[nftData.length] = object;
            for (uint i; i < nftIdsOnOwner[msg.sender].length; i++) {
                if (nftIdsOnOwner[msg.sender][i] == nftId) {
                    _removeElement(i, false);
                    break;
                }
            }

            delete objectsNFTOnOwner[msg.sender][nftId];
        }
        nftData.push(nftData.length);
        nft.approvalForAllAuction(msg.sender, auctionContract, true);
    }

    function buyNFT(uint nftId) public{
        NFTOnOwner memory curNFT = nftForSale[nftId];
        // require(curNFT.account != msg.sender, "impossible to buy locally!");
        require(token.balanceOf(msg.sender) >= curNFT.price, "not enough tokens!");
        NFTOnOwner memory obj = NFTOnOwner(msg.sender, curNFT.nftId, curNFT.amount, false, curNFT.price, curNFT.objectId);
        nftIdsOnOwner[msg.sender].push(curNFT.objectId);
        objectsNFTOnOwner[msg.sender][nftId] = obj;

        nft.safeTransferFrom(curNFT.account, msg.sender, nftId, curNFT.amount, "");
        token.approveUserOnAuction(msg.sender, auctionContract, curNFT.price);
        token.transferFrom(msg.sender, curNFT.account, curNFT.price);
        users[msg.sender].tokenBalance -= curNFT.price;
        delete nftForSale[nftId];

    }
    // аукцион

    function startAuction(uint endTime, uint startPrice, uint maxPrice, uint collectionId) public onlyOwner{
        // NFTCollection memory curCollection = allCollections[collectionId];
        // require(curCollection.owner != address(0), "not found collection");
        // require(allCollections[collectionId].nftIds.length >= 1, "collection have zero elements!");
        auctions.push(auctions.length);
        allAuctions[auctions.length - 1] = Auctions(collectionId, block.timestamp, endTime, startPrice, startPrice, maxPrice, msg.sender, true);

    }

    function endAuction(uint auctionId) public{
        // не работает
        if(allAuctions[auctionId].futureOwner != owner) {
            allAuctions[auctionId].status = false;
            uint curCollectionId = allAuctions[auctionId].collectionId;
            address futureOwner = allAuctions[auctionId].futureOwner;
            collectionsOnOwner[futureOwner].push(curCollectionId);

            nft.approvalForAllAuction(owner, auctionContract, true);

            for (uint i = 0; i < collectionsOnOwner[owner].length; i++) {
                if (collectionsOnOwner[owner][i] == curCollectionId) {
                    _removeElement(i, true);
                    break;
                }
            }

            for (uint i = 0; i < nftIdsOnOwner[owner].length; i++) {
                if (allNFT[objectsNFTOnOwner[owner][nftIdsOnOwner[owner][i]].nftId].collectionId == curCollectionId) {
                    _removeElement(i, false);
                    nftIdsOnOwner[futureOwner].push(objectsNFTOnOwner[owner][nftIdsOnOwner[owner][i]].objectId);
                    objectsNFTOnOwner[futureOwner][nftIdsOnOwner[owner][i]].objectId = objectsNFTOnOwner[owner][nftIdsOnOwner[owner][i]].objectId;
                    delete objectsNFTOnOwner[msg.sender][i];
                    // nft.safeTransferFrom(owner, futureOwner, objectsNFTOnOwner[owner][nftIdsOnOwner[owner][i]].objectId, objectsNFTOnOwner[owner][nftIdsOnOwner[owner][i]].amount, "");

                }
            }


        } else {
            allAuctions[auctionId].status = false;
        }

    }

    function bid(uint tokens, uint auctionId) public {
        // require(allAuctions[auctionId].currentPrice < tokens, "incorrect bid!");
        token.approveUserOnAuction(msg.sender, auctionContract, tokens);
        token.transferFrom(msg.sender, owner, tokens);
        users[msg.sender].tokenBalance -= tokens;

        if (allAuctions[auctionId].endTime < block.timestamp) {
            endAuction(auctionId);
        }
        else {
            // require(token.balanceOf(msg.sender) >= tokens, "not enough tokens!");
            uint curBid = tokens;
            allAuctions[auctionId].currentPrice = curBid;
            allAuctions[auctionId].futureOwner = msg.sender;
            if (tokens >= allAuctions[auctionId].maxPrice) {
                curBid = allAuctions[auctionId].maxPrice;
                allAuctions[auctionId].currentPrice = curBid;
                endAuction(auctionId);
            }
        }
    }

    // пользователи
    function createUser(address account, uint balance) public {
        _createUser(account, balance);
    }

    function _createUser(address account, uint balance) internal onlyOwner{
        // проверку на наличие токенов
        require(token.balanceOf(owner) >= balance, "not enough tokens!");
        bytes32 refCode = getReferralCode(account);
        users[account] = Users(account, balance, refCode, 0, false);
        token.approveAuction(owner, auctionContract, balance);
        token.transferFrom(owner, account, balance);

    }

    function getReferralCode(address account) public view returns (bytes32) {
        bytes32 refCode;
        if (users[account].account == address(0)) {
            refCode = _setReferralCode(account);
        } else {
            refCode = users[account].referralCode;
        }
        return refCode;
    }

    function _setReferralCode(address account) internal view returns (bytes32) {

        bytes2 to = bytes2(abi.encodePacked(account));
        bytes memory year = abi.encode("2024");
        bytes memory tokenSymbol = bytes(token.symbol());
        bytes32 hashBytes = keccak256(bytes.concat(tokenSymbol, to, year));
        return hashBytes;
    }

    function activateReferralCode(bytes32 refCode) public{
        require(users[msg.sender].referralCode != refCode, "it's your code!");
        require(users[msg.sender].isActivatedCode == false, "code is activated!");

        users[msg.sender].tokenBalance += 100;
        token.approveAuction(owner, auctionContract, 100);
        token.transferFrom(owner, users[msg.sender].account, 100);
        users[msg.sender].isActivatedCode = true;

        if(users[msg.sender].discount < 3) {
            users[msg.sender].discount += 1;
        }
    }

    function gift(address account, uint nftId) public {
        require(users[account].account != address(0));
        nft.approvalForAllAuction(msg.sender, auctionContract, true);
        nft.safeTransferFrom(msg.sender, account, nftId, objectsNFTOnOwner[msg.sender][nftId].amount, "");
        for (uint i; i < nftIdsOnOwner[msg.sender].length; i++) {
            if (nftIdsOnOwner[msg.sender][i] == nftId) {
               _removeElement(i, false);
               break;
            }
        }

        nftIdsOnOwner[account].push(nftId);
        NFTOnOwner memory object = objectsNFTOnOwner[msg.sender][nftId];
        delete objectsNFTOnOwner[msg.sender][nftId];
        objectsNFTOnOwner[account][nftId] = object;

    }


    function _removeElement(uint256 index, bool isCollection) internal {


        if (isCollection) {
            uint[] storage array = collectionsOnOwner[owner];
                for (uint256 i = index; i < array.length - 1; i++) {
                array[i] = array[i + 1];
            }

            array.pop();
        } else {
            uint[] storage array = nftIdsOnOwner[msg.sender];
                for (uint256 i = index; i < array.length - 1; i++) {
                array[i] = array[i + 1];
            }

            array.pop();
        }
        // Сдвигаем все элементы после удаляемого на одну позицию влево

    }

    receive() external payable {}

    fallback() external payable {}

}