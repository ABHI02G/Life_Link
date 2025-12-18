// =============================
// USER APPOINTMENT SYSTEM
// =============================

// Firebase init for user appointment database
const userApp = firebase.initializeApp(appointmentConfig, "userAppointments");
const userDB = firebase.database(userApp);

// UID injected from Flask (appointments.html)
const USER_UID = window.USER_UID;

// DOM elements
const form = document.getElementById("form");
const tbody = document.querySelector("#table tbody");

// Load appointments on page load
function loadUserAppointments() {
    userDB.ref("user_appointments/" + USER_UID).on("value", snap => {
        const data = snap.val() || {};
        renderUserTable(data);
    });
}

// Render table rows
function renderUserTable(data) {
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
                <button class="btn ghost" onclick="deleteUserAppt('${id}')">Delete</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Delete appointment
window.deleteUserAppt = function (id) {
    userDB.ref("user_appointments/" + USER_UID + "/" + id).remove();
};

// Save new appointment
form.addEventListener("submit", e => {
    e.preventDefault();

    const appt = {
        patient: document.getElementById("patient").value,
        phone: document.getElementById("phone").value,
        doctor: document.getElementById("doctor").value,
        department: document.getElementById("department").value,
        date: document.getElementById("date").value,
        time: document.getElementById("time").value,
        notes: document.getElementById("notes").value,
        createdAt: Date.now()
    };

    userDB.ref("user_appointments/" + USER_UID).push(appt);
    form.reset();
});

// Start loading
loadUserAppointments();
