window.walletAddress = null;
const connectWallet = document.getElementById('connectWallet');
const walletAddress = document.getElementById('walletAddress');

function checkMetamaskExtension() {
    if(window.ethereum === undefined) {
        walletAddress.innerText = 'расширение MetaMask не установленно';
        return false;
    }
}

async function connectWalletWithMetaMask() {
    const accounts = await window.ethereum.request({method: 'eth_requestAccounts'})
    .catch(error => {
        console.error(error);
        return;
    })
    if (!accounts) {return}

    window.walletAddress = accounts[0];
    walletAddress.innerText = window.walletAddress;

    connectWallet.innerText = 'Sign Out';
    connectWallet.removeEventListener('click', connectWalletWithMetaMask);
    connectWallet.addEventListener('click', signOutMetaMask);
}

async function signOutMetaMask() {
    window.walletAddress = null;
    walletAddress.innerText = '';
    connectWallet.innerText = 'Войти';
    connectWallet.removeEventListener('click', signOutMetaMask);
    connectWallet.addEventListener('click', connectWalletWithMetaMask);
}
document.addEventListener('DOMContentLoaded', function() {

    checkMetamaskExtension();
    connectWallet.addEventListener('click', connectWalletWithMetaMask());
})