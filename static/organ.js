// ----------------------------
// Firebase Initialization
// ----------------------------
const firebaseConfig = {
  apiKey: "AIzaSyDSA49V396sFFFtKymJBc78hz7kc9zBCVg",
  authDomain: "organdatabase-9023e.firebaseapp.com",
  projectId: "organdatabase-9023e",
  storageBucket: "organdatabase-9023e.firebasestorage.app",
  messagingSenderId: "591330653454",
  appId: "1:591330653454:web:51dd1b79476d4f5f39935f",
  measurementId: "G-N4MQB3675S"
};

firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

// SEARCH & RENDER ORGAN RESULTS
async function renderResults(group, organ) {
  const resultsBody = document.getElementById("resultsBody");
  const resultsCount = document.getElementById("resultsCount");

  resultsBody.innerHTML = "";

  const snapshot = await db
    .collection("organs")
    .where("bloodGroup", "==", group)
    .where("organ", "==", organ)
    .get();

  if (snapshot.empty) {
    resultsBody.innerHTML =
      `<tr><td colspan="6">No records found.</td></tr>`;
    resultsCount.textContent = "0 hospitals found";
    updateMap(null, null);
    return;
  }

  let first = null;

  snapshot.forEach((doc, index) => {
    const data = doc.data();
    if (index === 0) first = data;

    const row = `
      <tr>
        <td>${data.bloodGroup}</td>
        <td>${data.organLabel || data.organ}</td>
        <td>${data.hospital}</td>
        <td>${data.phone}</td>
        <td>${data.address}</td>
        <td><button class="btn ghost btn-map"
          data-map="${data.mapQuery}"
          data-hospital="${data.hospital}">
          View
        </button></td>
      </tr>
    `;
    resultsBody.innerHTML += row;
  });

  resultsCount.textContent = snapshot.size + " results found";

  document.querySelectorAll(".btn-map").forEach(btn => {
    btn.addEventListener("click", () => {
      updateMap(btn.dataset.map, btn.dataset.hospital);
    });
  });

  if (first) {
    updateMap(first.mapQuery, first.hospital);
  }
}
document.addEventListener("DOMContentLoaded", function () {
  const organForm = document.getElementById("organForm");
  const bloodSelect = document.getElementById("organBloodGroup");
  const organSelect = document.getElementById("organType");
  const resultsBody = document.getElementById("organResultsBody");
  const resultsCount = document.getElementById("organResultsCount");
  const mapFrame = document.getElementById("organMapFrame");
  const mapDescription = document.getElementById("organMapDescription");

  function updateMap(mapQuery, hospitalName) {
    if (!mapQuery) {
      mapFrame.src = "https://www.google.com/maps?q=organ+transplant+hospital+near+me&output=embed";
      mapDescription.textContent = "No precise location selected. Showing transplant hospitals near you.";
      return;
    }
    const encoded = encodeURIComponent(mapQuery);
    mapFrame.src = "https://www.google.com/maps?q=" + encoded + "&output=embed";
    mapDescription.textContent = "Map centered on: " + hospitalName + " (" + mapQuery + ")";
  }

  function renderResults(results) {
    resultsBody.innerHTML = "";
    if (!results || results.length === 0) {
      resultsBody.innerHTML = '<tr><td colspan="6">No hospitals found for this selection.</td></tr>';
      resultsCount.textContent = "0 hospitals found";
      updateMap(null, null);
      return;
    }

    results.forEach((item) => {
      const mapQuery = item.hospitalName + " " + (item.address || "");
      const tr = document.createElement("tr");
      tr.innerHTML =
        "<td>" + (item.blood || "") + "</td>" +
        "<td>" + (Array.isArray(item.organs) ? item.organs.join(", ") : "") + "</td>" +
        "<td>" + (item.hospitalName || "") + "</td>" +
        "<td><span>" + (item.phone || "N/A") + "</span></td>" +
        "<td>" + (item.address || "") + "</td>" +
        '<td><button type="button" class="btn ghost btn-map" data-map="' +
        mapQuery.replace(/"/g, "&quot;") +
        '" data-hospital="' +
        (item.hospitalName || "").replace(/"/g, "&quot;") +
        '">View</button></td>';

      resultsBody.appendChild(tr);
    });

    resultsCount.textContent = results.length + (results.length > 1 ? " hospitals found" : " hospital found");

    const mapButtons = resultsBody.querySelectorAll(".btn-map");
    mapButtons.forEach((btn) => {
      btn.addEventListener("click", function () {
        const mq = this.getAttribute("data-map");
        const hn = this.getAttribute("data-hospital");
        updateMap(mq, hn);
      });
    });

    // center on first
    const first = results[0];
    if (first) {
      updateMap(first.hospitalName + " " + (first.address || ""), first.hospitalName);
    }
  }

  async function fetchOrganResults(group, organ) {
    // normalize organ same way hospitals saved
    const organKey = organ.toLowerCase();
    const url = `/api/get_organs?organ=${encodeURIComponent(organKey)}&blood=${encodeURIComponent(group)}`;
    try {
      const res = await fetch(url);
      const data = await res.json();
      if (res.ok && data.organ_results) {
        renderResults(data.organ_results);
      } else {
        console.error("Fetch error", data);
        renderResults([]);
      }
    } catch (e) {
      console.error("Network error", e);
      renderResults([]);
    }
  }

  organForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const group = bloodSelect.value;
    const organ = organSelect.value;
    fetchOrganResults(group, organ);
  });

  // initial load
  fetchOrganResults(bloodSelect.value, organSelect.value);
});
