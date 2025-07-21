import { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [downloadLink, setDownloadLink] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('image', file);
    formData.append('brightness', 0.9); // example param

    try {
      const res = await axios.post('http://localhost:5000/generate', formData, {
        responseType: 'blob'
      });

      const blob = new Blob([res.data], { type: 'application/sla' });
      const url = URL.createObjectURL(blob);
      setDownloadLink(url);
    } catch (err) {
      console.error('Error generating STL:', err);
    }
  };

  return (
    <div>
      <h1>Lithophane Generator</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button type="submit">Generate STL</button>
      </form>
      {downloadLink && (
        <a href={downloadLink} download="lithophane.stl">Download STL</a>
      )}
    </div>
  );
}

export default App;