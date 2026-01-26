function toggleSidebar() {
    document.getElementById("sidebar").classList.toggle("show");
}

function toggleProfile() {
    const menu = document.getElementById("profileMenu");
    menu.style.display = menu.style.display === "block" ? "none" : "block";
}

function toggleDropdown(e) {
    e.stopPropagation();
    const dropdown = e.target.nextElementSibling;
    dropdown.style.display =
        dropdown.style.display === "block" ? "none" : "block";
}

function resetFilters() {
    document.querySelectorAll(".dropdown-content input").forEach(cb => {
        cb.checked = false;
    });
    alert("Filters reset (connect logic here)");
}

/* Optional demo data */
const sampleData = [
    [1, "ITM001", "Laptop", "Store A", 3, 80000, 6, 240000, 1800],
    [2, "ITM002", "Mouse", "Store B", 10, 1200, 9, 12000, 90]
];

const tbody = document.querySelector("#itemTable tbody");
const cardContainer = document.getElementById("cardContainer");

sampleData.forEach(row => {
    const tr = document.createElement("tr");
    row.forEach((cell, i) => {
        const td = document.createElement("td");
        td.innerText = cell;
        tr.appendChild(td);
    });
    tbody.appendChild(tr);

    const card = document.createElement("div");
    card.className = "inventory-card";
    const labels = ["SN","Code","Category","Location","Quantity","NPR Rate","USD Rate","Total NPR","Total USD"];
    row.forEach((cell, i) => {
        const div = document.createElement("div");
        div.innerHTML = `<strong>${labels[i]}:</strong> ${cell}`;
        card.appendChild(div);
    });
    cardContainer.appendChild(card);
});
