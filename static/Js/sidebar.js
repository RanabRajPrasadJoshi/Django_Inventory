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