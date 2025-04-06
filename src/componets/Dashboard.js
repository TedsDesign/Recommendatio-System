import { useState, useEffect } from "react";
import Recomm1 from "./Recomm1";
import LastPurchase from "./LastPurchase";
import BrowsingHistory from "./BrowsingHistory";
import Season from "./Season";
import BasedOnInterest from "./BasedOnInterest";
import "./Dashboard.css";

function Dashboard({ customerID }) {
  const [recomm1, setRecomm1Data] = useState(null);
  const [lP, setLP] = useState(null);
  const [bH, setBH] = useState(null);
  const [sD, setSD] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [interestedProducts, setInterestedProducts] = useState([]);
  const [recommendedProducts, setRecommendedProducts] = useState(null);

  const handleProcessInterested = async () => {
    try {
      const response = await fetch(
        "http://localhost:5000/api/recommendInterestedData",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ interested_products: interestedProducts }),
        }
      );

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const Interesteddata = await response.json();
      setRecommendedProducts(Interesteddata);
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to get recommendations");
    } finally {
    }
  };

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        setLoading(true);

        // Fetch all data in parallel
        const [recommRes, browiHistRes, lastPurRes, seasonRes] =
          await Promise.all([
            fetch(`http://127.0.0.1:5000/api/user/Recomm1/${customerID}`),
            fetch(
              `http://127.0.0.1:5000/api/user/BrowsingHistory/${customerID}`,
              {
                headers: {
                  "Content-type": "application-json",
                },
              }
            ),
            fetch(`http://127.0.0.1:5000/api/user/LastPurchase/${customerID}`, {
              headers: {
                "Content-type": "application-json",
              },
            }),
            fetch(`http://127.0.0.1:5000/api/user/Season/${customerID}`, {
              headers: {
                "Content-type": "application-json",
              },
            }),
          ]);

        const [
          Recomm1Data,
          BrowsingHitsoryData,
          LastPurcahaseData,
          SeasonData,
        ] = await Promise.all([
          recommRes.json(),
          lastPurRes.json(),
          browiHistRes.json(),
          seasonRes.json(),
        ]);

        if (!recommRes.ok)
          throw new Error(Recomm1Data.error || "Recommendation Data failed");
        if (!lastPurRes.ok)
          throw new Error(lastPurRes.error || "Recommendation Data failed");

        setRecomm1Data(Recomm1Data);
        setLP(LastPurcahaseData);
        setBH(BrowsingHitsoryData);
        setSD(SeasonData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (customerID) fetchUserData();
  }, [customerID]);

  if (loading) return <div>Loading user data...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="dashboard">
      <Recomm1 data={recomm1} />
      <div className="dashboard-grid">
        <LastPurchase
          data={lP}
          interestedProducts={interestedProducts}
          onInterestChange={setInterestedProducts}
        />
        <BrowsingHistory
          data={bH}
          interestedProducts={interestedProducts}
          onInterestChange={setInterestedProducts}
        ></BrowsingHistory>
        <Season
          data={sD}
          interestedProducts={interestedProducts}
          onInterestChange={setInterestedProducts}
        />
        <div className="interested-products-summary">
          {/* <h3>Your Interested Products ({interestedProducts.length})</h3>
          <ul>
            {interestedProducts.map((productId) => (
              <li key={productId}>{productId}</li>
            ))}
          </ul> */}
          {
            <button className="action-button" onClick={handleProcessInterested}>
              Get Products Based on Your Interest
            </button>
          }
        </div>
        {recommendedProducts && (
          <BasedOnInterest
            data={recommendedProducts}
            interestedProducts={interestedProducts}
            onInterestChange={setInterestedProducts}
          />
        )}
      </div>
    </div>
  );
}

export default Dashboard;
