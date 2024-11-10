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

// Image Modal
function openModal(imgSrc) {
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImg");
    modalImg.src = imgSrc;
    modal.style.display = "block";
}

function closeModal() {
    const modal = document.getElementById("imageModal");
    modal.style.display = "none";
}
