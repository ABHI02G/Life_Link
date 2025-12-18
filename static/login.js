document.addEventListener("DOMContentLoaded", () => {

  const userBtn = document.getElementById("userBtn");
  const hospitalBtn = document.getElementById("hospitalBtn");
  const sliderPill = document.getElementById("sliderPill");
  const capsule = document.getElementById("capsule");

  const userForm = document.getElementById("userForm");
  const hospitalForm = document.getElementById("hospitalForm");

  const modeLabel = document.getElementById("modeLabel");

  /* -------------------------
      MODE SWITCHING
  -------------------------- */
  function positionSlider(button) {
    const btnRect = button.getBoundingClientRect();
    const capRect = capsule.getBoundingClientRect();
    const left = btnRect.left - capRect.left + 4;
    sliderPill.style.left = `${left}px`;
    sliderPill.style.width = `${btnRect.width - 8}px`;
  }

  function setUserMode() {
    userBtn.classList.add("active");
    hospitalBtn.classList.remove("active");
    userForm.classList.add("active");
    hospitalForm.classList.remove("active");
    document.body.classList.add("user-mode");
    document.body.classList.remove("hospital-mode");
    modeLabel.textContent = "User";
    positionSlider(userBtn);
  }

  function setHospitalMode() {
    hospitalBtn.classList.add("active");
    userBtn.classList.remove("active");
    hospitalForm.classList.add("active");
    userForm.classList.remove("active");
    document.body.classList.add("hospital-mode");
    document.body.classList.remove("user-mode");
    modeLabel.textContent = "Hospital";
    positionSlider(hospitalBtn);
  }

  userBtn.addEventListener("click", setUserMode);
  hospitalBtn.addEventListener("click", setHospitalMode);
  requestAnimationFrame(setUserMode);

  /* -------------------------
      USER LOGIN
  -------------------------- */
  userForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("u_email").value.trim();
    const password = document.getElementById("u_pass").value.trim();

    if (!email || !password) {
      alert("Please enter your email and password.");
      return;
    }

    try {
      const res = await fetch("/login_user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });

      const data = await res.json();

      if (data.status === "success") {
        window.location.href = "/dashboard";
      } else {
        alert("Incorrect email or password.");
      }

    } catch (err) {
      alert("Server error. Try again.");
    }
  });

  /* -------------------------
      HOSPITAL LOGIN
  -------------------------- */
  hospitalForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("h_email").value.trim();
    const password = document.getElementById("h_pass").value.trim();

    if (!email || !password) {
      alert("Please enter hospital login credentials.");
      return;
    }

    try {
      const res = await fetch("/login_hospital", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });

      const data = await res.json();

      if (data.status === "success") {
        window.location.href = "/h_dashboard";
      } else {
        alert("Incorrect hospital login details.");
      }

    } catch (err) {
      alert("Server error. Try again.");
    }
  });

});
