// ---------- Hospital Side Organ Saving (Firebase via Flask API) ----------

// Get selected organs
function getCheckedOrgans() {
  return Array.from(
    document.querySelectorAll('#organsCheckboxes input[type="checkbox"]:checked')
  ).map((i) => i.value.toLowerCase().replace(/\s+/g, '-')); // normalize
}

// Save to Firebase via backend API
async function saveEntryToServer() {
  const name = document.getElementById("h_name").value.trim();
  const address = document.getElementById("h_address").value.trim();
  const organs = getCheckedOrgans();

  if (!name || organs.length === 0) {
    alert("Please provide hospital name and select at least one organ.");
    return;
  }

  const payload = {
    hospitalName: name,
    address: address,
    organs: organs,
    blood: document.getElementById("bloodType").value,
    smoking: document.getElementById("smoking").value,
    drinking: document.getElementById("drinking").value,
    chronic: document.getElementById("chronic").value,
    ageGroup: document.getElementById("ageGroup").value,
    urgency: document.getElementById("urgency").value
  };

  try {
    const res = await fetch("/api/save_organ", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (res.ok && data.status === "success") {
      alert("✔ Organ data saved to Firebase");
    } else {
      alert("❌ Save failed: " + (data.message || "Unknown error"));
    }
  } catch (e) {
    console.error(e);
    alert("❌ Network error when saving");
  }
}

// Attach this function to Save button
document.addEventListener("DOMContentLoaded", () => {
  const saveBtn = document.getElementById("saveBtn");
  saveBtn.addEventListener("click", saveEntryToServer);
});
