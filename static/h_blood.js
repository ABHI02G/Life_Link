// h_blood.js - attach to hospital page to POST blood records to /api/save_blood
document.addEventListener("DOMContentLoaded", () => {
  // NOTE: your h_blood.html had duplicate id="quantity" on multiple inputs.
  // We assume you updated the HTML as instructed below (h_name, h_address, q_quantity).
  const saveBtn = document.getElementById("addBtn");
  const hName = document.getElementById("h_name");
  const hAddress = document.getElementById("h_address");
  const bloodType = document.getElementById("bloodType");
  const component = document.getElementById("component");
  const quantity = document.getElementById("q_quantity");
  const entryDate = document.getElementById("entryDate");
  const phone = document.getElementById("h_phone"); // optional, add to html if desired
  const mapQueryInput = document.getElementById("mapQuery"); // optional

  async function saveBloodToServer() {
    const payload = {
      hospitalName: hName ? hName.value.trim() : "",
      address: hAddress ? hAddress.value.trim() : "",
      bloodType: bloodType ? bloodType.value : "",
      component: component ? component.value : "",
      quantity: quantity ? Number(quantity.value) : 0,
      mapQuery: mapQueryInput ? mapQueryInput.value.trim() : "",
      phone: phone ? phone.value.trim() : "",
    };

    if (!payload.hospitalName || !payload.bloodType || !payload.component || !payload.quantity) {
      alert("Please fill Hospital name, blood type, component and quantity");
      return;
    }

    try {
      const res = await fetch("/api/save_blood", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (res.ok && data.status === "success") {
        alert("Saved to Blood DB");
        // optionally refresh UI or clear form
      } else {
        alert("Save failed: " + (data.message || "unknown"));
      }
    } catch (err) {
      console.error(err);
      alert("Network error saving blood record");
    }
  }

  if (saveBtn) saveBtn.addEventListener("click", (e) => {
    e.preventDefault();
    saveBloodToServer();
  });
});
