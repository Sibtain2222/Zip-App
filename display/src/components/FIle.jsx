import React from 'react'
import { useState } from 'react'
import axiosInstance from '../axiosInstance' 
import JSZip, { file } from "jszip";
import '../assets/css/style.css'

const FIle = () => {
    const [file, setFile] = useState(null);
    const [file_id,setfileId]=useState(null);
    const [sizes, setSizes] = useState({ original: null, compressed: null });
    const handleFile = async (e) => {
    e.preventDefault();
    if (!file) return;


    const formData = new FormData();
    formData.append("file", file); // key must match backend

   try {
      const response = await axiosInstance.post("/api/file", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      const {file_id, original_size, compressed_size} = response.data;
      setfileId(file_id);
      setSizes({original: original_size, compressed: compressed_size});

      console.log("original:" ,original_size , "compressed:" , compressed_size)
      console.log("Response:", response.data);

     

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
    }
  }
  const Handel_Download = async(e)=>{
    if (!file_id) return;
      
    try{
      const fileresponse = await  axiosInstance.get(`/api/file/download/${file_id}`,{
       responseType:"blob",

        });
      const url =window.URL.createObjectURL(new Blob([fileresponse.data]));
      const link= document.createElement("a")
      link.href=url;
      link.setAttribute("download" , "compressed_file.zip");
      document.body.appendChild(link)
      link.click();
      link.remove();
    } catch(error){
      console.error("Download error:" , error.response?.data || error.message);



    };


  }


    

return (
    <>
     <div className='container'>
    <div className="file-container">
      <form onSubmit={handleFile}>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button   type="submit">Zip File</button>
        </form>

      {sizes.original && (
      <div className="result-card file-result">
        <h3>📄 File Compression Result</h3>
        <p>📂 Original size: <span>{sizes.original}</span></p>
        <p>📦 Compressed size: <span>{sizes.compressed}</span></p>
        {/* Progress Bar */}
        <div className="progress-wrap">
          <div className="progress-fill file-progress" style={{ width: `${sizes.savedPercent || 0}%` }}></div></div>
           <p className="progress-text"> 💾 Space Saved: {sizes.savedPercent || 0}</p>
        <button className="download-btn" onClick={Handel_Download}>
          ⬇ Download File Zip
        </button>
      </div>
    )}
      
   </div>
   </div>
    </>
    )
}

export default FIle