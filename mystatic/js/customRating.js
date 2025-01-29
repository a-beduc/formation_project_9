document.addEventListener("DOMContentLoaded", () => {
    const ratingInput = document.querySelector(".formReview__hidden");
    const stars = document.getElementsByClassName("formReview__stars__elem");
    const starContainer = document.querySelector(".formReview__stars");

    window.gfg = function(n) {
        removeStars();
        for (let i = 0; i < n+1; i++) {
            stars[i].classList.add("checked");
        }
        ratingInput.value = n;
    }

    function removeStars() {
        let i = 1;
        while (i < 6) {
            stars[i].classList.remove("checked");
            i++
        }
        ratingInput.value = 0;
    }

    let reviewRating = parseInt(starContainer.getAttribute("data-rating"), 10);
    gfg(reviewRating);
})