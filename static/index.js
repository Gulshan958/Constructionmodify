// Slider 
document.addEventListener("DOMContentLoaded", function () {
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');
    const progressBars = document.querySelectorAll('.progress-bar div');
    let slideInterval;

    function showSlide() {
        slides.forEach((slide, index) => {
            slide.style.opacity = index === currentSlide ? "1" : "0";
        });
        resetProgressBars();
        progressBars[currentSlide].style.width = "100%";
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide();
        resetInterval();
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlide();
        resetInterval();
    }

    function startSlideshow() {
        slideInterval = setInterval(nextSlide, 3000);
        resetProgressBars();
    }

    function resetInterval() {
        clearInterval(slideInterval);
        startSlideshow();
    }

    function resetProgressBars() {
        progressBars.forEach((bar, index) => {
            bar.style.width = "0%";
            if (index === currentSlide) {
                setTimeout(() => {
                    bar.style.width = "100%";
                }, 10);
            }
        });
    }

    document.querySelector(".btn-prev").addEventListener("click", prevSlide);
    document.querySelector(".btn-next").addEventListener("click", nextSlide);

    showSlide();
    startSlideshow();
});


// Drop Down
    document.addEventListener("DOMContentLoaded", function () {
    let dropdownBtn = document.querySelector(".dropdown-btn");
    let dropdownMenu = document.querySelector(".dropdown-menu");

    if (dropdownBtn && dropdownMenu) {
        dropdownBtn.addEventListener("click", function (event) {
            dropdownMenu.classList.toggle("show-menu");
            event.stopPropagation(); // Prevent closing when clicking button
        });

        // Close dropdown when clicking outside
        document.addEventListener("click", function (event) {
            if (!dropdownBtn.contains(event.target) && !dropdownMenu.contains(event.target)) {
                dropdownMenu.classList.remove("show-menu");
            }
        });
    }
});



// Search Input 
document.addEventListener("DOMContentLoaded", function () {
    let productNotFound = "{{ product_not_found }}";
    if (productNotFound === "True") {
        alert("Product not found!");
    }
});

function searchProduct() {
    let searchValue = document.getElementById("searchInput").value.trim();
    if (searchValue === "") {
        alert("Please enter a product name to search!");
        return;
    }
    window.location.href = `/shop?search=${encodeURIComponent(searchValue)}`;
}

