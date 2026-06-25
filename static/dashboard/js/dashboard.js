/**
 * @file sidebar.js
 * @description Controls navigation panels and binds instant mobile touch tracking hooks.
 */

// Native WebKit layout hook: Forces mobile browsers to process active state clicks instantly
document.addEventListener("touchstart", () => {}, { passive: true });

class DashboardMenuController {
    constructor() {
        this.menuToggle = document.getElementById("mobile-menu-toggle");
        this.menuClose = document.getElementById("mobile-menu-close");
        this.sidebar = document.getElementById("sidebar-drawer");
        this.overlay = document.getElementById("menu-overlay");

        if (this.menuToggle && this.sidebar && this.overlay) {
            this.registerDrawerListeners();
        }
    }

    registerDrawerListeners() {
        this.menuToggle.addEventListener("click", () => this.openMenu());
        this.overlay.addEventListener("click", () => this.closeMenu());

        if (this.menuClose) {
            this.menuClose.addEventListener("click", () => this.closeMenu());
        }
    }

    openMenu() {
        this.sidebar.classList.add("is-active");
        this.overlay.classList.add("is-active");
    }

    closeMenu() {
        this.sidebar.classList.remove("is-active");
        this.overlay.classList.remove("is-active");
    }
}

class DashboardModalController {
    constructor() {
        this.triggerBtn = document.getElementById("global-create-btn");
        this.closeBtn = document.getElementById("modal-close-btn");
        this.overlay = document.getElementById("create-modal-overlay");

        if (this.triggerBtn && this.closeBtn && this.overlay) {
            this.initModalListeners();
        }
    }

    initModalListeners() {
        this.triggerBtn.addEventListener("click", () => this.showModal());
        this.closeBtn.addEventListener("click", () => this.hideModal());
        this.overlay.addEventListener("click", (e) => {
            if (e.target === this.overlay) this.hideModal();
        });

        window.addEventListener("keydown", (e) => {
            if (
                e.key === "Escape" &&
                this.overlay.classList.contains("is-active")
            ) {
                this.hideModal();
            }
        });
    }

    showModal() {
        this.overlay.classList.add("is-active");
    }

    hideModal() {
        this.overlay.classList.remove("is-active");
    }
}

/* --- Navigation Bootstrapping --- */
document.addEventListener("DOMContentLoaded", () => {
    new DashboardMenuController();
    new DashboardModalController();
});
