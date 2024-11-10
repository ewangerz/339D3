// Scroll-to-Top Button
window.onscroll = function () { toggleScrollTopButton(); };

function toggleScrollTopButton() {
    const scrollTopBtn = document.getElementById("scrollTopBtn");
    if (window.pageYOffset > 200) {
        scrollTopBtn.style.display = "block";
    } else {
        scrollTopBtn.style.display = "none";
    }
}

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: "smooth" });
}

// Toggle Collapsible Sections
function toggleSection(button, sectionId) {
    const content = document.getElementById(sectionId).querySelector(".collapsible-content");
    if (content.style.display === "none") {
        content.style.display = "block";
        button.innerText = "Collapse";
    } else {
        content.style.display = "none";
        button.innerText = "Expand";
    }
}

// JavaScript to handle broken images by replacing them with a placeholder
function handleBrokenImages() {
    const images = document.querySelectorAll('.athlete img');
    images.forEach(img => {
        img.onerror = function () {
            this.onerror = null; // Prevent infinite loop if placeholder also fails
            this.src = '../images/placeholder.png'; // Path to your placeholder image
            this.alt = 'Placeholder image';
        };
    });
}

window.onload = handleBrokenImages; // Run on page load

