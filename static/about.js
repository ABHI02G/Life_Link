document.addEventListener("DOMContentLoaded", () => {
  // Smooth scroll for internal links
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener("click", e => {
      const id = link.getAttribute("href").substring(1);
      const target = document.getElementById(id);
      if (!target) return;

      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  // Scroll reveal
  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("reveal-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.2 }
  );

  document.querySelectorAll(".reveal").forEach(el => observer.observe(el));

  // Tilt effect for cards (desktop only)
  const tiltCards = document.querySelectorAll(".tilt-card");
  const enableTilt = () => {
    if (window.innerWidth < 768) return;

    tiltCards.forEach(card => {
      card.addEventListener("mousemove", e => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const rotateY = ((x / rect.width) - 0.5) * 8;
        const rotateX = ((y / rect.height) - 0.5) * -8;
        card.style.transform = `perspective(700px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
      });
      card.addEventListener("mouseleave", () => {
        card.style.transform = "";
      });
    });
  };
  enableTilt();
  window.addEventListener("resize", () => tiltCards.forEach(c => (c.style.transform = "")));

  // Emergency button -> alert mode + toast
  const emergencyBtn = document.getElementById("emergencyBtn");
  const emergencyToast = document.getElementById("emergencyToast");
  const closeToast = document.getElementById("closeToast");

  const enterAlertMode = () => {
    document.body.classList.add("alert-mode");
    emergencyToast.classList.add("show");
  };

  const exitAlertMode = () => {
    document.body.classList.remove("alert-mode");
    emergencyToast.classList.remove("show");
  };

  emergencyBtn.addEventListener("click", () => {
    enterAlertMode();
  });

  closeToast.addEventListener("click", () => {
    exitAlertMode();
  });

  emergencyToast.addEventListener("click", e => {
    if (e.target === emergencyToast) {
      exitAlertMode();
    }
  });
});
