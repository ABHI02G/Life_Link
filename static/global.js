// =============== SIDEBAR & MENU TOGGLE ===============

document.addEventListener("DOMContentLoaded", function () {
  const body = document.body;
  const sidebarToggle = document.querySelector(".sidebar-toggle");
  const sidebarClose = document.querySelector(".sidebar-close");
  const sidebarLinks = document.querySelectorAll(".sidebar-links a");

  function openSidebar() {
    body.classList.add("sidebar-open");
  }

  function closeSidebar() {
    body.classList.remove("sidebar-open");
  }

  function toggleSidebar() {
    if (body.classList.contains("sidebar-open")) {
      closeSidebar();
    } else {
      openSidebar();
    }
  }

  // MENU button (hamburger)
  if (sidebarToggle) {
    sidebarToggle.addEventListener("click", toggleSidebar);
  }

  // Close icon inside sidebar
  if (sidebarClose) {
    sidebarClose.addEventListener("click", closeSidebar);
  }

  // Close after clicking any sidebar link (mobile/desktop)
  if (sidebarLinks && sidebarLinks.length) {
    sidebarLinks.forEach((link) => {
      link.addEventListener("click", closeSidebar);
    });
  }

  // ESC key closes sidebar
  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeSidebar();
    }
  });
});

// =============== EMERGENCY BUTTON & TOAST ===============

(function () {
  const emergencyBtn = document.getElementById("emergencyBtn");
  const emergencyToast = document.getElementById("emergencyToast");
  const closeToastBtn = document.getElementById("closeToast");

  if (!emergencyBtn || !emergencyToast) return;

  function openToast() {
    emergencyToast.classList.add("active");
  }

  function closeToast() {
    emergencyToast.classList.remove("active");
  }

  emergencyBtn.addEventListener("click", openToast);

  if (closeToastBtn) {
    closeToastBtn.addEventListener("click", closeToast);
  }

  // Auto-hide toast after some time
  emergencyBtn.addEventListener("click", () => {
    setTimeout(() => {
      closeToast();
    }, 7000);
  });
})();

// =============== REVEAL-ON-SCROLL ANIMATION ===============

(function () {
  const revealEls = document.querySelectorAll(".reveal");
  if (!revealEls.length) return;

  if (!("IntersectionObserver" in window)) {
    revealEls.forEach((el) => el.classList.add("reveal-visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("reveal-visible");
        observer.unobserve(entry.target);
      });
    },
    {
      threshold: 0.1,
    }
  );

  revealEls.forEach((el) => observer.observe(el));
})();

// =============== TILT-CARD HOVER EFFECT ===============

(function () {
  const cards = document.querySelectorAll(".tilt-card");
  if (!cards.length) return;

  const maxTilt = 10; // degrees

  cards.forEach((card) => {
    let rect = null;

    function updateRect() {
      rect = card.getBoundingClientRect();
    }

    function handleMove(event) {
      if (!rect) updateRect();

      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;

      const percentX = x / rect.width - 0.5;
      const percentY = y / rect.height - 0.5;

      const rotateX = (-percentY * maxTilt).toFixed(2);
      const rotateY = (percentX * maxTilt).toFixed(2);

      card.style.transform =
        `rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(0)`;
    }

    function resetTilt() {
      card.style.transform = "rotateX(0deg) rotateY(0deg) translateZ(0)";
    }

    card.addEventListener("mouseenter", updateRect);
    card.addEventListener("mousemove", handleMove);
    card.addEventListener("mouseleave", resetTilt);

    window.addEventListener("resize", () => {
      rect = null;
    });
  });
})();
