document.getElementById('bookingForm').onsubmit = function(e) {
    e.preventDefault();

    let slotId = document.querySelector('input[name="slot_id"]').value;
    let userId = document.querySelector('input[name="user_id"]').value;

    fetch('/book_slot/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
        },
        body: JSON.stringify({
            slot_id: slotId,
            user_id: userId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ошибка при создании записи');
    });
};
