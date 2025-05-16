document.addEventListener("DOMContentLoaded", function () {
    const bookButton = document.getElementById("bookButton");

    if (bookButton) {
        bookButton.addEventListener("click", function () {
            const slotIdInput = document.querySelector('input[name="slot_id"]');
            const userIdInput = document.querySelector('input[name="user_id"]');
            const csrfTokenInput = document.querySelector('[name="csrfmiddlewaretoken"]');

            const programSelect = document.querySelector('select[name="program"]');
            const levelSelect = document.querySelector('select[name="level"]');

            // Проверка на наличие всех необходимых данных
            if (!slotIdInput || !userIdInput || !csrfTokenInput || !programSelect || !levelSelect) {
                alert("Не удалось получить необходимые данные для бронирования.");
                return;
            }

            const slotId = slotIdInput.value;
            const userId = userIdInput.value;
            const csrfToken = csrfTokenInput.value;
            const program = programSelect.value;
            const level = levelSelect.value;

            fetch("/book_slot/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({
                    slot_id: slotId,
                    user_id: userId,
                    program: program,
                    level: level
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Ошибка HTTP: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.message) {
                    alert(data.message);
                    window.location.href = "/"; // или другая страница после успешного бронирования
                } else {
                    alert(data.error || "Произошла неизвестная ошибка.");
                }
            })
            .catch(error => {
                console.error("Ошибка при создании записи:", error);
                alert("Ошибка при создании записи. Повторите попытку позже.");
            });
        });
    }
});









