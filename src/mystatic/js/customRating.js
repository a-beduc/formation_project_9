/**
 * Script to highlight star elements based on a user-selected rating
 * and synchronize that selection with a hidden form input.
 */
document.addEventListener("DOMContentLoaded", () => {
    const ratingInput = document.querySelector(".formReview__hidden");
    const stars = document.getElementsByClassName("formReview__stars__elem");
    const starContainer = document.querySelector(".formReview__stars");

    const starsArray = Array.from(stars);
    starsArray.forEach((star, i) => {
        star.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                gfg(i);
            }
        })
        star.addEventListener("click", (event) => {
            gfg(i);
        })
    })

    /**
     * Highlights the stars from index up to index n (included)
     * Updates the hidden rating input to the selected value of n.
     * @param n - integer
     */
    window.gfg = function(n) {
        removeStars();
        for (let i = 0; i < n+1; i++) {
            stars[i].classList.add("checked");
        }
        ratingInput.value = n;
    }

    /**
     * Removes the highlight of all the stars.
     */
    function removeStars() {
        let i = 1;
        while (i < 6) {
            stars[i].classList.remove("checked");
            i++
        }
        ratingInput.value = 0;
    }

    // Read the initial rating of a ticket if it exists and color the corresponding stars,
    // used when modifying a Review.
    let reviewRating = parseInt(starContainer.getAttribute("data-rating"), 10);
    gfg(reviewRating);
})