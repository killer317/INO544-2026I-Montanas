import os
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image

# Importamos tu función del modelo
from validar_modelo import evaluar_foto

# ── CONFIGURACIÓN DE TEMA ──
ctk.set_appearance_mode("Dark")  # Forzamos modo oscuro para un look más "hacker/profesional"
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ves lo que veo 👁️🤖 - Clasificador CNN")
        self.geometry("650x700")
        self.resizable(False, False)

        self.ruta = ""
        self.ctk_image = None
        self._build_ui()

    def _build_ui(self):
        # ── TÍTULO ──
        titulo = ctk.CTkLabel(self, text="Clasificador de Montañas con IA", font=("Segoe UI", 24, "bold"))
        titulo.pack(pady=(20, 5))
        
        subtitulo = ctk.CTkLabel(self, text="Proyecto Feria I-2026 • Red Neuronal Convolucional", font=("Segoe UI", 12), text_color="gray")
        subtitulo.pack(pady=(0, 20))

        # ── BOTONES RÁPIDOS DE DEMOSTRACIÓN (Para la feria) ──
        demo_frame = ctk.CTkFrame(self, fg_color="transparent")
        demo_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkButton(demo_frame, text="⛰️ Cargar Ejemplo Montaña", fg_color="#27ae60", hover_color="#219150", 
                      command=lambda: self.cargar_ejemplo("prueba_montana.jpg")).pack(side="left", expand=True, padx=5)
                      
        ctk.CTkButton(demo_frame, text="🏙️ Cargar Ejemplo No Montaña", fg_color="#c0392b", hover_color="#a53125",
                      command=lambda: self.cargar_ejemplo("prueba_ciudad.jpg")).pack(side="right", expand=True, padx=5)

        # ── SELECTOR DE ARCHIVO MANUAL ──
        file_frame = ctk.CTkFrame(self)
        file_frame.pack(fill="x", padx=20, pady=5)

        self.ruta_entry = ctk.CTkEntry(file_frame, placeholder_text="O selecciona una imagen manual...", font=("Segoe UI", 12))
        self.ruta_entry.pack(side="left", fill="x", expand=True, padx=(10, 10), pady=10)
        
        ctk.CTkButton(file_frame, text="Examinar", width=100, command=self.seleccionar_archivo).pack(side="right", padx=(0, 10))

        # ── ÁREA DE VISTA PREVIA (PREVIEW) ──
        self.preview_frame = ctk.CTkFrame(self, height=320)
        self.preview_frame.pack(fill="both", expand=True, padx=20, pady=15)
        self.preview_frame.pack_propagate(False) # Evita que el frame colapse si no hay imagen

        self.thumb_label = ctk.CTkLabel(self.preview_frame, text="Esperando imagen...", font=("Segoe UI", 14), text_color="gray")
        self.thumb_label.pack(expand=True)

        # ── BOTÓN DE EVALUACIÓN ──
        self.btn_evaluar = ctk.CTkButton(self, text="🧠 Analizar con Red Neuronal", command=self.evaluar, 
                                         height=45, font=("Segoe UI", 16, "bold"))
        self.btn_evaluar.pack(padx=20, pady=(5, 15), fill="x")

        # ── ÁREA DE RESULTADOS Y BARRA DE PROGRESO ──
        self.result_label = ctk.CTkLabel(self, text="", font=("Segoe UI", 20, "bold"))
        self.result_label.pack(pady=(0, 5))

        self.progress_bar = ctk.CTkProgressBar(self, width=500, height=20, corner_radius=10)
        self.progress_bar.set(0) # Inicia vacía
        self.progress_bar.pack(pady=(0, 5))
        
        self.porcentaje_label = ctk.CTkLabel(self, text="", font=("Segoe UI", 14))
        self.porcentaje_label.pack(pady=(0, 20))

    def seleccionar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if ruta:
            self.procesar_nueva_ruta(ruta)

    def cargar_ejemplo(self, nombre_archivo):
        # Esta función busca la foto en la misma carpeta del script
        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre_archivo)
        if not os.path.exists(ruta):
            self.result_label.configure(text=f"No se encontró '{nombre_archivo}'", text_color="orange")
            return
        self.procesar_nueva_ruta(ruta)

    def procesar_nueva_ruta(self, ruta):
        self.ruta = ruta
        self.ruta_entry.delete(0, "end")
        self.ruta_entry.insert(0, ruta)
        self._mostrar_preview(ruta)
        # Limpiar resultados anteriores
        self.result_label.configure(text="")
        self.porcentaje_label.configure(text="")
        self.progress_bar.set(0)

    def _mostrar_preview(self, ruta):
        img = Image.open(ruta)
        # Redimensionar manteniendo proporciones para el UI
        img.thumbnail((500, 300), Image.Resampling.LANCZOS)
        self.ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
        self.thumb_label.configure(image=self.ctk_image, text="")

    def evaluar(self):
        if not self.ruta:
            self.result_label.configure(text="⚠️ Selecciona una imagen primero.", text_color="orange")
            return

        self.btn_evaluar.configure(state="disabled", text="Analizando...")
        self.update() # Forzar actualización gráfica

        # Llamamos a tu modelo
        es_montana, confianza = evaluar_foto(self.ruta)
        
        self.btn_evaluar.configure(state="normal", text="🧠 Analizar con Red Neuronal")

        if es_montana is None:
            self.result_label.configure(text="❌ Error al procesar la imagen.", text_color="red")
            return

        # ==========================================
        # AQUÍ AGREGAMOS EL PORCENTAJE AL INSTANTE
        # ==========================================
        if es_montana:
            texto = f"🏔️ ¡ES UNA MONTAÑA! ({confianza:.1f}%)"
            color = "#2ecc71" # Verde
        else:
            texto = f"🚫 NO ES UNA MONTAÑA ({confianza:.1f}%)"
            color = "#e74c3c" # Rojo

        # Mostramos el resultado con el número inmediatamente
        self.result_label.configure(text=texto, text_color=color)
        self.porcentaje_label.configure(text="") # Ocultamos el texto pequeño de abajo
        self.progress_bar.configure(progress_color=color)
        
        # Iniciar animación solo para que la barra se llene visualmente
        target_value = confianza / 100.0
        self.animar_barra(target_value, 0.0)

    def animar_barra(self, target, current):
        """Genera una animación fluida llenando solo la barra de progreso"""
        step = 0.05 # Velocidad de la animación
        if current < target:
            current += step
            if current > target: # Evitar pasarse del valor real
                current = target
            self.progress_bar.set(current)
            self.after(20, self.animar_barra, target, current) # Llama de nuevo en 20ms
        else:
            self.progress_bar.set(target)
if __name__ == "__main__":
    App().mainloop()