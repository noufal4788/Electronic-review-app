function toggleDetails(button) {
    const moreDetails = button.nextElementSibling;
    
    if (moreDetails.style.display === "none" || moreDetails.style.display === "") {
      moreDetails.style.display = "block";
      button.innerHTML = '<i class="fa-solid fa-cart-shopping"></i> Show Less';
    } else {
      moreDetails.style.display = "none";
      button.innerHTML = '<i class="fa-solid fa-cart-shopping"></i> Show More';
    }
  }