/**
 * Unified Inline Update Engine
 *
 * Handles double-click event streams to transform elements into
 * form components, processing database modifications asynchronously.
 */

document.querySelectorAll(".editable").forEach((element) => {
    element.addEventListener("dblclick", function () {
        if (this.querySelector("input, textarea, select")) return;

        const currentText = this.innerText.trim();
        const field = this.getAttribute("data-field");
        const type = this.getAttribute("data-type") || "text";
        const url = this.getAttribute("data-url");
        const token = this.getAttribute("data-csrf");

        const input = createInputElement(type, currentText, this);

        this.replaceChildren(input);
        input.focus();

        // Transaction lock to prevent simultaneous Enter/Blur execution
        let isSaving = false;

        const save = () => {
            if (isSaving) return;
            isSaving = true;
            sendUpdate(this, input, currentText, field, url, token);
        };

        if (type === "select") {
            input.addEventListener("change", save);
            input.addEventListener("blur", save);
        } else {
            input.addEventListener("blur", save);
            if (type !== "textarea") {
                input.addEventListener("keydown", (e) => {
                    if (e.key === "Enter") save();
                });
            }
        }
    });
});

/**
 * Factory function to instantiate configured HTML form elements.
 *
 * @param {string} type - System interface target layout type.
 * @param {string} text - Existing text node values.
 * @param {HTMLElement} el - Wrapper element context.
 * @returns {HTMLElement} Form management component node.
 */
function createInputElement(type, text, el) {
    let input;

    if (type === "textarea") {
        input = document.createElement("textarea");
        input.rows = 4;
        input.cols = 50;
    } else if (type === "select") {
        input = document.createElement("select");
        const rawOpts = el.getAttribute("data-options") || "{}";
        const options = JSON.parse(rawOpts);

        for (const [key, label] of Object.entries(options)) {
            const opt = document.createElement("option");
            opt.value = key;
            opt.textContent = label;
            if (label === text) opt.selected = true;
            input.appendChild(opt);
        }
        return input;
    } else {
        input = document.createElement("input");
        input.type = type;

        if (type === "number") {
            input.min = "0";
            input.step = "1";
        }
    }

    const isFallback = text.startsWith("No ") || text.includes("Empty");
    input.value = isFallback ? "" : text.replace(" ", "T");
    return input;
}

/**
 * Dispatches the updated parameters securely to the backend framework.
 *
 * @param {HTMLElement} el - Element wrapper tracking states.
 * @param {HTMLElement} input - Active input node holding values.
 * @param {string} oldText - Text state before editing.
 * @param {string} field - Model attribute identifier string.
 * @param {string} url - Target routing path for database saving.
 * @param {string} token - CSRF structural protection value.
 */
function sendUpdate(el, input, oldText, field, url, token) {
    let newValue = input.value.trim();

    if (input.type === "number" && newValue === "") {
        newValue = "0";
    }

    let display = newValue;

    if (input.tagName === "SELECT") {
        display = input.options[input.selectedIndex].text;
    }

    if (newValue === "" || display === oldText) {
        el.textContent = oldText;
        return;
    }

    const formData = new FormData();
    formData.append("field", field);
    formData.append("value", newValue);
    formData.append("csrfmiddlewaretoken", token);

    fetch(url, {
        method: "POST",
        body: formData,
        headers: { "X-Requested-With": "XMLHttpRequest" },
    })
        .then((res) => {
            const ct = res.headers.get("content-type");
            if (!res.ok || !ct || !ct.includes("application/json")) {
                throw new Error("Expected JSON response from server.");
            }
            return res.json();
        })
        .then((data) => {
            if (data.status === "success") {
                el.textContent = display;
            } else {
                el.textContent = oldText;
                alert("Error saving changes.");
            }
        })
        .catch((err) => {
            el.textContent = oldText;
            alert("Backend transaction failed or returned invalid format.");
            console.error("System Engine Failure Context:", err);
        });
}

document.addEventListener("DOMContentLoaded", () => {
    const deleteForm = document.getElementById("secure-delete-form");
    if (deleteForm) {
        deleteForm.addEventListener("submit", (e) => {
            if (!confirm("Permanently delete this item?")) {
                e.preventDefault();
            }
        });
    }
});
