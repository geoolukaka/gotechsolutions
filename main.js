/* GoTech Solutions - shared front-end behaviour
   - mobile nav toggle
   - pre-fill "Area of Interest" on the contact page from ?service=
   - submit the contact form to a Google Sheet via a Google Apps Script Web App
*/

// ======================================================================
// 1. CONFIG — point this at your deployed Python backend's /api/contact
//    endpoint. See /backend/README.md for setup (MySQL or Google Sheets).
//    For local testing: http://localhost:5000/api/contact
// ======================================================================
const CONTACT_API_URL = "PASTE_YOUR_BACKEND_API_URL_HERE/api/contact";

// ----------------------------------------------------------------------
// Mobile menu toggle
// ----------------------------------------------------------------------
function initMobileMenu() {
  const toggleBtn = document.querySelector("[data-menu-toggle]");
  const menu = document.querySelector("[data-mobile-menu]");
  if (!toggleBtn || !menu) return;

  toggleBtn.addEventListener("click", () => {
    const isOpen = menu.classList.toggle("open");
    toggleBtn.setAttribute("aria-expanded", isOpen ? "true" : "false");
    const icon = toggleBtn.querySelector(".material-symbols-outlined");
    if (icon) icon.textContent = isOpen ? "close" : "menu";
  });

  // Close menu when a link inside it is clicked
  menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      menu.classList.remove("open");
      toggleBtn.setAttribute("aria-expanded", "false");
      const icon = toggleBtn.querySelector(".material-symbols-outlined");
      if (icon) icon.textContent = "menu";
    });
  });
}

// ----------------------------------------------------------------------
// Pre-fill contact form's "Area of Interest" from a query string,
// e.g. contact.html?service=Graphic%20Design (set by "Learn More" links)
// ----------------------------------------------------------------------
function prefillServiceFromQuery() {
  const select = document.querySelector("#service");
  if (!select) return;

  const params = new URLSearchParams(window.location.search);
  const service = params.get("service");
  if (!service) return;

  const options = Array.from(select.options);
  const match = options.find(
    (opt) => opt.value.toLowerCase() === service.toLowerCase()
  );
  if (match) {
    select.value = match.value;
  }
}

// ----------------------------------------------------------------------
// Contact form submission -> Python backend (MySQL or Google Sheets)
// ----------------------------------------------------------------------
function initContactForm() {
  const form = document.querySelector("#contact-form");
  if (!form) return;

  const statusBox = document.querySelector("#form-status");
  const submitBtn = form.querySelector('button[type="submit"]');

  function showStatus(message, type) {
    if (!statusBox) return;
    statusBox.textContent = message;
    statusBox.classList.remove("success", "error", "show");
    statusBox.classList.add(type, "show");
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Simple client-side validation
    const name = form.name.value.trim();
    const phone = form.phone.value.trim();
    const email = form.email.value.trim();
    const service = form.service.value.trim();
    const message = form.message.value.trim();

    if (!name || !email || !message) {
      showStatus("Please fill in your name, email, and project details.", "error");
      return;
    }
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
      showStatus("Please enter a valid email address.", "error");
      return;
    }

    if (CONTACT_API_URL.includes("PASTE_YOUR_BACKEND_API_URL_HERE")) {
      showStatus(
        "Form is not connected yet. Add your backend API URL in assets/js/main.js (see backend/README.md).",
        "error"
      );
      return;
    }

    submitBtn.disabled = true;
    const originalLabel = submitBtn.textContent;
    submitBtn.textContent = "Sending...";

    const payload = {
      name,
      phone,
      email,
      service,
      message,
      page: window.location.href
    };

    try {
      const response = await fetch(CONTACT_API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const result = await response.json().catch(() => ({}));

      if (response.ok && result.status === "success") {
        showStatus("Thank you! Your inquiry has been sent. We'll be in touch shortly.", "success");
        form.reset();
      } else {
        showStatus(
          result.message || "Something went wrong sending your message. Please try again or email us directly.",
          "error"
        );
      }
    } catch (err) {
      console.error("Contact form submission failed:", err);
      showStatus("Something went wrong sending your message. Please try again or email us directly.", "error");
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = originalLabel;
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initMobileMenu();
  prefillServiceFromQuery();
  initContactForm();
});
