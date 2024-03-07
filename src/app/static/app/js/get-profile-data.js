async function getProfileData() {
    let addressDiv = document.getElementById("address");
    let ethBl = document.getElementById("eth-balance");
    const accounts = await window.ethereum.request({method: 'eth_requestAccounts'})
    
    .catch(error => {
        console.error(error);
        return;
    })

    window.addressDiv = accounts[0];
    addressDiv.innerHTML = window.addressDiv;

    const ethBalance = await window.ethereum.request({method: "eth_getBalance",
    params: [
        window.addressDiv,
        "latest"
    ]
    })
    .catch(error => {
        console.error(error);
        return;
    })

    ethBl.innerHTML = parseFloat((ethBalance) / Math.pow(10, 18));
}

getProfileData();