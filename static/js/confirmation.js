document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('confirmButton').addEventListener('click', function() {
        var program = document.getElementById('program').value;
        var level = document.getElementById('level').value;
        var url = this.dataset.url;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({
                teacher_id: "{{ teacher.id }}",
                slot_id: "{{ slot.id }}",
                program: program,
                level: level
            })
        }).then(response => response.json())
          .then(data => {
              if (data.success) {
                  alert('Бронирование успешно завершено!');
                  window.location.href = '{% url 'main-page' %}';
              } else {
                  alert('Ошибка при бронировании.');
              }
          });
    });
});
