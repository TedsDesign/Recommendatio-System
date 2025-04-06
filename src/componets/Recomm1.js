import "./cards.css";
function Recomm1({ data }) {
  if (!data) return <div>No Profile Found</div>;

  return (
    <div className="profile-card">
      <h2 className="heading">
        Hyper-Personalized Product Recommendations System{" "}
      </h2>
      <p className="personal-data">{data}</p>
    </div>
  );
}

export default Recomm1;
