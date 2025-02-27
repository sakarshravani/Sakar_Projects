import React, { useEffect, useState } from "react";  // Import React and hooks
import "./SPMReport.css"; // Import CSS file for styling
import sakarLogo from './sakar.png';  // Adjust the path according to the location of the image
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";  // Import axios for API calls

const SPMReport = () => {
  const location = useLocation();
  const passedData = location.state || {};
  const formData = passedData.formData || {};
  const file = passedData.file; // The uploaded Excel file
  
  const navigate = useNavigate();
  
  const [totalDistance, setTotalDistance] = useState("N/A");
  const [mpsAchieved, setMpsAchieved] = useState("N/A");
  const [nearMpsDistance, setNearMpsDistance] = useState("N/A");
  
  const [totalJourneyDistance, setTotalJourneyDistance] = useState("N/A");
  const [totalJourneyTime, setTotalJourneyTime] = useState("N/A");
  const [avgSpeed, setAvgSpeed] = useState("N/A");
  const [avgRunSpeed, setAvgRunSpeed] = useState("N/A");
  const [bftTime, setBftTime] = useState("N/A");
  const [bftSpeedDrop, setBftSpeedDrop] = useState("N/A");
  const [bptTime, setBptTime] = useState("N/A");
  const [bptSpeedDrop, setBptSpeedDrop] = useState("N/A");
  
  const [noOfStops, setNoOfStops] = useState("N/A");
  
  const [startTime, setStartTime] = useState("N/A");
  const [endTime, setEndTime] = useState("N/A");
  
  const [menuOpen, setMenuOpen] = useState(false);
  
  // Toggle the menu visibility
  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };
  

  useEffect(() => {
    const fetchCalculatedData = async () => {
      if (file) {
        try {
          const fd = new FormData();
          fd.append("file", file);
          const response = await axios.post("http://localhost:8000/api/total_distance", fd, {
            headers: { "Content-Type": "multipart/form-data" },
          });
          console.log("Total Distance API Response:", response.data);
          setTotalDistance(response.data.total_mps_distance);
          setMpsAchieved(response.data.mps_achieved);
          setNearMpsDistance(response.data.total_distance_near_mps);
          
          setTotalJourneyDistance(response.data.total_journey_distance);
          setTotalJourneyTime(response.data.total_journey_time);
          setAvgSpeed(response.data.avg_speed);
          setAvgRunSpeed(response.data.avg_run_speed);
          setBftTime(response.data.bft_time);
          setBftSpeedDrop(response.data.bft_speed_drop);
          setBptTime(response.data.bpt_time);
          setBptSpeedDrop(response.data.bpt_speed_drop);
          setNoOfStops(response.data.no_of_stops);
          setStartTime(response.data.start_time);
          setEndTime(response.data.end_time);
        } catch (error) {
          console.error("Error fetching calculated data:", error);
          setTotalDistance("Error");
          setMpsAchieved("Error");
          setNearMpsDistance("Error");
          
          setTotalJourneyDistance("Error");
          setTotalJourneyTime("Error");
          setAvgSpeed("Error");
          setAvgRunSpeed("Error");
          setBftTime("Error");
          setBftSpeedDrop("Error");
          setBptTime("Error");
          setBptSpeedDrop("Error");
          setStartTime("Error");
          setEndTime("Error");
          setNoOfStops("Error");
        }
      }
    };

    fetchCalculatedData();
  }, [file]);
  
  return (
    <div className="spm-report-container">
      {/* Header Bar */}
      <div className="header-bar">
        <div
          className="logo-container"
          onClick={() => navigate("/")}
          style={{ cursor: "pointer" }}
        >
          <img src={sakarLogo} alt="Sakar Logo" className="sakar-logo" />
        </div>
        <div className="cvvrs-text">CVVRS and SPM Analysis</div>
      </div>
      {/* Menu Bar */}
      <div className={`menubar ${menuOpen ? 'open' : 'closed'}`}>
        {/* Inside Menu: Close Button ("×") */}
        {menuOpen && (
          <button className="menu-button inside" onClick={toggleMenu}>
            ×
          </button>
        )}

        <ul className="menu-list">
          <li><a href="/">Home</a></li>
          <li><a href="/analytics">Analytics</a></li>
          <li><a href="/setting">Setting</a></li>
          <li><a href="/about-us">About Us</a></li>
          <li><a href="/contact-us">Contact Us</a></li>
        </ul>
      </div>

      {/* Outside Menu: Open Button ("☰") */}
      {!menuOpen && (
        <button className="menu-button outside" onClick={toggleMenu}>
          ☰
        </button>
      )}
      <h2>Speedometer Data Analysis</h2>

      {/* First Table (4 Columns, 6 Rows) */}
      <table className="spm-table">
        <tbody>
          <tr>
            <td>Train Number:</td>
            <td>{formData.trainNo || "N/A"}</td>
            <td>Loco Number:</td>
            <td>{formData.locoNo || "N/A"}</td>
          </tr>
          <tr>
            <td>Journey Date:</td>
            <td>{formData.inspectionDate || "N/A"}</td>
            <td>Inspector Name:</td>
            <td>{formData.inspectorName || "N/A"}</td>
          </tr>
          <tr>
            <td>Report ID:</td>
            <td>{formData.reportID || "N/A"}</td>
            <td>Report Date:</td>
            <td>{formData.todayDate || "N/A"}</td>
          </tr>
          <tr>
            <td>MPS:</td>
            <td>{mpsAchieved || "N/A"}</td>
            
            <td>No. of Stops:</td>
            <td>{noOfStops !== null && noOfStops !== undefined ? noOfStops : "N/A"}</td>
            <td colSpan="2"></td>
          </tr>
          <tr>
            <td>LP Name:</td>
            <td>{formData.lpName || "None"}</td>
            <td>ALP Name:</td>
            <td>{formData.alpName || "None"}</td>
          </tr>
          <tr>
            <td>Start Time of Analysis:</td>
             <td>{startTime || "N/A"}</td>
            <td>End Time of Analysis:</td>
            <td>{endTime || "N/A"}</td>
          </tr>
        </tbody>
      </table>


      {/* Second Table */}
<table className="spm-table">
  <tbody>
    <tr>
      <td>MPS Achieved:</td>
       <td colSpan="3">{mpsAchieved || "N/A"}</td>
    </tr>
    <tr>
  <td>Total Distance at Achieved MPS:</td>
  <td colSpan="3">{totalDistance !== null && totalDistance !== undefined ? totalDistance : "0.0"}</td>

</tr>
    <tr>
      <td>Distance at near Achieved MPS(95%):</td>
         <td colSpan="3">{nearMpsDistance || "N/A"}</td>
    </tr>
    
    <tr>
      <td>Total Journey Distance:</td>
     <td colSpan="3">{totalJourneyDistance || "0.0"}</td>
    </tr>
    <tr>
      <td>Total Journey Time:</td>
     <td colSpan="3">{totalJourneyTime || "0.001"}</td>
    </tr>
    <tr>
      <td>Average Speed: (Distance/time):</td>
      <td colSpan="3">{avgSpeed || "N/A"}</td>
    </tr>
    <tr>
      <td>Average Running Speed:</td>
      <td colSpan="3">{avgRunSpeed || "N/A"}</td>
    </tr>
    <tr>
      <td>Number of stops taken:</td>
      <td colSpan="3">
        <input type="text" className="spm-secondary-input" />
      </td>
    </tr>
    <tr>
      <td>Unscheduled Stops:</td>
      <td colSpan="3">
        <input type="text" className="spm-secondary-input" />
      </td>
    </tr>
  

          {/* Last 2 rows with meaningful names */}
          <tr>
            <td>BFT Time:</td>
            <td>{bftTime || "N/A"}</td>
            <td>Speed Drop:</td>
             <td>{bftSpeedDrop || "N/A"}</td>
          </tr>
          <tr>
            <td>BPT Time:</td>
            <td>{bptTime || "N/A"}</td>
            <td>Speed Drop:</td>
            <td>{bptSpeedDrop || "N/A"}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default SPMReport;

