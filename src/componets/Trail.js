import React, { useState, useEffect } from "react";

function Trail() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/api/data")
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.log("Error:", error));
  }, []);

  return (
    <div>
      {data ? (
        <div>
          <h1>{data.message}</h1>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default Trail;
