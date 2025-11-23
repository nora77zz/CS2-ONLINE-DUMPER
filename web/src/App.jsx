import { useState, useEffect } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const FILES = [
  'animationsystem_dll.json',
  'buttons.json',
  'client_dll.json',
  'engine2_dll.json',
  'host_dll.json',
  'info.json',
  'interfaces.json',
  'materialsystem2_dll.json',
  'networksystem_dll.json',
  'offsets.json',
  'panorama_dll.json',
  'particles_dll.json',
  'pulse_system_dll.json',
  'rendersystemdx11_dll.json',
  'resourcesystem_dll.json',
  'scenesystem_dll.json',
  'schemasystem_dll.json',
  'server_dll.json',
  'soundsystem_dll.json',
  'steamaudio_dll.json',
  'vphysics2_dll.json',
  'worldrenderer_dll.json'
].sort();

function App() {
  const [selectedFile, setSelectedFile] = useState(FILES[0]);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData(selectedFile);
  }, [selectedFile]);

  const fetchData = async (filename) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_URL}/latest/${filename}`);
      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    if (data) {
      navigator.clipboard.writeText(JSON.stringify(data, null, 2));
      alert('Copied to clipboard!');
    }
  };

  const downloadJson = () => {
    if (!data) return;
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = selectedFile;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen p-8 font-mono bg-black text-white">
      <header className="mb-8 text-center">
        <h1 className="text-4xl font-bold text-white mb-2">CS2 Online Dumper</h1>
        <p className="text-gray-400">Always up-to-date offsets</p>
      </header>

      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-6">

        <div className="bg-gray-800 p-4 rounded-lg h-fit">
          <h2 className="text-xl font-semibold mb-4 text-gray-300">Files</h2>
          <div className="space-y-2 max-h-[70vh] overflow-y-auto pr-2 custom-scrollbar">
            {FILES.map(file => (
              <button
                key={file}
                onClick={() => setSelectedFile(file)}
                className={`w-full text-left px-4 py-2 rounded transition-colors text-sm ${selectedFile === file
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
              >
                {file}
              </button>
            ))}
          </div>
        </div>


        <div className="md:col-span-3 bg-gray-800 p-6 rounded-lg relative">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-green-400">{selectedFile}</h2>
            <div className="flex gap-2">
              <button
                onClick={downloadJson}
                className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded text-sm transition-colors flex items-center gap-2"
                disabled={!data}
              >
                <span>Download</span>
              </button>
              <button
                onClick={copyToClipboard}
                className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded text-sm transition-colors"
                disabled={!data}
              >
                Copy JSON
              </button>
            </div>
          </div>

          <div className="bg-gray-900 p-4 rounded overflow-auto max-h-[70vh] border border-gray-700">
            {loading && <p className="text-yellow-500">Loading...</p>}
            {error && <p className="text-red-500">Error: {error}</p>}
            {data && (
              <pre className="text-sm text-gray-300">
                {JSON.stringify(data, null, 2)}
              </pre>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
