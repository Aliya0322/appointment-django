document.addEventListener("DOMContentLoaded", function () {
    let selectedSlotId = null;
    let selectedDate = null;
    const bookButton = document.getElementById("bookButton");

    if (!bookButton) {
        console.error("Кнопка 'Записаться' не найдена!");
        return;
    }

    const dateElements = document.querySelectorAll(".date");
    const timeElements = document.querySelectorAll(".time");

    // Проверяем, есть ли даты на странице
    if (dateElements.length > 0) {
        dateElements.forEach(dateElem => {
            dateElem.addEventListener("click", function () {
                dateElements.forEach(el => el.classList.remove("selected"));
                this.classList.add("selected");

                selectedDate = this.dataset.date;
                console.log("Выбрана дата:", selectedDate);

                updateAvailableTimes(selectedDate);

                // Сбрасываем выбор времени при смене даты
                selectedSlotId = null;
                bookButton.disabled = true;
            });
        });
    } else {
        console.warn("Нет доступных дат для выбора.");
    }

    // Фильтрация доступного времени для выбранной даты
    function updateAvailableTimes(selectedDate) {
        let found = false;

        if (timeElements.length > 0) {
            timeElements.forEach(timeElem => {
                if (timeElem.dataset.date === selectedDate) {
                    timeElem.hidden = false;
                    found = true;
                } else {
                    timeElem.hidden = true;
                    timeElem.classList.remove("selected"); // Убираем выделение скрытых
                }
            });
        }

        if (!found) {
            console.log("Для этой даты нет доступного времени.");
        }
    }

    // Проверяем, есть ли время на странице
    if (timeElements.length > 0) {
        timeElements.forEach(timeElem => {
            timeElem.addEventListener("click", function () {
                timeElements.forEach(el => el.classList.remove("selected"));
                this.classList.add("selected");

                selectedSlotId = this.dataset.slotId;
                bookButton.disabled = false;
            });
        });
    } else {
        console.warn("Нет доступного времени для выбора.");
    }

    // Обработчик кнопки "Записаться"
    bookButton.addEventListener("click", function () {
        let baseUrl = this.dataset.url;
        if (selectedSlotId) {
            window.location.href = `${baseUrl}?slot_id=${selectedSlotId}`;
        } else {
            alert("Пожалуйста, выберите время!");
        }
    });
});
