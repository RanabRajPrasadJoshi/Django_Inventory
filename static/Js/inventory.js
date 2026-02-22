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




document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    const table = document.getElementById("itemTable");
    const rows = table.querySelectorAll("tbody tr");

    const totalQty = document.getElementById("totalQuantity");
    const totalMarket = document.getElementById("totalMarket");
    const totalCost = document.getElementById("totalCost");

    // ================= TOTALS =================
    function calculateTotals() {
        let qty = 0, mp = 0, cp = 0;

        rows.forEach(row => {
            if (row.style.display !== "none") {
                qty += parseFloat(row.cells[5].innerText) || 0;
                mp += parseFloat(row.cells[7].innerText) || 0;
                cp += parseFloat(row.cells[9].innerText) || 0;
            }
        });

        totalQty.innerText = qty;
        totalMarket.innerText = mp.toFixed(2);
        totalCost.innerText = cp.toFixed(2);
    }

    calculateTotals();

    // ================= SEARCH =================
    searchInput.addEventListener("keyup", function () {
        const value = this.value.toLowerCase();

        rows.forEach(row => {
            row.style.display = row.innerText.toLowerCase().includes(value)
                ? ""
                : "none";
        });

        calculateTotals();
    });

    // ================= FILTER =================
    document.querySelectorAll(".filter-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const col = btn.dataset.col;
            const val = prompt("Enter filter value:");

            if (!val) return;

            rows.forEach(row => {
                const cell = row.cells[col].innerText.toLowerCase();
                row.style.display = cell.includes(val.toLowerCase()) ? "" : "none";
            });

            calculateTotals();
        });
    });

    // ================= RESET =================
    window.resetFilters = function () {
        rows.forEach(row => row.style.display = "");
        searchInput.value = "";
        calculateTotals();
    };
});
