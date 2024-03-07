
function getReferralCode() {
    let refCode = document.getElementById("ref_code").placeholder;
    navigator.clipboard.writeText(refCode)
        .catch(err => {
            console.error('Не удалось скопировать текст: ', err);
        });
    
}


document.addEventListener('DOMContentLoaded', function() {
    let refCodeButton = document.getElementById('button-addon1');
    refCodeButton.addEventListener('click', getReferralCode());
})