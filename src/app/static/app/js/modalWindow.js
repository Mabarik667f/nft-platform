let modal = document.getElementById('myModal');

document.addEventListener("DOMContentLoaded", function() {
    let modalButtons = document.querySelectorAll("[data-bs-toggle='modal']");

    modalButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            let myModal = new bootstrap.Modal(document.getElementById('myModal'), {});
            const modal = document.getElementById('myModal');
            modal.querySelector("#nft-name").textContent = button.getAttribute("data-nft-name");
            modal.querySelector("#nft-describe").textContent = button.getAttribute("data-nft-describe");
            modal.querySelector("#nft-pathToImage").textContent = button.getAttribute("data-nft-path-to-image");
            modal.querySelector("#nft-price").textContent = button.getAttribute("data-nft-price");
            modal.querySelector("#nft-amount").textContent = button.getAttribute("data-nft-amount");
            modal.querySelector("#nft-createDate").textContent = button.getAttribute("data-nft-create-date");
            modal.querySelector("#nft-sell-or-buy").href = `/nft-sell/${button.getAttribute("data-nft-id")}/`
            // modal.querySelector("#nft-onSale").textContent = button.getAttribute("data-nft-on-sale");

            myModal.show();
        });
    });
    let closeButton = document.querySelector(".modal .btn-close");
    closeButton.addEventListener("click", function() {
        let myModal = new bootstrap.Modal(document.getElementById('myModal'), {});
        myModal.hide();

        document.body.classList.remove('modal-open');
        modal.classList.remove('show');
        let modalBackdrop = document.querySelector('.modal-backdrop');
        modalBackdrop.parentNode.removeChild(modalBackdrop);
    });

})