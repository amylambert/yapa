/**
 * @file register.js
 * @description Secure OOP password verification with active event tracking.
 */

class PasswordStrengthEngine {
    /**
     * @param {string} passwordSelector - Selector for password input.
     * @param {string} usernameSelector - Selector for username input.
     * @param {string} targetContainerId - Element to attach metrics to.
     */
    constructor(passwordSelector, usernameSelector, targetContainerId) {
        this.passwordInput = document.querySelector(passwordSelector);
        this.usernameInput = document.querySelector(usernameSelector);
        this.container = document.getElementById(targetContainerId);

        console.log("Initializing Password Engine...");
        console.log("Target Input Element:", this.passwordInput);
        console.log("Target Render Container:", this.container);

        if (!this.passwordInput || !this.container) {
            console.warn("Aborting: Critical DOM targets not found.");
            return;
        }

        this.criteria = [
            {
                id: "len",
                text: "Must contain at least 8 characters.",
                check: (val) => val.length >= 8,
            },
            {
                id: "num",
                text: "Cannot be entirely numeric.",
                check: (val) => val.length > 0 && /\D/.test(val),
            },
            {
                id: "user",
                text: "Cannot match or contain your username.",
                check: (val) => {
                    const user = this.usernameInput?.value || "";
                    if (!user || !val) return true;
                    return !val.toLowerCase().includes(user.toLowerCase());
                },
            },
            {
                id: "cpx",
                text: "Must contain an uppercase letter or symbol.",
                check: (val) => /[A-Z]/.test(val) || /[^A-Za-z0-9]/.test(val),
            },
        ];

        this.elements = {};
        this.setupUI();
        this.registerListeners();
    }

    /**
     * Generates UI elements using secure, XSS-proof DOM methods.
     */
    setupUI() {
        const wrapper = document.createElement("div");
        wrapper.className = "indicator-wrapper";

        const track = document.createElement("div");
        track.className = "meter-track";

        this.elements.fill = document.createElement("div");
        this.elements.fill.className = "meter-fill";
        track.appendChild(this.elements.fill);
        wrapper.appendChild(track);

        const list = document.createElement("ul");
        list.className = "criteria-list";

        this.elements.items = {};
        this.criteria.forEach((item) => {
            const li = document.createElement("li");
            li.className = "criteria-item";
            li.textContent = item.text;
            list.appendChild(li);
            this.elements.items[item.id] = li;
        });

        wrapper.appendChild(list);
        this.container.appendChild(wrapper);
        console.log("UI Elements successfully mounted to DOM.");
    }

    /**
     * Attaches listeners with forced instance context execution.
     */
    registerListeners() {
        this.passwordInput.addEventListener("input", () => {
            console.log("Keystroke event captured on password field.");
            this.evaluate();
        });

        if (this.usernameInput) {
            this.usernameInput.addEventListener("input", () => {
                console.log("Keystroke event captured on username field.");
                this.evaluate();
            });
        }
    }

    /**
     * Evaluates active validation states across rules.
     */
    evaluate() {
        const value = this.passwordInput.value;
        let checksMet = 0;

        console.log(`Evaluating string value: "${value}"`);

        this.criteria.forEach((item) => {
            const isPassed = item.check(value);
            const el = this.elements.items[item.id];

            if (isPassed && value.length > 0) {
                el.classList.add("is-met");
                checksMet++;
            } else {
                el.classList.remove("is-met");
            }
        });

        console.log(`Validation complete. Rules passed: ${checksMet}`);
        this.updateMeter(checksMet);
    }

    /**
     * Updates progress bar inline spacing and styling classes.
     * @param {number} totalPassed - Structural total of passed rules.
     */
    updateMeter(totalPassed) {
        const percentage = (totalPassed / this.criteria.length) * 100;
        this.elements.fill.style.width = `${percentage}%`;
        this.elements.fill.className = "meter-fill";

        if (totalPassed === 0) return;

        if (totalPassed === 1) {
            this.elements.fill.classList.add("fill-weak");
        } else if (totalPassed === 2) {
            this.elements.fill.classList.add("fill-fair");
        } else if (totalPassed === 3) {
            this.elements.fill.classList.add("fill-good");
        } else {
            this.elements.fill.classList.add("fill-strong");
        }
    }
}

/**
 * Instantiates the class targeting default Django form field IDs.
 */
function initializeStrengthEngine() {
    new PasswordStrengthEngine(
        "#id_password1",
        "#id_username",
        "password-requirements-feedback",
    );
}

/* --- Defensive Execution Guard against DOM Race Conditions --- */
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
        initializeStrengthEngine();
    });
} else {
    initializeStrengthEngine();
}
