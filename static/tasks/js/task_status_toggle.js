/**
 * Task Status Toggle Engine
 *
 * Listens for click changes on task checkboxes and asynchronously
 * updates their status field via the Django backend API.
 */

document.querySelectorAll(".status-toggle").forEach((checkbox) => {
    checkbox.addEventListener("change", function () {
        const updateUrl = this.getAttribute("data-url");
        const csrfToken = this.getAttribute("data-csrf");
        const targetStatus = this.checked ? "DONE" : "TODO";

        const formData = new FormData();
        formData.append("field", "status");
        formData.append("value", targetStatus);
        formData.append("csrfmiddlewaretoken", csrfToken);

        fetch(updateUrl, {
            method: "POST",
            body: formData,
            headers: { "X-Requested-With": "XMLHttpRequest" },
        })
            .then((response) => {
                // Robust check: Catch 403, 404, or 500 pages before parsing JSON
                if (!response.ok) {
                    throw new Error(`HTTP network error: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                if (data.status === "success") {
                    const labels = { TODO: "To Do", DONE: "Done" };

                    // Update sub-task text inside list configurations
                    const listItem = this.closest("li");
                    if (listItem) {
                        const statusSpan =
                            listItem.querySelector(".subtask-status");
                        if (statusSpan) {
                            statusSpan.textContent = labels[targetStatus];
                        }
                    }

                    // Update main-task details header text layouts
                    const mainStatus =
                        document.querySelector(".main-task-status");
                    if (
                        mainStatus &&
                        this.classList.contains("main-task-toggle")
                    ) {
                        mainStatus.textContent = labels[targetStatus];
                    }
                } else {
                    this.checked = !this.checked;
                    alert("Could not update task execution status.");
                }
            })
            .catch((error) => {
                // Roll back interface and print clear diagnostic errors to F12
                this.checked = !this.checked;
                console.error("Task update operation failed:", error);
                alert("Network communication failure.");
            });
    });
});
