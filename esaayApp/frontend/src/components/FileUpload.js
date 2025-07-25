import React, { useState } from 'react';

function FileUpload() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploadStatus, setUploadStatus] = useState('');
    const [uploadLoading, setUploadLoading] = useState(false);
    const [fileFeedback, setFileFeedback] = useState('');

    const handleFileUpload = async (e) => {
        e.preventDefault();
        if(!selectedFile){
          setUploadStatus('Please select a file first');
          return;
        }
    
        setUploadLoading(true);
        setUploadStatus('');
    
        const formData = new FormData();
        formData.append('file', selectedFile);
        try {
          const response = await fetch('http://localhost:8000/api/upload-essay-file', {
            method: 'POST',
            body: formData  
          });
    
          const data = await response.json();
    
          if (response.ok) {
            setUploadStatus(`File uploaded successfully! File ID: ${data.file_id}`);
            setFileFeedback(data.feedback || ''); // <-- Add this line
            setSelectedFile(null);
          } else {
            setUploadStatus(`Upload failed: ${data.error || 'Unknown error'}`);
            setFileFeedback('');
          }
        } catch (error) {
          setUploadStatus('Error: Could not connect to server');
        } finally {
          setUploadLoading(false);
        }
      };

      return (
        <div style={{ marginTop: '20px' }}>
            <h3>Or Upload Essay File:</h3>
            <input
                type="file"
                accept=".pdf,.doc,.docx,.txt"
                onChange={(e) => setSelectedFile(e.target.files[0])}
            />
            <button onClick={handleFileUpload} disabled={uploadLoading}>
                {uploadLoading ? 'Uploading...' : 'Upload File'}
            </button>
            {uploadStatus && (
                <div style={{ marginTop: '10px', padding: '10px', backgroundColor: '#e8f5e8' }}>
                    <p>{uploadStatus}</p>
                </div>
            )}
            {fileFeedback && (
                <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#f0f0f0' }}>
                    <h3>File Feedback:</h3>
                    <p>{fileFeedback}</p>
                </div>
            )}
        </div>
      );
    }
    
    export default FileUpload;