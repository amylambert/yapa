/**
 * @fileoverview Manages state and accessibility flags for the notes tree.
 * Uses a centralized state class strategy to prevent CSS display conflicts.
 */

class NotesDirectoryTree {
    /**
     * Bind component tracking to the wrapper container element.
     * @param {string} containerSelector - Main tree wrapper query string.
     */
    constructor(containerSelector) {
        this.container = document.querySelector(containerSelector);
        if (!this.container) return;

        this.init();
    }

    /** Attach click event listeners securely to interaction targets. */
    init() {
        const triggers = this.container.querySelectorAll(
            ".note-toggle-trigger",
        );

        triggers.forEach((trigger) => {
            trigger.addEventListener("click", (event) => {
                this.toggleNode(event.currentTarget);
            });
        });
    }

    /**
     * Toggle the active card state class and synchronize ARIA values.
     * @param {HTMLButtonElement} trigger - The interactive header element.
     */
    toggleNode(trigger) {
        const card = trigger.closest(".note-accordion-card");
        if (!card) return;

        // Toggle state class and derive current status for screen readers
        const isOpen = card.classList.toggle("is-open");
        trigger.setAttribute("aria-expanded", isOpen.toString());
    }
}

// Fire initialization as soon as the DOM framework finishes parsing
document.addEventListener("DOMContentLoaded", () => {
    new NotesDirectoryTree(".notes-directory-tree");
});
