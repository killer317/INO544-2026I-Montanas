// ... existing code ...
import React, { useState, useRef, useEffect } from 'react'
import { Upload, Cpu, Monitor, Terminal as TerminalIcon, Image as ImageIcon, Zap } from 'lucide-react'

// Estilos globales integrados para asegurar compilación
const globalStyles = `
  body {
    margin: 0;
    padding: 0;
    overflow-x: hidden;
    background-color: #020617; /* slate-950 */
  }
  @keyframes scan {
    0%, 100% { top: 0; }
    50% { top: 100%; }
  }
`;

export default function App() {
  const [imageSrc, setImageSrc] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const [status, setStatus] = useState("ESPERANDO SEÑAL");
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [progress, setProgress] = useState(0);
  const [logs, setLogs] = useState([
    "[SISTEMA] Interfaz React unificada inicializada.",
    "[SISTEMA] Motor de evaluación preparado..."
  ]);
  
  const fileInputRef = useRef(null);
  const logsEndRef = useRef(null);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setImageSrc(url);
      setImageFile(file);
      setStatus("IMAGEN CARGADA");
      setProgress(0);
      setLogs(prev => [...prev, `[SISTEMA] Archivo cargado en memoria: ${file.name}`]);
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  const handleEvaluate = async () => {
    if (!imageFile) {
      setLogs(prev => [...prev, "[ERROR] No hay señal de imagen para procesar."]);
      return;
    }

    setIsEvaluating(true);
    setStatus("EVALUANDO TENSOR...");
    setProgress(0);
    setLogs(prev => [...prev, "[ACCIÓN] Enviando tensor al motor ONNX local..."]);

    // Animación de progreso mientras esperamos la respuesta de Python
    const interval = setInterval(() => {
      setProgress(p => (p < 85 ? p + Math.floor(Math.random() * 15) : p));
    }, 200);

    try {
      const formData = new FormData();
      formData.append("image", imageFile);

      // Llamamos a nuestro nuevo servidor Flask
      const response = await fetch("http://localhost:5000/api/evaluate", {
        method: "POST",
        body: formData
      });
      
      const data = await response.json();
      clearInterval(interval);
      setProgress(100);
      setIsEvaluating(false);
      setStatus("EVALUACIÓN COMPLETADA");

      if (data.error) throw new Error(data.error);

      setLogs(prev => [
        ...prev, 
        "[PROCESO] Inferencia ONNX completada con éxito.",
        `[RESULTADO] ${data.es_montana ? 'ES UNA MONTAÑA 🏔️' : 'NO ES MONTAÑA 🚫'} (Confianza: ${data.confianza.toFixed(2)}%)`
      ]);

    } catch (error) {
      clearInterval(interval);
      setIsEvaluating(false);
      setStatus("ERROR DE CONEXIÓN");
      setLogs(prev => [...prev, `[ERROR] Servidor IA no responde: ${error.message}`]);
    }
  };

  return (
    <>
      <style>{globalStyles}</style>
      <div className="flex flex-col md:flex-row h-screen bg-slate-950 text-cyan-50 font-sans selection:bg-cyan-900 w-full overflow-hidden">
        
        {/* PANEL LATERAL */}
        <aside className="w-full md:w-72 bg-slate-900 border-b md:border-b-0 md:border-r border-cyan-900/50 p-6 flex flex-col shadow-[4px_0_24px_rgba(8,145,178,0.1)] z-10 shrink-0">
          <div className="flex items-center gap-3 mb-10 text-cyan-400">
            <Zap className="w-8 h-8" />
            <h1 className="text-xl font-bold tracking-widest">MÓDULO<br/>VISIÓN</h1>
          </div>

          <div className="space-y-4 flex-1">
            <input 
              type="file" 
              ref={fileInputRef} 
              onChange={handleImageUpload} 
              accept="image/*" 
              className="hidden" 
            />
            
            <button 
              onClick={triggerFileInput}
              disabled={isEvaluating}
              className="w-full flex items-center justify-center gap-2 bg-cyan-950/50 hover:bg-cyan-900/80 border border-cyan-800 hover:border-cyan-400 text-cyan-300 py-3 px-4 rounded-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed group cursor-pointer"
            >
              <Upload className="w-5 h-5 group-hover:-translate-y-1 transition-transform" />
              <span>Cargar Imagen</span>
            </button>

            <button 
              onClick={handleEvaluate}
              disabled={isEvaluating || !imageSrc}
              className="w-full flex items-center justify-center gap-2 bg-transparent hover:bg-cyan-950 border-2 border-cyan-700/50 hover:border-cyan-400 hover:shadow-[0_0_15px_rgba(34,211,238,0.3)] text-cyan-400 py-3 px-4 rounded-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed group cursor-pointer"
            >
              <Cpu className={`w-5 h-5 ${isEvaluating ? 'animate-pulse text-cyan-200' : ''}`} />
              <span>{isEvaluating ? 'Procesando...' : 'Evaluar Imagen'}</span>
            </button>
          </div>

          <div className="mt-auto pt-6 border-t border-cyan-900/50 text-xs text-cyan-700 font-mono text-center">
            SYS.VER 3.14.15 // ONLINE
          </div>
        </aside>

        {/* ÁREA PRINCIPAL */}
        <main className="flex-1 flex flex-col p-4 md:p-8 overflow-hidden relative">
          <div className="absolute inset-0 bg-[linear-gradient(rgba(8,145,178,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(8,145,178,0.03)_1px,transparent_1px)] bg-[size:30px_30px] pointer-events-none"></div>

          <header className="mb-6 z-10 flex items-center justify-between shrink-0">
            <div className="flex items-center gap-3">
              <Monitor className="w-6 h-6 text-cyan-500" />
              <h2 className="text-2xl font-semibold tracking-wide text-cyan-100">Panel de Control CNN</h2>
            </div>
            <div className="bg-slate-900 border border-cyan-800/60 px-4 py-2 rounded-full flex items-center gap-3 shadow-[0_0_10px_rgba(8,145,178,0.15)]">
              <div className={`w-2.5 h-2.5 rounded-full ${isEvaluating ? 'bg-yellow-400 animate-pulse' : 'bg-green-400 shadow-[0_0_8px_rgba(74,222,128,0.8)]'}`}></div>
              <span className="font-mono text-sm uppercase tracking-wider text-cyan-300">{status}</span>
            </div>
          </header>

          {/* CONTENEDOR DE LA IMAGEN */}
          <div className="flex-1 min-h-[200px] bg-slate-900/80 border border-cyan-900/60 rounded-xl relative overflow-hidden flex items-center justify-center z-10 mb-6 backdrop-blur-sm group">
            {imageSrc ? (
              <>
                <img 
                  src={imageSrc} 
                  alt="Target" 
                  className={`max-w-full max-h-full object-contain z-10 transition-all duration-700 ${isEvaluating ? 'contrast-125 brightness-110 saturate-150' : ''}`}
                />
                {isEvaluating && (
                  <div className="absolute top-0 left-0 w-full h-1 bg-cyan-400 shadow-[0_0_15px_#22d3ee] animate-[scan_2s_ease-in-out_infinite] z-20 opacity-70"></div>
                )}
                <div className="absolute inset-0 border-2 border-cyan-500/20 m-4 rounded pointer-events-none z-20">
                  <div className="absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 border-cyan-400"></div>
                  <div className="absolute top-0 right-0 w-4 h-4 border-t-2 border-r-2 border-cyan-400"></div>
                  <div className="absolute bottom-0 left-0 w-4 h-4 border-b-2 border-l-2 border-cyan-400"></div>
                  <div className="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-cyan-400"></div>
                </div>
              </>
            ) : (
              <div className="flex flex-col items-center text-cyan-800">
                <ImageIcon className="w-16 h-16 mb-4 opacity-50" />
                <p className="font-mono tracking-widest text-sm">[ SIN SEÑAL DE VIDEO ]</p>
              </div>
            )}
          </div>

          {/* BARRA DE PROGRESO */}
          <div className="mb-6 z-10 shrink-0">
            <div className="flex justify-between text-xs font-mono text-cyan-500 mb-2">
              <span>PROGRESO DE ANÁLISIS</span>
              <span>{progress}%</span>
            </div>
            <div className="h-2 w-full bg-slate-900 rounded-full overflow-hidden border border-cyan-900/50">
              <div 
                className="h-full bg-cyan-500 shadow-[0_0_10px_#22d3ee] transition-all duration-300 ease-out"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div>

          {/* CONSOLA DE LOGS */}
          <div className="h-32 md:h-40 bg-slate-950 border border-cyan-900/50 rounded-xl p-4 font-mono text-sm overflow-y-auto z-10 shadow-inner flex flex-col gap-1 shrink-0">
            <div className="flex items-center gap-2 mb-2 text-cyan-600 border-b border-cyan-900/30 pb-2">
              <TerminalIcon className="w-4 h-4" />
              <span className="text-xs tracking-wider">TERMINAL DE SALIDA</span>
            </div>
            {logs.map((log, index) => (
              <div key={index} className={`${log.includes('[ERROR]') ? 'text-red-400' : log.includes('[RESULTADO]') ? 'text-green-400 font-bold' : 'text-cyan-500'} break-words`}>
                <span className="text-cyan-800 opacity-50 mr-2">{'>'}</span> {log}
              </div>
            ))}
            <div ref={logsEndRef} />
          </div>
        </main>
      </div>
    </>
  );
}