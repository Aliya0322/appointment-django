document.addEventListener("DOMContentLoaded", function () {
    let selectedSlotId = null;
    let selectedDate = null;

    // Обработчик выбора даты
    document.querySelectorAll(".date").forEach(dateElem => {
        dateElem.addEventListener("click", function () {
            document.querySelectorAll(".date").forEach(el => el.classList.remove("selected"));
            this.classList.add("selected");

            selectedDate = this.dataset.date;
            console.log("Выбрана дата:", selectedDate); // Лог для проверки
            updateAvailableTimes(selectedDate);
        });
    });

    // Фильтрация доступного времени для выбранной даты
    function updateAvailableTimes(selectedDate) {
        let found = false;
        document.querySelectorAll(".time").forEach(timeElem => {
            if (timeElem.dataset.date === selectedDate) {
                timeElem.style.display = "block"; // Показываем время
                found = true;
            } else {
                timeElem.style.display = "none"; // Скрываем время для других дат
            }
        });

        if (!found) {
            console.log("Для этой даты нет доступного времени.");
        }
    }

    // Обработчик выбора времени
    document.querySelectorAll(".time").forEach(timeElem => {
        timeElem.addEventListener("click", function () {
            document.querySelectorAll(".time").forEach(el => el.classList.remove("selected"));
            this.classList.add("selected");

            selectedSlotId = this.dataset.slotId;
            document.getElementById("bookButton").disabled = false; // Активируем кнопку
        });
    });

    // Обработчик кнопки "Записаться"
    document.getElementById("bookButton").addEventListener("click", function () {
        if (selectedSlotId) {
            window.location.href = `{% url 'confirmation-page' %}?slot_id=${selectedSlotId}`;
        } else {
            alert("Пожалуйста, выберите время!");
        }
    });
});