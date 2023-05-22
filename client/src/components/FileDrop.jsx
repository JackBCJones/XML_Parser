import React, { useState } from 'react';

function FileUpload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [downloadLink, setDownloadLink] = useState(null);
  const [xMultiplier, setXMultiplier] = useState(1.15);
  const [yMultiplier, setYMultiplier] = useState(0.74);


  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', selectedFile);

    const url = `https://fbxml.herokuapp.com/upload?x_multiplier=${xMultiplier}&y_multiplier=${yMultiplier}`;

    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
        mode: 'cors'
      })
      .then((response) => response.blob())
      .then((blob) => {
        const fileUrl = URL.createObjectURL(blob);
        setDownloadLink(fileUrl);
      })
    } catch (error) {
      console.error(error);
    }
  };
  
  
  

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <div>
        <label>Field Width (x):</label>
        <input
          type="number"
          step="0.10"
          value={xMultiplier}
          onChange={(e) => setXMultiplier(e.target.value)}
        />
      </div>
      <div>
        <label>Field Height (y):</label>
        <input
          type="number"
          step="0.10"
          value={yMultiplier}
          onChange={(e) => setYMultiplier(parseFloat(e.target.value))}
        />
      </div>
      <button onClick={handleUpload}>Upload</button>
      {downloadLink && (
        <a href={downloadLink} download="converted_file.json">
          Download converted_file
        </a>
      )}
    </div>
  );
}

export default FileUpload;
