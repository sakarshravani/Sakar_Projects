
import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import sakarLogo from "./sakar.png"; // Ensure the logo is located in the src folder.
import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom"; // Import Router and Routes
import SectionalMPS from './SectionalMPS'; // Import the SectionalMPS component
import SpmReport from "./SPMReport";
import CvvrsReport from "./cvvrsreport";
import SpmGraph from "./spmgraph";
import Header from "./header";
import Home from "./page/home";
import Analytics from "./page/analytics";
import Setting from "./page/setting";
import About from "./page/about";
import Contact from "./page/contact";
import * as XLSX from "xlsx";

const API_URL = "http://127.0.0.1:45448/upload_video/"; // Backend API URL


// --- Helper function to clean Excel file data ---
export const cleanExcelData = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const binaryStr = e.target.result;
        const workbook = XLSX.read(binaryStr, { type: "binary" });
        const sheetName = workbook.SheetNames[0];
        const sheet = workbook.Sheets[sheetName];
        // Read as an array of arrays
        const allRows = XLSX.utils.sheet_to_json(sheet, { header: 1 });
        if (allRows.length === 0) {
          resolve([]);
          return;
        }
        
        // 2) Define skip patterns for lines we want to remove
        //    (Adjust or add more as needed)
        const skipPatterns = [
          "laxven speed recorder file",
          "data displayed",
          "mem freez",
          "poweron",
          // etc...
        ];
        
        // Filter out rows that contain any of the skip patterns
        const filteredRows = allRows.filter((row) => {
          const rowString = row.join(" ").toLowerCase();
          if (!rowString.trim()) return false;
          return !skipPatterns.some((pat) => rowString.includes(pat));
        });

        if (filteredRows.length === 0) {
          resolve([]);
          return;
        }
        
        
        
        
        // 5) Mapping from your desired keys -> possible header name variations
        const headerMapping = {
          Date: ["date", "journey date", "date of journey"],
          Time: ["time", "timestamp"],
          Distance: ["distance", "distance (km)", "km"],
          Speed: ["speed", "speed(km/h)", "speed (km/h)"]
        };
        
         let headerRowIndex = -1;
        for (let i = 0; i < filteredRows.length; i++) {
          const rowString = filteredRows[i].join(" ").toLowerCase();
          // Check that for each required key, at least one possible name appears in the row
          const hasAll = Object.values(headerMapping).every((names) =>
            names.some((name) => rowString.includes(name))
          );
          if (hasAll) {
            headerRowIndex = i;
            break;
          }
        }


       if (headerRowIndex === -1) {
          reject("No valid header row found containing Date, Time, Distance, and Speed.");
          return;
        }
        
       // Use the found header row
        const headers = filteredRows[headerRowIndex].map((cell) =>
          cell.toString().trim().toLowerCase()
        );
        console.log("Final Headers:", headers);
        
        // Helper to find the index of a header for a required field
        const findHeaderIndex = (field) => {
          const possible = headerMapping[field];
          for (let i = 0; i < headers.length; i++) {
            if (possible.some((p) => headers[i].includes(p))) {
              return i;
            }
          }
          return -1;
        };

       const dateIndex = findHeaderIndex("Date");
        const timeIndex = findHeaderIndex("Time");
        const distanceIndex = findHeaderIndex("Distance");
        const speedIndex = findHeaderIndex("Speed");
        
        if (dateIndex === -1 || timeIndex === -1 || distanceIndex === -1 || speedIndex === -1) {
          reject("Missing one or more required columns: Date, Time, Distance, Speed.");
          return;
        }
        
         // Map rows after the header row into objects
        const dataRows = filteredRows.slice(headerRowIndex + 1);
        const cleanedData = dataRows.map((row) => {
          const rawDate = row[dateIndex];
          const rawTime = row[timeIndex];
          const rawDistance = row[distanceIndex];
          const rawSpeed = row[speedIndex];
          
          // Convert numeric fields
          const distanceNum = parseFloat(rawDistance);
          const speedNum = parseFloat(rawSpeed);
          
          return {
            Date: rawDate ? rawDate.toString().trim() : "",
            Time: rawTime ? rawTime.toString().trim() : "",
            Distance: isNaN(distanceNum) ? null : distanceNum,
            Speed: isNaN(speedNum) ? null : speedNum
          };
        }).filter(item =>
          item.Date && item.Time && item.Distance !== null && item.Speed !== null
        );
        
        resolve(cleanedData);
      } catch (error) {
        reject(error);
      }
    };
    reader.onerror = (error) => reject(error);
    reader.readAsBinaryString(file);
  });
};


function App() {
  // State Variables
  const [trainNo, setTrainNo] = useState("");
  const [locoNo, setLocoNo] = useState(""); // Added Loco No. state
  const [inspectorName, setInspectorName] = useState("");
  const [inspectionDate, setInspectionDate] = useState("");
  const [video, setVideo] = useState(null);
  const [processedVideoURL, setProcessedVideoURL] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [reportID, setReportID] = useState("");
  const [selectedOption, setSelectedOption] = useState("");
  const [dropdownVisible, setDropdownVisible] = useState(false);
  
  const [goodsOption, setGoodsOption] = useState("");
  const [loadAmount, setLoadAmount] = useState("");
  
  const [lpName,setlpname] = useState("");
  const [lpDesignation,setlpdesignation] = useState("");
  const [alpName,setalpname] = useState("");
  const [alpDesignation,setalpdesignation] = useState("");
  const [file, setFile] = useState(null);
  const [cleanedRows, setCleanedRows] = useState([]);
  
  const [excelFile, setExcelFile] = useState(null);

  
  const [data, setData] = useState([]); // Ensure state is defined
  const [sectionMarkers, setSectionMarkers] = useState([]);

  const [todayDate] = useState(new Date().toISOString().split("T")[0]);
  

  const navigate = useNavigate();
  
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === "trainNo") setTrainNo(value);
    else if (name === "locoNo") setLocoNo(value);
    else if (name === "inspectorName") setInspectorName(value);
    else if (name === "inspectionDate") setInspectionDate(value);
    else if (name === "reportID")setReportID(value);
    else if (name === "lpName")setlpname(value);
    else if (name === "alpName")setalpname(value);
  };
  
   const handleFileUpload = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
    cleanExcelData(selectedFile)
      .then((cleanData) => {
        console.log("Cleaned Excel Data:", cleanData);
        // Optionally store cleanData if needed
      })
      .catch((error) => {
        console.error("Error cleaning Excel file:", error);
      });
  };


  
  const handleGenerateSpmReport = async () => {
    let noOfStops = "N/A";
    let mps = "N/A";
    let startTime = "N/A";
    let endTime = "N/A";
    if (file) {
      try {
        const result = await processExcelFile(file);
        noOfStops = result.stops;
        mps = result.mps;
        startTime = result.startTime;
        endTime = result.endTime;
      } catch (error) {
        console.error("Error processing Excel file:", error);
      }
    }
 
 const formData = {
            trainNo,
            locoNo,
            inspectorName,
            inspectionDate,
            reportID,
            todayDate,
            lpName,
            alpName,
            noOfStops,
            mps,
            startTime,
            endTime
        };
    navigate("/spm-report", { state: { formData, file } });
    };
   
    // Helper function to convert Excel time fraction to HH:MM:SS (if needed)
  const convertExcelTime = (excelTime) => {
    if (typeof excelTime === "number") {
      const totalSeconds = Math.round(excelTime * 24 * 3600);
      const hours = Math.floor(totalSeconds / 3600);
      const minutes = Math.floor((totalSeconds % 3600) / 60);
      const seconds = totalSeconds % 60;
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    return excelTime;
  };
    
    // Function to process the Excel file: count stops, compute MPS, and extract start/end times.
  const processExcelFile = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const binaryStr = e.target.result;
        const workbook = XLSX.read(binaryStr, { type: "binary" });
        const sheetName = workbook.SheetNames[0];
        const sheet = workbook.Sheets[sheetName];
        const jsonData = XLSX.utils.sheet_to_json(sheet);
        let stops = 0;
        let maxSpeed = 0;
        
        // Process each row for stops and MPS
        jsonData.forEach((row) => {
          const rawSpeed = row.Speed ?? row["Speed(km/h)"];
          if (rawSpeed !== undefined && rawSpeed !== null && rawSpeed !== "") {
            const speed = parseFloat(rawSpeed);
            if (speed === 0) stops++;
            if (speed > maxSpeed) maxSpeed = speed;
          }
        });
        
        // Extract times from the "Time" column.
        const times = jsonData
          .map((row) => row.Time)
          .filter((t) => t !== undefined && t !== null && t.toString().trim() !== "");
        
        // Convert the Excel time fraction to a proper HH:MM:SS string if needed.
        const startTime = times.length > 0 ? convertExcelTime(times[0]) : "N/A";
        const endTime = times.length > 0 ? convertExcelTime(times[times.length - 1]) : "N/A";
  
        resolve({ stops, mps: maxSpeed, startTime, endTime });
      } catch (error) {
        reject(error);
      }
    };
    reader.onerror = (error) => reject(error);
    reader.readAsBinaryString(file);
  });
};
  
    
  const handleRadioChange = (e) => {
     setSelectedOption(e.target.value);
    setGoodsOption(""); // Reset goods option when switching between "goods" and "chg"
    setLoadAmount("");  // Reset load amount when switching between "goods" and "chg"
  };
  
  const handleDropdownChange = (e) => {
    setGoodsOption(e.target.value); // Capture selected dropdown value
    setLoadAmount(""); // Reset load amount if dropdown value changes
  };
  
  const handleTrainNoChange = (e) => {
  // Allow only numbers (0-9)
  const value = e.target.value;
  if (/^\d*$/.test(value)) {
    setTrainNo(value); // Only update the state if the value is numeric
  }
};


  const handleLoadAmountChange = (e) => {
    setLoadAmount(e.target.value);
  };
  
  const [crewDetails, setCrewDetails] = useState({
    lpName: "",
    alpName: "",
    lpDesignation: "",
    alpDesignation: "",
    lpActivity: "",
    alpActivity: "",
    lpActivity2: "",
    alpActivity2: "",
    lpActivity3: "",
    alpActivity3: "",
    lpActivity4: "",
    alpActivity4: "",
    lpActivity5: "",
    alpActivity5: "",
    lpName2: "",
    alpName2: "",
    lpDesignation2: "",
    alpDesignation2: "",
    lpName3: "",
    alpName3: "",
    lpDesignation3: "",
    alpDesignation3: "",
    lpName4: "",
    alpName4: "",
    lpDesignation4: "",
    alpDesignation4: "",
  });
  
  

  const supportedFormats = ["video/mp4", "video/webm", "video/ogg"];
  
  const [checkbox1, setCheckbox1] = useState(false);
  const [checkbox2, setCheckbox2] = useState(false);
  
  // Handler functions for the checkboxes
  const handleCheckbox1Change = (e) => {
  setCheckbox1(e.target.checked);
};

  const handleCheckbox2Change = (e) => {
  setCheckbox2(e.target.checked);
};

 

  const handleGenerateCvvrsReport = () => {
  // Add logic to generate CVVRS report here
  navigate("/cvvrs-report");
};
  
  const handleGenerateSpmGraph = () => {
  if (excelFile) {
    navigate("/spm-graph", { state: { file: excelFile } });
  } else {
    alert("Please upload an Excel file first.");
  }
};
  const handleGenerateSummaryVideo = () => {
  // Add your logic to generate summary video here
  alert("Generating Summary Video...");
};

  // WebSocket for Real-Time Video URL Updates
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.processed_video_url) {
        setProcessedVideoURL(data.processed_video_url);
      }
    };
    return () => ws.close();
  }, []);

  // Handle video file input
  const handleVideoChange = (e) => {
    const file = e.target.files[0];
    if (file && supportedFormats.includes(file.type)) {
      setVideo(file);
    } else {
      alert("Unsupported video format! Please upload MP4, WebM, or Ogg.");
    }
  };
  
  const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    console.log("Selected file:", file.name);
    setExcelFile(file);
  }
};

  
  const handleUploadFileClick = () => {
    alert("Upload File Button Clicked");
  };
  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
     if (!trainNo || isNaN(trainNo)) {
    alert("Please enter a valid numeric Train Number.");
    return;
  }

    
    const formData = new FormData();
    formData.append("file", video);

    setIsUploading(true);

    try {
      const response = await axios.post(API_URL, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setProcessedVideoURL(response.data.processed_video_url);
      alert("Video uploaded and processing started!");
    } catch (error) {
      console.error("Error uploading video:", error);
      alert("Failed to upload and process the video.");
    } finally {
      setIsUploading(false);
    }
  };

  // Handle crew detail changes
  const handleCrewDetailChange = (e) => {
    const { name, value } = e.target;
    setCrewDetails((prevDetails) => ({
      ...prevDetails,
      [name]: value,
    }));
  };

  // Use navigate hook for routing
 
  
  // Handle Button Clicks
  const handleSectionalMpsClick = () => {
    navigate("/sectionalmps"); // Navigate to Sectional MPS page
  };
  
   const handleGoodsClick = () => {
    alert(`Selected Goods Option: ${goodsOption}`);
  };

  const handleChgClick = () => {
    alert("CHG Button Clicked");
  };
  

  return (
    <div className="app-container">
      <Header /> {/* Use the Header component here */}
      
      
      {/* Main Dashboard Layout */}
      <div className="dashboard-layout">
        {/* Left Panel: Form */}
        <div className="form-container">
          

          {/* Form row for parallel fields */}
          <div className="form-row">
            <div className="form-group">
              <label>Train Number:</label>
              <input
                type="text"
                name="trainNo"
                value={trainNo}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Journey Date:</label>
              <input
                type="date"
                name="inspectionDate"
                value={inspectionDate}
                onChange={handleChange} required />
            </div>
          </div>

          {/* Added fields below Train Number and Journey Date */}
          <div className="form-row">
            <div className="form-group">
              <label>Loco No.:</label>
              <input
                type="text"
                name="locoNo"
                value={locoNo}
                onChange={handleChange} required />
            </div>

            <div className="form-group">
              <label>Inspector Name:</label>
              <input
                type="text"
                name="inspectorName"
                value={inspectorName}
                onChange={handleChange} required />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Report ID:</label>
              <input
                type="text"
                name="reportID"
                value={reportID}
                onChange={handleChange} required />
            </div>

            {/* Today's Date input */}
            <div className="form-group">
              <label>Today's Date:</label>
              <input
                type="date"
                value={new Date().toISOString().split('T')[0]}  // Dynamically set today's date
                readOnly
              />
            </div>
          </div>

           {/* Added Loco Pilot Name and Designation below Report ID and Today's Date */}
<div className="form-row">
  <div className="form-group">
    <label>Loco Pilot Name:</label>
    <input
      type="text"
      value={lpName}
      onChange={(e) => setlpname(e.target.value)}
      name="lpName"
      required
    />
  </div>

  <div className="form-group">
    <label>Loco Pilot Designation:</label>
    <input
      type="text"
      value={lpDesignation}
      onChange={(e) =>setlpdesignation(e.target.value)}
      name="lpDesignation"
      required
    />
  </div>
</div>

        {/* Added Auto Loco Pilot Name and Designation */}
<div className="form-row">
  <div className="form-group">
    <label>Assitant Loco Pilot Name:</label>
    <input
      type="text"
      value={alpName}
      onChange={(e) => setalpname(e.target.value)}
      name="alpName"
      required
    />
  </div>

  <div className="form-group">
    <label>Assitant Loco Pilot Designation:</label>
    <input
      type="text"
      value={alpDesignation}
      onChange={(e) => setalpdesignation(e.target.value)}
      name="lpDesignation"
      required
    />
  </div>
</div>

{/* Added Start KM and SPM type */}
<div className="form-row">
  <div className="form-group">
    <label>Start KM:</label>
    <input
      type="text"
      value={crewDetails.lpName}
      onChange={(e) => handleCrewDetailChange(e)}
      name="lpName"
      required
    />
  </div>

  <div className="form-row">
  <div className="form-group">
    <label>SPM Type:</label>
    <select
      value={crewDetails.lpDesignation} // Bind the value to the state
      onChange={(e) => handleCrewDetailChange(e)} // Use the same handler for change
      name="lpDesignation" // Update the state with the name of the field
      required
    >
      <option value="">Select SPM Type</option>
      <option value="Medha">Medha</option>
      <option value="Laxven">Laxven</option>
      <option value="Telpro">Telpro</option>
    </select>
  </div>
</div>

          </div>

         
   </div>
  

        {/* Right Panel: Crew Details */}
        
        <div className="crew-details">
  

  {/* Button and Radio Buttons Row */}
  <div className="button-row">
    {/* Sectional MPS Button */}
    <div className="sectional">
      <button type="button" onClick={handleSectionalMpsClick}>
        Caution Order
      </button>
    </div>
    
  
    {/* Goods Radio Button */}
    <div className="form-group">
      <label className="radio-container">
        <input
          type="radio"
          name="goodsChg"
          value="goods"
          checked={selectedOption === "goods"}
          onChange={handleRadioChange}
          className="radio-input"
        />
        <span className="radio-circle"></span>
        Goods
      </label>
    </div>

    {/* CHG Radio Button */}
    <div className="form-group">
      <label className="radio-container">
        <input
          type="radio"
          name="goodsChg"
          value="chg"
          checked={selectedOption === "chg"}
          onChange={handleRadioChange}
          className="radio-input"
        />
        <span className="radio-circle"></span>
        CHG
      </label>
    </div>
  </div>

  {/* Conditional Dropdown for Goods */}
{selectedOption === "goods" && (
  <div className="form-group" style={{ textAlign: "right" }}>
    <label>Select Goods Type:</label>
    <select 
      value={goodsOption} 
      onChange={handleDropdownChange}
      style={{ marginLeft: "auto", display: "block", width: "fit-content" }}
    >
      <option value="">Select an option</option>
      <option value="Loaded (BMBS)">Loaded (BMBS)</option>
      <option value="Loaded (CONV)">Loaded (CONV)</option>
      <option value="Unloaded (BMBS)">Unloaded (BMBS)</option>
      <option value="Unloaded (CONV)">Unloaded (CONV)</option>
    </select>
  </div>
)}

{/* Load Amount Input Field */}
{selectedOption === "goods" && (goodsOption === "Loaded (BMBS)" || goodsOption === "Loaded (CONV)") && (
  <div className="form-group" style={{ textAlign: "right" }}>
    <label>Load Amount (in tons):</label>
    <input
      type="number"
      value={loadAmount}
      onChange={handleLoadAmountChange}
      placeholder="Enter load amount"
      style={{ marginLeft: "auto", display: "block", width: "fit-content" }}
    />
  </div>
)}

{/* Upload File Button */}
    <div className="upload-file">
      <button type="button" onClick={handleUploadFileClick}>
        Upload File
      </button>
    </div>
    
    {/* Checkboxes */}
<div className="checkbox-group">
  <label className="checkbox-container">
    <input
      type="checkbox"
      name="checkbox1"
      checked={checkbox1}
      onChange={handleCheckbox1Change}
    />
    SPM
  </label>
  <label className="checkbox-container">
    <input
      type="checkbox"
      name="checkbox2"
      checked={checkbox2}
      onChange={handleCheckbox2Change}
    />
    CVVRS
  </label>
</div>
    
<div className="form-row">
            <div className="form-group">
              <input
                type="file"
                accept={supportedFormats.join(", ")}
                onChange={handleVideoChange}
                required
              />
            </div>
          </div>
          
          <div className="form-row">
            <div className="form-group">
  <input
    type="file"
    accept=".xlsx, .xls, .csv"
    onChange={handleFileUpload}
    required
  />
</div>

          </div>
          
          {/* Report Buttons */}
<div className="report-buttons">
  <button
    type="button"
    onClick={handleGenerateSpmReport}
    className="spm-report"
  >
    Generate SPM Report
  </button>
  <button
    type="button"
    onClick={handleGenerateCvvrsReport}
    className="cvvrs-report"
  >
    Generate CVVRS Report
  </button>
</div>

{/* Additional Report Buttons */}
<div className="additional-report-buttons">
  <button
    type="button"
    onClick={handleGenerateSpmGraph}
    className="spm-graph"
  >
    Generate SPM Graph
  </button>
  <button
    type="button"
    onClick={handleGenerateSummaryVideo}
    className="summary-video"
  >
    Generate Summary Video
  </button>
</div>

</div>

      </div>

      {/* Processed Video Display */}
      {processedVideoURL && (
        <div className="processed-video-container">
          <h2>Processed Video</h2>
          <video controls>
            <source src={processedVideoURL} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
      
    </div>
  );
}

export default App;


