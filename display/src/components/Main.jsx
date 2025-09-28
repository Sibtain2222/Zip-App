import React from 'react'
import { useState } from 'react'
import axiosInstance from '../axiosInstance' 
import JSZip from "jszip";
import '../assets/css/style.css'


const Main = () => {
  const [folder, setFolder] = useState(null);
  const [folder_id, setfolderId] = useState(null);
  const [sizes, setSizes] = useState({ original: null, compressed: null });
  const handleFolder= async(e)=>{
    e.preventDefault();
    if (!folder) return;
     const zip = new JSZip();
    for (let i = 0; i < folder.length; i++) {
      const file = folder[i]; 
      const relativePath = file.webkitRelativePath || file.name;
      zip.file(relativePath, file);
    }

    const blob = await zip.generateAsync({ type: "blob" });
    const formData = new FormData();
    for (let i = 0; i < folder.length; i++) {
      formData.append("files", folder[i]);
  }

    try {
      // Upload files
      const response = await axiosInstance.post("/api/folder", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const { folder_id, original_size, compressed_size } = response.data;
      setfolderId(folder_id);
      setSizes({ original: original_size, compressed: compressed_size });

      console.log("Original:", original_size, "Compressed:", compressed_size);


      

// Convert sizes to numbers (assuming MB or KB with units)
      const parseSize = (sizeStr) => parseFloat(sizeStr); 
      const savedPercent = Math.max(
        0,
        Math.round(((parseSize(original_size) - parseSize(compressed_size)) / parseSize(original_size)) * 100)
      );

      setSizes({
        original: original_size,
        compressed: compressed_size,
        savedPercent,
      });


    } catch (error) {
      console.error("Upload error:", error.response?.data || error.message);
    } };
   const handleDownload = async () => {
    if (!folder_id) return;

    try {
      const downloadRes = await axiosInstance.get(`/api/folder/download/${folder_id}`, {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([downloadRes.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "compressed_folder.zip");
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("Download error:", error.response?.data || error.message);
    }
  };
  

    



  return (
    <>
    <div className='container'>
        <div className="button">
            <form onSubmit={handleFolder}>
              <input type="file" webkitdirectory="true" directory="true"  multiple onChange={(e) => setFolder(e.target.files)} />
              <button  value={folder}type='submit'>Zip Folder</button>
            </form>
            {sizes.original && (
            <div className="result-card folder-result">
              <h3>📁 Folder Compression Result</h3>
              <p>📂 Original size: <span>{sizes.original}</span></p>
              <p>📦 Compressed size: <span>{sizes.compressed}</span></p>
               {/* Progress Bar */}
              <div className="progress-wrap"><div className="progress-fill folder-progress" style={{ width: `${sizes.savedPercent || 0}%` }}></div></div>
              <p className="progress-text">💾 Space Saved: {sizes.savedPercent || 0 }</p>
              <button className="download-btn" onClick={handleDownload}>⬇ Download Folder Zip
              </button>
            </div>
          )}
        </div>
    </div>
    </>
  )
}


export default Main