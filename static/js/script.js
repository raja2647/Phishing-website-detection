document.addEventListener("DOMContentLoaded", function () {
    const main = document.querySelector(".main");
    const sections = document.querySelectorAll(".section");
    const navLinks = document.querySelectorAll(".items a");

    function updateActiveLink() {
        sections.forEach((section, i) => {
            let isActive = false;

            // For horizontal scrolling (desktop view)
            if (main.scrollWidth > main.clientWidth) {
                const sectionLeft = section.offsetLeft;
                const sectionWidth = section.offsetWidth;
                const scrollLeft = main.scrollLeft;

                if (scrollLeft >= sectionLeft - sectionWidth / 2 && scrollLeft < sectionLeft + sectionWidth / 2) {
                    isActive = true;
                }
            }
            // For vertical scrolling (mobile view)
            else {
                const rect = section.getBoundingClientRect();
                if (rect.top >= 0 && rect.top < window.innerHeight / 2) {
                    isActive = true;
                }
            }

            // Apply active class
            if (isActive) {
                navLinks.forEach(link => link.classList.remove("active"));
                navLinks[i]?.classList.add("active");
            }
        });
    }

    updateActiveLink();

    main.addEventListener("scroll", updateActiveLink);
    window.addEventListener("scroll", updateActiveLink); // For mobile view where page scrolls vertically
});

document.addEventListener("DOMContentLoaded", function () {
    const input = document.querySelector("input[type='text']");
    const resultBox = document.createElement('div');
    resultBox.classList.add("suggestions");
    input.parentNode.appendChild(resultBox);

    input.addEventListener("input", function () {
        const query = input.value;
        if (!query) {
            resultBox.innerHTML = '';
            return;
        }
        fetch(`/search?q=${query}`)
            .then(response => response.json())
            .then(data => {
                resultBox.innerHTML = '';
                data.forEach(item => {
                    const div = document.createElement('div');
                    div.classList.add("suggestion");
                    div.textContent = item.url;
                    div.onclick = () => {
                        window.location.href = `/report/${item.id}`;
                    };
                    resultBox.appendChild(div);
                });
            });
    });
});
