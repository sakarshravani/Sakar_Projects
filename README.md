# SPM CVVRS System  
**A Standalone Application for Railway Data Collection, Monitoring, and Reporting**

---

## **Introduction**  
The **SPM CVVRS System** (Speedometer and Crew Voice/Video Recording System) is a comprehensive software solution designed to automate railway operations monitoring. It integrates data analysis, report generation, and AI-driven video processing to enhance safety, compliance, and decision-making for locomotive management.  

---

## **Key Features**  
- **Data Entry & Management**:  
  - Input fields for Train Number, Journey Date, Loco Number, Inspector Name, Loco Pilot/ALP details, and more.  
  - Upload options for SPM (Excel) and CVVRS (video) files.  
- **Automated Reporting**:  
  - Generate SPM Reports (speed analysis) and CVVRS Reports (crew action logs).  
  - Interactive SPM graphs for speed/overall analysis with toggleable features.  
- **AI-Powered Video Processing**:  
  - Detect and log Assistant Loco Pilot (ALP) actions (e.g., door approach, hand gestures).  
  - Generate summary videos with annotated action timestamps.  
- **Admin Controls**:  
  - Secure credential-based access to update train details, stops, and Permanent Speed Restrictions (PSR).  
- **User-Friendly Interface**:  
  - Guided navigation, caution order integration, and real-time data visualization.  

---

## **Installation**  
1. **Download the Application**:  
   - Access the latest build from your organization’s repository (e.g., Zoho, GitHub).  
2. **Dependencies**:  
   - Ensure [Python 3.8+](https://www.python.org/) and [OpenCV](https://opencv.org/) are installed for video processing.  
   - Install required libraries:  
     ```bash  
     pip install pandas numpy opencv-python matplotlib  
     ```  
3. **Run the Application**:  
   - Execute the main script for CVVRS:  
     ```bash  
     python main.py  
     ```
   - Execute the main script for CVVRS:  
     ```bash  
     uvicorn main:app --reload  
     ```   

---

## **Usage Guide**  
### **1. Data Entry & SPM Report Generation**  
- Fill in all mandatory fields (e.g., Train Number, Loco Pilot Details).  
- Upload an Excel file for SPM data.  
- Click **Generate SPM Report** to process data and export results.  

### **2. Interactive SPM Graph**  
- Navigate to the home page and select **Generate SPM Graph**.  
- Toggle between *Speed Analysis* and *Overall Analysis*.  
- Customize graph features using checkboxes.  

### **3. CVVRS Video Processing**  
- Upload a video file and click **Generate Summary Video**.  
- The system will detect ALP actions (e.g., sitting, hand gestures) and produce a timestamped log.  

### **4. Admin Settings**  
- Go to **Settings** > Enter admin credentials.  
- Update train details, stops, or PSR data as needed.  

---

## **Admin Controls & Security**  
- **Access Restrictions**: Only authorized users can modify critical parameters.  
- **Database Management**: Securely update routes, stops, and speed restrictions.  

---

## **Technical Stack**  
- **Backend**: Python (Pandas, OpenCV, NumPy)  
- **Frontend**: [Specify UI framework, e.g., Tkinter, PyQt]  
- **AI Model**: [Mention if using TensorFlow/PyTorch for action detection]  

---

## **Contributing**  
This project is managed internally. For feedback or issues, contact the development team.  

---

## **License**  
Proprietary software owned by [Your Organization Name].  

---

## **Contact**  
- **Project Lead**: [Your Name]  
- **Email**: [Your Email]  
- **GitHub**: [Your Office GitHub Account Link]  

---

**Thank you for using the SPM CVVRS System!** 


