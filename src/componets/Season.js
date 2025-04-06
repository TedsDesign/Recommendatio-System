import React from "react";
import "./cards.css";

function Season({ data, onInterestChange, interestedProducts }) {
  const handleInterestClick = (productId) => {
    // Check if the product is already in the array
    if (!interestedProducts.includes(productId)) {
      onInterestChange([...interestedProducts, productId]);
    } else {
      // Remove if clicked again
      onInterestChange(interestedProducts.filter((id) => id !== productId));
    }
    console.log("Interested Products:", interestedProducts);
  };

  return (
    <>
      <h2 className="head-line">Product Recommendation Based on Season</h2>
      <div className="product-container">
        {data.map((product) => (
          <div key={product.Product_ID} className="product-card">
            <div className="product-header">
              <h3>{product.Product_ID}</h3>
              <div className="product-category">
                {product.Subcategory}, {product.Category}
              </div>
            </div>
            <div className="product-details">
              <div className="brand">{product.Brand}</div>
              <div className="Rating">Rating : {product.Product_Rating}</div>
            </div>
            <button className="buy-button">Buy Now @ Rs.{product.Price}</button>
            <button
              className={`interest-button ${
                interestedProducts.includes(product.Product_ID)
                  ? "interested"
                  : ""
              }`}
              onClick={() => handleInterestClick(product.Product_ID)}
            >
              {interestedProducts.includes(product.Product_ID)
                ? "Interested ✓"
                : "Interested"}
            </button>
          </div>
        ))}
      </div>
    </>
  );
}

export default Season;
