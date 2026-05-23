import os
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image

# Importamos tu función del modelo (Asegúrate de que validar_modelo.py esté en la misma carpeta)
from validar_modelo import evaluar_foto

# ── CONFIGURACIÓN DEL TEMA ──
ctk.set_appearance_mode("Light") 
ctk.set_default_color_theme("blue")

class AppModerna(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Identificador de Montañas IA")
        self.geometry("1100x700") # Un poco más ancho para imitar la pantalla de la tablet
        self.resizable(False, False)
        
        # Fondo de la aplicación (Color azul muy clarito casi blanco, simulando el entorno)
        self.configure(fg_color="#E8F1F9") 

        self.ruta_actual = ""
        self.ctk_image = None
        
        # Configurar el grid principal
        # Fila 0: Cabecera (Título y Botones)
        # Fila 1: Paneles (Izquierdo y Derecho)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self._build_header()
        self._build_sidebar()
        self._build_main_area()

    def _build_header(self):
        # ── CABECERA SUPERIOR ──
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=30, pady=(20, 10))

        # Título
        titulo_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        titulo_frame.pack(side="left")
        
        ctk.CTkLabel(titulo_frame, text="🏔️", font=("Segoe UI", 28)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(titulo_frame, text="IDENTIFICADOR DE MONTAÑAS IA", 
                     font=("Segoe UI", 22, "bold"), text_color="#0F2B5B").pack(side="left")

        # Botones superiores
        botones_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        botones_frame.pack(side="right")

        btn_examinar = ctk.CTkButton(botones_frame, text="📁 Examinar Archivos", font=("Segoe UI", 14, "bold"),
                                     fg_color="#FFFFFF", text_color="#0F2B5B", hover_color="#F3F4F6", 
                                     corner_radius=10, height=45, command=self.seleccionar_archivo)
        btn_examinar.pack(side="left", padx=(0, 15))

        self.btn_analizar = ctk.CTkButton(botones_frame, text="Analizar Imagen", font=("Segoe UI", 14, "bold"),
                                          fg_color="#3B82F6", hover_color="#1D4ED8", 
                                          corner_radius=10, height=45, command=self.evaluar)
        self.btn_analizar.pack(side="left")


    def _build_sidebar(self):
        # ── PANEL IZQUIERDO (Tarjeta Flotante Blanca) ──
        self.sidebar_frame = ctk.CTkFrame(self, width=320, corner_radius=20, fg_color="#FFFFFF")
        self.sidebar_frame.grid(row=1, column=0, sticky="nsew", padx=(30, 15), pady=(10, 30))
        self.sidebar_frame.grid_propagate(False)

        # Título del panel
        ctk.CTkLabel(self.sidebar_frame, text="Administrador de Imágenes", 
                     font=("Segoe UI", 18, "bold"), text_color="#0F2B5B").pack(pady=(25, 15), padx=20, anchor="w")

        # Barra de búsqueda simulada
        self.search_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="🔍 Buscar imagen local...", 
                                         height=40, corner_radius=10, fg_color="#F0F4F8", border_width=0,
                                         text_color="#4B5563")
        self.search_entry.pack(padx=20, pady=(0, 20), fill="x")

        # Área de galería (Simulada con un frame escroleable y botones grilla)
        self.scroll_gallery = ctk.CTkScrollableFrame(self.sidebar_frame, fg_color="transparent")
        self.scroll_gallery.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Crear una pequeña grilla visual falsa para que se parezca al diseño
        self.scroll_gallery.grid_columnconfigure((0,1,2), weight=1)
        iconos = ["📄", "📄", "🏔️", "🏔️", "🏔️", "🏔️", "🏔️", "🏔️", "🏔️", "📄", "📄", "📂", "📂", "📂"]
        
        for i, icono in enumerate(iconos):
            row = i // 3
            col = i % 3
            # Tarjetitas de la galería
            card = ctk.CTkFrame(self.scroll_gallery, width=70, height=70, corner_radius=12, fg_color="#F0F4F8" if icono != "🏔️" else "#D1E2FA")
            card.grid(row=row, column=col, padx=8, pady=8)
            card.pack_propagate(False)
            ctk.CTkLabel(card, text=icono, font=("Segoe UI", 24)).pack(expand=True)


    def _build_main_area(self):
        # ── PANEL DERECHO (Contenedor de tarjetas de imagen y resultados) ──
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.grid(row=1, column=1, sticky="nsew", padx=(15, 30), pady=(10, 30))

        # -- Tarjeta de Vista Previa (Azul claro) --
        self.preview_card = ctk.CTkFrame(self.right_container, fg_color="#407CE8", corner_radius=20)
        self.preview_card.pack(fill="both", expand=True, pady=(0, 20))

        ctk.CTkLabel(self.preview_card, text="Imagen Cargada", font=("Segoe UI", 16, "bold"), text_color="#FFFFFF").pack(anchor="w", padx=25, pady=(15, 10))

        # Contenedor de la imagen con el borde neón cyan
        self.image_border_frame = ctk.CTkFrame(self.preview_card, fg_color="#1E1E1E", corner_radius=15, 
                                               border_width=3, border_color="#00E5FF")
        self.image_border_frame.pack(expand=True, fill="both", padx=25, pady=(0, 25))
        
        self.thumb_label = ctk.CTkLabel(self.image_border_frame, text="Ninguna imagen seleccionada", text_color="gray", corner_radius=15)
        self.thumb_label.pack(expand=True, fill="both", padx=2, pady=2)

        # -- Tarjeta de Resultados (Azul muy oscuro) --
        self.result_box = ctk.CTkFrame(self.right_container, fg_color="#091636", corner_radius=20, height=140)
        self.result_box.pack(fill="x")
        self.result_box.pack_propagate(False)

        # Textos superiores del cuadro oscuro
        text_frame = ctk.CTkFrame(self.result_box, fg_color="transparent")
        text_frame.pack(fill="x", padx=25, pady=(20, 5))
        
        ctk.CTkLabel(text_frame, text="RESULTADOS DEL ANÁLISIS", font=("Segoe UI", 12, "bold"), text_color="#A3B8D7").pack(side="left")
        self.lbl_probabilidad = ctk.CTkLabel(text_frame, text="PROBABILIDAD: --%", font=("Segoe UI", 16, "bold"), text_color="#FFFFFF")
        self.lbl_probabilidad.pack(side="right")

        # Barra de progreso (Fondo oscuro, borde cyan, relleno azul)
        self.progress_bar = ctk.CTkProgressBar(self.result_box, height=28, corner_radius=14, 
                                               fg_color="#091636", border_width=2, border_color="#00E5FF",
                                               progress_color="#3B82F6")
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=25, pady=(10, 5))

        # Textos inferiores de la barra
        labels_frame = ctk.CTkFrame(self.result_box, fg_color="transparent")
        labels_frame.pack(fill="x", padx=30)
        
        self.lbl_resultado_izq = ctk.CTkLabel(labels_frame, text="NO ES MONTAÑA", font=("Segoe UI", 13, "bold"), text_color="#FFFFFF")
        self.lbl_resultado_izq.pack(side="left")
        
        self.lbl_resultado_final = ctk.CTkLabel(labels_frame, text="ES MONTAÑA", font=("Segoe UI", 14, "bold"), text_color="#00E5FF")
        self.lbl_resultado_final.pack(side="right")


    # ── LÓGICA DE LA APLICACIÓN ──
    def seleccionar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if ruta:
            self.ruta_actual = ruta
            self._mostrar_preview(ruta)
            # Resetear UI
            self.progress_bar.set(0)
            self.lbl_probabilidad.configure(text="PROBABILIDAD: --%", text_color="#FFFFFF")
            self.lbl_resultado_final.configure(text_color="#00E5FF") # Cyan por defecto
            self.image_border_frame.configure(border_color="#00E5FF") # Borde neón por defecto

    def _mostrar_preview(self, ruta):
        img = Image.open(ruta)
        # Redimensionamos para que quepa bien en el nuevo contenedor
        img.thumbnail((700, 400), Image.Resampling.LANCZOS) 
        self.ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
        self.thumb_label.configure(image=self.ctk_image, text="")

    def evaluar(self):
        if not self.ruta_actual:
            self.lbl_probabilidad.configure(text="SELECCIONE UNA IMAGEN", text_color="#EF4444")
            return

        self.btn_analizar.configure(state="disabled", text="Analizando...")
        self.update()

        # Llamamos al modelo
        es_montana, confianza = evaluar_foto(self.ruta_actual)
        
        self.btn_analizar.configure(state="normal", text="Analizar Imagen")

        if es_montana is None:
            self.lbl_probabilidad.configure(text="ERROR EN ARCHIVO", text_color="#EF4444")
            return

        # 1. Ajustes según el resultado
        color_neon = "#00E5FF" if es_montana else "#FF3366" # Cyan brillante (Montaña) o Rosa/Rojo neón (No Montaña)
        texto_prefijo = "PROBABILIDAD MONTAÑA" if es_montana else "PROBABILIDAD NO MONTAÑA"
        
        # Ajustamos el color del borde de la imagen, barra y texto inferior para que haga "juego"
        self.progress_bar.configure(border_color=color_neon)
        self.image_border_frame.configure(border_color=color_neon)
        self.lbl_resultado_final.configure(text_color=color_neon)

        # 2. Calculamos el porcentaje real para mostrar (Para que la barra siempre crezca)
        porcentaje_mostrar = confianza if confianza >= 50 else (100.0 - confianza)
        target_value = porcentaje_mostrar / 100.0
        
        self.progress_bar.set(0)
        self.animar_barra(target_value, 0.0, porcentaje_mostrar, texto_prefijo)

    def animar_barra(self, target, current, porcentaje_final, prefijo_texto):
        step = 0.03
        if current < target:
            current += step
            if current > target:
                current = target
                
            self.progress_bar.set(current)
            porcentaje_actual = current * 100
            
            self.lbl_probabilidad.configure(text=f"{prefijo_texto}: {porcentaje_actual:.1f}%")
            self.after(15, self.animar_barra, target, current, porcentaje_final, prefijo_texto)
        else:
            self.progress_bar.set(target)
            self.lbl_probabilidad.configure(text=f"{prefijo_texto}: {porcentaje_final:.1f}%")

if __name__ == "__main__":
    AppModerna().mainloop()