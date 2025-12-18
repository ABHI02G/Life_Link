/* ---------------------------------------------------------
   MODE SWITCHING (User <-> Hospital)
--------------------------------------------------------- */

const body = document.body;

const userBtn = document.getElementById("userBtn");
const hospitalBtn = document.getElementById("hospitalBtn");
const sliderPill = document.getElementById("sliderPill");
const userForm = document.getElementById("userForm");
const hospitalForm = document.getElementById("hospitalForm");
const brandTagline = document.getElementById("brandTagline");
const brandPoints = document.getElementById("brandPoints");

function setUserMode() {
  userBtn.classList.add("active");
  hospitalBtn.classList.remove("active");

  sliderPill.style.transform = "translateX(0)";

  body.classList.add("user-mode");
  body.classList.remove("hospital-mode");

  userForm.classList.add("active");
  hospitalForm.classList.remove("active");

  brandTagline.innerHTML =
    `Register as a <strong>User</strong> to access LifeLink’s emergency-ready features.`;

  brandPoints.innerHTML = `
    <li>✓ View your medical profile quickly</li>
    <li>✓ Save emergency contacts & hospitals</li>
    <li>✓ Get faster help when it matters</li>
  `;
}

function setHospitalMode() {
  hospitalBtn.classList.add("active");
  userBtn.classList.remove("active");

  sliderPill.style.transform = "translateX(126px)";

  body.classList.add("hospital-mode");
  body.classList.remove("user-mode");

  hospitalForm.classList.add("active");
  userForm.classList.remove("active");

  brandTagline.innerHTML =
    `Register as a <strong>Hospital</strong> to manage LifeLink emergency workflows.`;

  brandPoints.innerHTML = `
    <li>✓ Respond to incoming emergency requests</li>
    <li>✓ Access essential patient info securely</li>
    <li>✓ Coordinate faster with nearby facilities</li>
  `;
}

userBtn.addEventListener("click", setUserMode);
hospitalBtn.addEventListener("click", setHospitalMode);

// Default to USER
setUserMode();

/* ---------------------------------------------------------
   USER REGISTRATION (POST → Flask)
--------------------------------------------------------- */

document.getElementById("userLoginBtn").addEventListener("click", async (e) => {
  e.preventDefault();

  const name = document.querySelector("#userForm input[placeholder='Your Name']").value.trim();
  const age = document.querySelector("#userForm input[placeholder='Age']").value.trim();
  const email = document.getElementById("u_email").value.trim();
  const password = document.getElementById("u_pass").value.trim();

  if (!name || !age || !email || !password) {
    alert("Please fill all User Registration fields.");
    return;
  }

  try {
    const response = await fetch("/register_user", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, age, email, password })
    });

    const data = await response.json();

    if (data.status === "success") {
      window.location.href = "/dashboard";
    } else {
      alert("Registration failed.");
    }

  } catch (err) {
    console.error("User registration error:", err);
    alert("Something went wrong.");
  }
});

/* ---------------------------------------------------------
   HOSPITAL REGISTRATION (POST → Flask)
--------------------------------------------------------- */

document.getElementById("hospitalLoginBtn").addEventListener("click", async (e) => {
  e.preventDefault();

  const email = document.getElementById("h_email").value.trim();
  const password = document.getElementById("h_pass").value.trim();
  const name = document.getElementById("h_code").value.trim();
  
 

  

  try {
    const response = await fetch("/register_hospital", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, name })
    });

    const data = await response.json();

    if (data.status === "success") {
      window.location.href = "/h_dashboard";
    } else {
      alert("Hospital registration failed.");
    }

  } catch (err) {
    console.error("Hospital registration error:", err);
    alert("Something went wrong with hospital registration.");
  }
});
