connected = false;
walletAddress = null;

function checkMetamaskExtension() {
    if(window.ethereum === undefined) {
        return false;
    } 
    
}

async function checkLoginMematask() {
    if (!window.walletAddress) {
        let address = await connectWalletWithMetaMask();
        fetch(`/set-session/${address}`)
        .catch(error => {
            console.log(error);
        })
    } 
}

function initMetamask() {
    checkMetamaskExtension();
    checkLoginMematask()
}

async function connectWalletWithMetaMask() {
    try {
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
        if (accounts.length > 0) {
            window.walletAddress = accounts[0];
            connected = true;
            return accounts[0];
        } else {
            connected = false;
            console.error('No accounts found');
        }
    } catch (error) {
        console.error(error);
    }
}


document.addEventListener('DOMContentLoaded', function() {
    initMetamask();
});

window.ethereum.on('accountsChanged', async() => {
    initMetamask();
});