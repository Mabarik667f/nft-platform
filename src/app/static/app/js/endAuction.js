let auctionEndButton = document.querySelector('.endAuction');
function endAuction() {
    fetch(`/end-auction/${auctionEndButton.id}/`)
    .catch(error => {
        console.log(error);
    });
}


document.addEventListener('DOMContentLoaded', function() {
    auctionEndButton.addEventListener('click', endAuction());
})