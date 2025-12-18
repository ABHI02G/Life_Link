// =============================
// HOSPITAL APPOINTMENT SYSTEM
// =============================

// Firebase init for hospital appointment database
const hospitalApp = firebase.initializeApp(appointmentConfig, "hospitalAppointments");
const hospitalDB = firebase.database(hospitalApp);

// UID injected by Flask (happointments.html)
const HOSPITAL_UID = window.HOSPITAL_UID;

// DOM
const form = document.getElementById("form");
const tbody = document.querySelector("#table tbody");

// Load appointments
function loadHospitalAppointments() {
    hospitalDB.ref("hospital_appointments/" + HOSPITAL_UID).on("value", snap => {
        const data = snap.val() || {};
        renderHospitalTable(data);
    });
}

// Render table rows
function renderHospitalTable(data) {
    tbody.innerHTML = "";
    const keys = Object.keys(data);

    if (keys.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="muted">No appointments found</td></tr>`;
        return;
    }

    keys.forEach((id, index) => {
        const a = data[id];

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${index + 1}</td>
            <td>${a.patient || ""}</td>
            <td>${a.phone || ""}</td>
            <td>${a.doctor || ""}</td>
            <td>${a.department || ""}</td>
            <td>${a.date || ""} ${a.time || ""}</td>
            <td>${a.notes || ""}</td>
            <td>
                <button class="btn ghost" onclick="deleteHospitalAppt('${id}')">Delete</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Delete appointment
window.deleteHospitalAppt = function (id) {
    hospitalDB.ref("hospital_appointments/" + HOSPITAL_UID + "/" + id).remove();
};

// Save appointment
form.addEventListener("submit", e => {
    e.preventDefault();

    const appt = {
        hospitalName: document.getElementById("h_name").value,
        patient: document.getElementById("patient").value,
        phone: document.getElementById("phone").value,
        doctor: document.getElementById("doctor").value,
        department: document.getElementById("department").value,
        date: document.getElementById("date").value,
        time: document.getElementById("time").value,
        notes: document.getElementById("notes").value,
        createdAt: Date.now()
    };

    hospitalDB.ref("hospital_appointments/" + HOSPITAL_UID).push(appt);
    form.reset();
});

// Start
loadHospitalAppointments();
