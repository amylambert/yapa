/**
 * Focus Monitor Countdown Automation Engine with Session Persistence.
 * Handles Pomodoro orchestration and state persistence via localStorage.
 */
class FocusMonitorTimer {
    /**
     * Initializes elements and restores state from browser storage.
     */
    constructor() {
        this.display = document.getElementById("timer-clock-display");
        this.toggleBtn = document.getElementById("timer-toggle-btn");
        this.resetBtn = document.getElementById("timer-reset-btn");
        this.incBtn = document.getElementById("timer-inc-btn");
        this.decBtn = document.getElementById("timer-dec-btn");
        this.statusLbl = document.getElementById("timer-status-indicator");

        this.countdownInterval = null;

        if (this.display) {
            this.loadState();
            this.initEventListeners();
            this.renderDisplay();

            if (this.isRunning) {
                this.startIntervalLoop();
            }
        }
    }

    /**
     * Binds tracking routines to interface buttons.
     */
    initEventListeners() {
        this.toggleBtn.addEventListener("click", () => this.toggleExecution());
        this.resetBtn.addEventListener("click", () => this.resetHardware());
        this.incBtn.addEventListener("click", () => this.modifyMinutes(1));
        this.decBtn.addEventListener("click", () => this.modifyMinutes(-1));

        const presets = document.querySelectorAll(".preset-macro-btn");
        presets.forEach((btn) => {
            btn.addEventListener("click", (e) => this.applyPreset(e));
        });
    }

    /**
     * Restores state tracking boundaries from local browser storage.
     */
    loadState() {
        this.isRunning = localStorage.getItem("yapa_timer_running") === "true";
        this.currentMode =
            localStorage.getItem("yapa_timer_mode") || "Focus Session";

        const savedTotal = localStorage.getItem("yapa_timer_total");
        this.totalSeconds = savedTotal ? parseInt(savedTotal, 10) : 1500;

        if (this.isRunning) {
            const endTime = localStorage.getItem("yapa_timer_end_time");
            if (endTime) {
                const remaining = Math.round(
                    (parseInt(endTime, 10) - Date.now()) / 1000,
                );
                if (remaining > 0) {
                    this.totalSeconds = remaining;
                } else {
                    this.isRunning = false;
                    this.totalSeconds = 0;
                    this.clearStorageState();
                }
            }
        }
    }

    /**
     * Saves persistent execution data parameters to local storage.
     */
    saveState() {
        localStorage.setItem("yapa_timer_running", this.isRunning);
        localStorage.setItem("yapa_timer_mode", this.currentMode);
        localStorage.setItem("yapa_timer_total", this.totalSeconds);

        if (this.isRunning) {
            const endTime = Date.now() + this.totalSeconds * 1000;
            localStorage.setItem("yapa_timer_end_time", endTime);
        } else {
            localStorage.removeItem("yapa_timer_end_time");
        }
    }

    /**
     * Purges cached parameters from client browser storage.
     */
    clearStorageState() {
        localStorage.removeItem("yapa_timer_running");
        localStorage.removeItem("yapa_timer_mode");
        localStorage.removeItem("yapa_timer_total");
        localStorage.removeItem("yapa_timer_end_time");
    }

    /**
     * Toggles active clock calculation status.
     */
    toggleExecution() {
        if (this.isRunning) {
            this.pauseTracker();
        } else {
            this.startTracker();
        }
    }

    /**
     * Transitions system state into active running profile mode.
     */
    startTracker() {
        if (this.totalSeconds <= 0) return;
        this.isRunning = true;
        this.saveState();
        this.startIntervalLoop();
    }

    /**
     * Commences core execution loop thread.
     */
    startIntervalLoop() {
        this.toggleBtn.textContent = "PAUSE";
        this.statusLbl.textContent = this.currentMode;

        const storedEnd = localStorage.getItem("yapa_timer_end_time");
        const endTime = storedEnd
            ? parseInt(storedEnd, 10)
            : Date.now() + this.totalSeconds * 1000;

        this.countdownInterval = setInterval(() => {
            const remaining = Math.round((endTime - Date.now()) / 1000);

            if (remaining <= 0) {
                this.totalSeconds = 0;
                this.renderDisplay();
                this.handleCycleCompletion();
            } else {
                this.totalSeconds = remaining;
                this.renderDisplay();
            }
        }, 1000);
    }

    /**
     * Suspends processing ticks without clearing underlying limits.
     */
    pauseTracker() {
        this.isRunning = false;
        clearInterval(this.countdownInterval);
        this.saveState();
        this.toggleBtn.textContent = "START";
        this.statusLbl.textContent = "System Paused";
    }

    /**
     * Flushes parameters back onto safe initialization vectors.
     */
    resetHardware() {
        this.isRunning = false;
        clearInterval(this.countdownInterval);
        this.clearStorageState();
        this.totalSeconds = 1500;
        this.currentMode = "Focus Session";
        this.toggleBtn.textContent = "START";
        this.statusLbl.textContent = "System Idle";
        this.renderDisplay();
    }

    /**
     * Alters remaining durations incrementally by safe integer bounds.
     */
    modifyMinutes(deltaMinutes) {
        if (this.isRunning) return;
        const target = this.totalSeconds + deltaMinutes * 60;
        if (target >= 60 && target <= 5940) {
            this.totalSeconds = target;
            this.saveState();
            this.renderDisplay();
        }
    }

    /**
     * Applies pre-staged operational macros directly into variables.
     */
    applyPreset(event) {
        this.isRunning = false;
        clearInterval(this.countdownInterval);

        const workMinutes = parseInt(event.target.dataset.work, 10);
        this.totalSeconds = workMinutes * 60;
        this.currentMode = "Focus Session";
        this.isRunning = true;

        this.saveState();
        this.renderDisplay();
        this.startIntervalLoop();
    }

    /**
     * Executes fallback indicators when ticking steps complete.
     */
    handleCycleCompletion() {
        this.isRunning = false;
        clearInterval(this.countdownInterval);
        this.clearStorageState();
        this.toggleBtn.textContent = "START";
        this.statusLbl.textContent = "Cycle Finished!";

        if (window.Notification && Notification.permission === "granted") {
            new Notification("YAPA System: Focus cycle complete.");
        }
    }

    /**
     * Direct element layout writer pipeline utilizing safe text methods.
     */
    renderDisplay() {
        const minutes = Math.floor(this.totalSeconds / 60);
        const seconds = this.totalSeconds % 60;
        const displayMin = minutes.toString().padStart(2, "0");
        const displaySec = seconds.toString().padStart(2, "0");
        this.display.textContent = `${displayMin}:${displaySec}`;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    new FocusMonitorTimer();
});
