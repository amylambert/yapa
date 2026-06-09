/**
 * Task Inline Update Engine
 *
 * Handles double-click interactions to turn plain text fields into
 * editable input fields, textareas, or dropdown selectors. Saves
 * changes asynchronously via AJAX fetch requests to the Django backend.
 */

// Find all elements marked as editable on the page
document.querySelectorAll(".editable").forEach((element) => {
    element.addEventListener("dblclick", function () {
        // If an input already exists, do nothing
        if (
            this.querySelector("input") ||
            this.querySelector("textarea") ||
            this.querySelector("select")
        ) {
            return;
        }

        // Extract tracking parameters from HTML data attributes
        const currentText = this.innerText.trim();
        const fieldName = this.getAttribute("data-field");
        const fieldType = this.getAttribute("data-type") || "text";
        const updateUrl = this.getAttribute("data-url");
        const csrfToken = this.getAttribute("data-csrf");

        // Instantiate the correct input control via function
        const input = createInputElement(this, fieldType, currentText);

        // Wipe existing text nodes and mount new input control.
        this.replaceChildren(input);
        input.focus();

        // Define the execution closure for saving the modified value
        const saveHandler = () => {
            sendDatabaseUpdate(
                this,
                input,
                currentText,
                fieldName,
                updateUrl,
                csrfToken,
            );
        };

        // Configure event listeners based on the interactive control type
        if (fieldType === "select") {
            // For dropdowns, save immediately upon user selection change
            input.addEventListener("change", saveHandler);
            input.addEventListener("blur", saveHandler);
        } else {
            // For regular inputs, save when clicking away
            input.addEventListener("blur", saveHandler);
            // For single-line inputs, also save when pressing the Enter key
            if (fieldType !== "textarea") {
                input.addEventListener("keydown", (e) => {
                    if (e.key === "Enter") saveHandler();
                });
            }
        }
    });
});

/**
 * Factory function to create the appropriate form element.
 *
 * @param {HTMLElement} element - The original editable wrapper element.
 * @param {string} fieldType - The targeted layout type (text/textarea/select).
 * @param {string} currentText - The existing text value inside the node.
 * @returns {HTMLElement} The configured HTML input/textarea/select node.
 */
function createInputElement(element, fieldType, currentText) {
    // Handle long text content fields (e.g., descriptions)
    if (fieldType === "textarea") {
        const textarea = document.createElement("textarea");
        const fallback = "No description provided. Double click to add one.";
        textarea.rows = 4;
        textarea.cols = 50;
        // Clear out the placeholder text if it matches the default message
        textarea.value = currentText === fallback ? "" : currentText;
        return textarea;
    }

    // Handle choice-based selection fields (e.g., status, priority)
    if (fieldType === "select") {
        const select = document.createElement("select");
        // Parse the JSON mapping options configured inside the HTML attribute
        const rawOptions = element.getAttribute("data-options");
        const optionsMap = JSON.parse(rawOptions || "{}");

        // Dynamically generate option nodes from the JSON key-value map
        for (const [key, label] of Object.entries(optionsMap)) {
            const opt = document.createElement("option");
            opt.value = key;
            opt.textContent = label; // Securely text-encoded value assignment
            // Pre-select the option that matches the current displayed state
            if (label === currentText) {
                opt.selected = true;
            }
            select.appendChild(opt);
        }
        return select;
    }

    // Default fallback: Create a standard single-line text input
    const input = document.createElement("input");
    input.type = "text";
    input.value = currentText;
    return input;
}

/**
 * Sends the updated value to the Django backend using an AJAX Fetch request.
 *
 * @param {HTMLElement} element - The original wrapper element to update.
 * @param {HTMLElement} input - The active input element holding the new value.
 * @param {string} oldText - The original value before editing started.
 * @param {string} field - The model field name being modified.
 * @param {string} url - The backend endpoint URL processing the POST payload.
 * @param {string} token - The CSRF security token for request authentication.
 */
function sendDatabaseUpdate(element, input, oldText, field, url, token) {
    let newValue = input.value.trim();
    let displayValue = newValue;

    // For selection dropdowns, display user-friendly text label
    if (input.tagName === "SELECT") {
        displayValue = input.options[input.selectedIndex].text;
    }

    // Exit early if the input is empty or if no modifications were made
    if (newValue === "" || displayValue === oldText) {
        element.textContent = oldText; // Secure text restoration
        return;
    }

    // Package the updated state data into standard form parameters
    const formData = new FormData();
    formData.append("field", field);
    formData.append("value", newValue);
    formData.append("csrfmiddlewaretoken", token);

    // Transmit the payload to the server asynchronously
    fetch(url, {
        method: "POST",
        body: formData,
        headers: { "X-Requested-With": "XMLHttpRequest" },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === "success") {
                // Permanently render the new text using secure plain text assignment
                element.textContent = displayValue;
            } else {
                // Revert to old value if the backend validation fails
                element.textContent = oldText;
                alert("Error saving modifications.");
            }
        })
        .catch(() => {
            // Revert to old value if a network connectivity failure occurs
            element.textContent = oldText;
            alert("Connection failure.");
        });
}
