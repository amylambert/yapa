/**
 * Task Status Toggle Engine
 *
 * Listens for click changes on task checkboxes and asynchronously
 * updates their status field via the Django backend API.
 */

// Track all status toggle checkboxes on the current view layout
document.querySelectorAll(".status-toggle").forEach((checkbox) => {
    checkbox.addEventListener("change", function () {
        // Extract routing configuration from the component attributes
        const updateUrl = this.getAttribute("data-url");
        const csrfToken = this.getAttribute("data-csrf");

        // Determine the exact status payload based on the checked state
        const targetStatus = this.checked ? "DONE" : "TODO";

        // Prepare form parameter data wrappers matching the backend view
        const formData = new FormData();
        formData.append("field", "status");
        formData.append("value", targetStatus);
        formData.append("csrfmiddlewaretoken", csrfToken);

        // Fire network payload state updates asynchronously
        fetch(updateUrl, {
            method: "POST",
            body: formData,
            headers: { "X-Requested-With": "XMLHttpRequest" },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.status === "success") {
                    // Map database keys to human-friendly display labels
                    const labels = { TODO: "To Do", DONE: "Done" };

                    // Securely locate and update the text container sibling
                    const listItem = this.closest("li");
                    const statusSpan =
                        listItem.querySelector(".subtask-status");

                    if (statusSpan) {
                        statusSpan.textContent = labels[targetStatus];
                    }
                } else {
                    // Fall back to original interface state if server rejects edit
                    this.checked = !this.checked;
                    alert("Could not update task execution status.");
                }
            })
            .catch(() => {
                // Roll back the toggle switch state on network dropouts
                this.checked = !this.checked;
                alert("Network communication failure.");
            });
    });
});
