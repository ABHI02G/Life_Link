// blood.js - fetches /api/get_blood and renders results + map
document.addEventListener("DOMContentLoaded", function () {
  const bloodForm = document.getElementById("bloodForm");
  const bloodGroupInput = document.getElementById("bloodGroup");
  const resultsBody = document.getElementById("resultsBody");
  const resultsCount = document.getElementById("resultsCount");
  const mapFrame = document.getElementById("mapFrame");
  const mapDescription = document.getElementById("mapDescription");

  function updateMap(mapQuery, hospitalName) {
    if (!mapQuery) {
      mapFrame.src = "https://www.google.com/maps?q=blood+bank+near+me&output=embed";
      mapDescription.textContent = "Showing blood banks near you.";
      return;
    }
    const encoded = encodeURIComponent(mapQuery);
    mapFrame.src = "https://www.google.com/maps?q=" + encoded + "&output=embed";
    mapDescription.textContent = "Map centered on: " + hospitalName + " (" + mapQuery + ")";
  }

  function renderResults(results) {
    resultsBody.innerHTML = "";
    if (!results || results.length === 0) {
      resultsBody.innerHTML = '<tr><td colspan="6">No hospitals found for this blood group.</td></tr>';
      resultsCount.textContent = "0 hospitals found";
      updateMap(null, null);
      return;
    }

    results.forEach(item => {
      const mapQuery = item.mapQuery || (item.hospitalName + " " + item.address);
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${item.bloodType}</td>
        <td>${item.hospitalName}</td>
        <td><strong>${item.quantity}</strong> ml</td>
        <td>${item.phone || "N/A"}</td>
        <td>${item.address || ""}</td>
        <td><button type="button" class="btn ghost btn-map" data-map="${mapQuery.replace(/"/g,"&quot;")}" data-hospital="${(item.hospitalName||"").replace(/"/g,"&quot;")}">View</button></td>
      `;
      resultsBody.appendChild(tr);
    });

    resultsCount.textContent = `${results.length} hospital${results.length>1?"s":""} found`;

    // attach buttons
    resultsBody.querySelectorAll(".btn-map").forEach(btn => {
      btn.addEventListener("click", function () {
        const mq = this.getAttribute("data-map");
        const hn = this.getAttribute("data-hospital");
        updateMap(mq, hn);
      });
    });

    // center map on first
    updateMap(results[0].mapQuery || (results[0].hospitalName + " " + results[0].address), results[0].hospitalName);
  }

  async function fetchBlood(group) {
    const url = `/api/get_blood?blood=${encodeURIComponent(group)}`;
    try {
      const res = await fetch(url);
      const data = await res.json();
      if (res.ok && data.blood_results) {
        renderResults(data.blood_results);
      } else {
        renderResults([]);
      }
    } catch (e) {
      console.error(e);
      renderResults([]);
    }
  }

  bloodForm.addEventListener("submit", function (e) {
    e.preventDefault();
    fetchBlood(bloodGroupInput.value);
  });

  // initial load
  fetchBlood(bloodGroupInput.value);
});
