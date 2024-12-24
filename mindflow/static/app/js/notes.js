const textarea = document.getElementById('autoResizeTextarea');

textarea.addEventListener('input', function () {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
});

document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            const noteElement = this.closest(".note");
            const noteId = noteElement.dataset.noteId;

            if (confirm("Вы уверены, что хотите удалить эту заметку?")) {
                fetch(`/delete_note/${noteId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        noteElement.remove();
                    } else {
                        alert("Ошибка при удалении заметки.");
                    }
                });
            }
        });
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