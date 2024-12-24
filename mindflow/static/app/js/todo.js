const textarea = document.getElementById('autoResizeTextarea');

textarea.addEventListener('input', function () {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
});

document.querySelectorAll('.todo-checkbox').forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        const todoId = this.dataset.todoId;
        const done = this.checked;

        console.log(`Отправка запроса для todo_id: ${todoId}, done: ${done}`);

        fetch('/update-todo-status/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                todo_id: todoId,
                done: done
            })
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert('Ошибка обновления состояния задачи');
            } else {
                console.log('Задача обновлена успешно');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Ошибка обновления состояния задачи');
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.body.addEventListener("click", function(event) {
        if (event.target && event.target.classList.contains("delete-btn")) {
            const todoElement = event.target.closest(".todo-today");
            const todoId = todoElement.dataset.todoId;

            if (confirm("Вы уверены, что хотите удалить эту задачу?")) {
                fetch(`/delete_todo/${todoId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        todoElement.remove();
                        location.reload();
                    } else {
                        alert("Ошибка при удалении задачи.");
                    }
                })
                .catch(error => {
                    console.error("Ошибка запроса:", error);
                    alert("Ошибка при удалении задачи.");
                });
            }
        }
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
