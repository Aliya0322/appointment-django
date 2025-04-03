

document.addEventListener("DOMContentLoaded", function() {

    document.querySelectorAll(".cancel-button").forEach(button => {
        button.addEventListener("click", function() {
            let lessonId = this.getAttribute("data-lesson-id");

            if (confirm("Вы уверены, что хотите отменить занятие?")) {
                fetch("/cancel_lesson/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCSRFToken()
                    },
                    body: JSON.stringify({ lesson_id: lessonId })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert("Занятие отменено!");
                        this.closest(".block").remove();
                    } else {
                        alert("Ошибка при отмене занятия.");
                    }
                })
                .catch(error => console.error("Ошибка:", error));
            }
        });
    });
});

// Функция для получения CSRF-токена
function getCSRFToken() {
    return document.cookie.split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}