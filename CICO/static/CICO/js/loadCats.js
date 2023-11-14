
function loadCats() {
    const userId = document.getElementById('userId').value;  // assuming you have the user's ID stored in a hidden input field
    fetch('/api/cats/get_cats_for_user/', {
    method: 'GET',
    credentials: 'same-origin',
    headers: {
        'X-Requested-With': 'XMLHttpRequest',
    },
})
.then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok :' + response.statusText);
    }
    return response.json();
})
.then(data => {
    console.log(data.cats); // Here's your user-specific cats data
})
.catch((error) => {
    console.error('There has been a problem with your fetch operation:', error);
});
}
