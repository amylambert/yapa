/**
 * @fileoverview Manages structural state, triggers, and live status labels.
 * Operates class engines uniformly across multiple directory layout systems.
 */

class DirectoryTree {
    /**
     * Bind component tracking to a target directory tree wrapper instance.
     * @param {HTMLElement} element - Root container node element.
     */
    constructor(element) {
        this.container = element;
        this.init();
    }

    /** Attach event listeners securely to interaction targets. */
    init() {
        const triggers = this.container.querySelectorAll(
            ".note-toggle-trigger",
        );
        const checkboxes = this.container.querySelectorAll(
            ".task-native-checkbox",
        );

        triggers.forEach((trigger) => {
            trigger.addEventListener("click", (event) => {
                this.toggleNode(event.currentTarget);
            });
        });

        checkboxes.forEach((checkbox) => {
            checkbox.addEventListener("change", (event) => {
                this.syncStatusText(event.currentTarget);
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

        const isOpen = card.classList.toggle("is-open");
        trigger.setAttribute("aria-expanded", isOpen.toString());
    }

    /**
     * Update internal status labels dynamically to mirror checkbox mutations.
     * @param {HTMLInputElement} checkbox - The target checklist form node.
     */
    syncStatusText(checkbox) {
        const card = checkbox.closest(".note-accordion-card");
        if (!card) return;

        const label = card.querySelector(".live-status-text");
        if (!label) return;

        // Use clean textContent configuration to rule out any XSS threats
        label.textContent = checkbox.checked ? "Done" : "Todo";
    }
}

// Find and build tracking modules across all designated folder blocks
document.addEventListener("DOMContentLoaded", () => {
    const trees = document.querySelectorAll(".directory-tree");
    trees.forEach((tree) => new DirectoryTree(tree));
});
