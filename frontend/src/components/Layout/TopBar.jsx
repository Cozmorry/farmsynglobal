// src/components/Layout/TopBar.jsx
import React, { useContext, useState } from "react";
import { UsersContext } from "../../context/UsersContext";

export default function TopBar() {
  const { user, currentFarm, selectFarm, logout } = useContext(UsersContext);
  const [showFarmMenu, setShowFarmMenu] = useState(false);

  const handleLogout = () => {
    logout();
  };

  const handleFarmSelect = (farm) => {
    selectFarm(farm);
    setShowFarmMenu(false);
  };

  return (
    <div className="top-bar">
      {/* Left: Notifications */}
      <div className="notifications">
        <span>🔔 3 New Alerts</span>
      </div>

      {/* Center: Farm selection */}
      <div className="farm-selector">
        <span onClick={() => setShowFarmMenu(!showFarmMenu)}>
          🌾 {currentFarm?.name || "Select Farm"} ▼
        </span>
        {showFarmMenu && user?.farms?.length > 1 && (
          <div className="farm-menu">
            {user.farms.map((farm) => (
              <div
                key={farm.id}
                className="farm-menu-item"
                onClick={() => handleFarmSelect(farm)}
              >
                {farm.name}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Right: User Info */}
      <div className="user-info">
        <span>{user?.username}</span>
        <button onClick={handleLogout} className="signout-btn">
          Sign Out
        </button>
      </div>
    </div>
  );
}
