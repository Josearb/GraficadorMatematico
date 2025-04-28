import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from tkinter import messagebox
from tkinter import ttk

class GraficadorMatematico:
    def __init__(self):
        self.window = Tk()
        self.window.title("ATcnea_Graph Pro")
        self.window.geometry("1100x800")
        self.window.configure(bg="#1e1e2d")  # Fondo oscuro moderno
        
        # Estilo global
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background="#1e1e2d")
        self.style.configure('TLabel', background="#1e1e2d", foreground="#ffffff", font=('Arial', 11))
        self.style.configure('TButton', font=('Arial', 10), padding=6)
        self.style.map('TButton', 
                      background=[('active', '#3a3a4d'), ('!disabled', '#2a2a3a')],
                      foreground=[('!disabled', '#ffffff')])
        
        # Configuración de la figura con fondo blanco
        plt.style.use('default')  # Usar estilo por defecto (fondo blanco)
        self.fig, self.ax = plt.subplots(figsize=(7, 5), facecolor='white')
        self.ax.set_facecolor('white')
        
        # Canvas para la gráfica
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
        
        # Barra de herramientas de navegación
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.window, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack(side=TOP, fill=X, padx=10)
        
        # Marco principal para controles
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=X, padx=10, pady=5)
        
        # Etiqueta de instrucciones
        label_instrucciones = ttk.Label(main_frame, 
                                      text="Ingrese su función matemática (use 'x' como variable):", 
                                      font=('Arial', 12, 'bold'))
        label_instrucciones.pack(pady=(0, 10))
        
        # Marco para entrada de función (más compacto)
        func_frame = ttk.Frame(main_frame)
        func_frame.pack(fill=X, pady=5)
        
        ttk.Label(func_frame, text="f(x) =").pack(side=LEFT, padx=(0, 5))
        
        self.entry_funcion = ttk.Entry(func_frame, width=30, font=('Arial', 12))  # Más pequeño (30 caracteres)
        self.entry_funcion.pack(side=LEFT, expand=True, fill=X, padx=5)
        
        # Botón de graficar al lado del entry (más grande)
        btn_graficar = ttk.Button(func_frame, text="GRAFICAR", command=self.graficar, 
                                 style='Accent.TButton', width=12)
        btn_graficar.pack(side=LEFT, padx=5)
        
        # Configurar estilo especial para los botones
        self.style.configure('Accent.TButton', background='#4CAF50', foreground='white', font=('Arial', 10, 'bold'))
        self.style.configure('Large.TButton', font=('Arial', 10, 'bold'), padding=8)
        
        # Marco para botones de funciones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X, pady=10)
        
        # Botones de funciones matemáticas
        comandos = [
            ("sen(x)", "np.sin(x)"), 
            ("cos(x)", "np.cos(x)"), 
            ("tan(x)", "np.tan(x)"), 
            ("cot(x)", "1/np.tan(x)"), 
            ("log(x)", "np.log(x)"), 
            ("√x", "np.sqrt(x)"), 
            ("∛x", "np.cbrt(x)"), 
            ("x²", "x**2"),
            ("eˣ", "np.exp(x)"),
            ("|x|", "np.abs(x)"),
            ("π", "np.pi"),
            ("e", "np.e")
        ]
        
        # Organizar botones en una cuadrícula
        for i, (texto, comando) in enumerate(comandos):
            btn = ttk.Button(button_frame, text=texto, 
                           command=lambda c=comando: self.insertar_comando(c),
                           width=6)
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)
        
        # Marco para botones de control (más grandes)
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=X, pady=10)
        
        # Botones más grandes con texto claro
        btn_limpiar = ttk.Button(control_frame, text="LIMPIAR TODO", 
                               command=self.limpiar,
                               style='Large.TButton',
                               width=15)
        btn_limpiar.pack(side=LEFT, padx=5)
        
        btn_ayuda = ttk.Button(control_frame, text="AYUDA / INSTRUCCIONES", 
                             command=self.mostrar_ayuda,
                             style='Large.TButton',
                             width=20)
        btn_ayuda.pack(side=LEFT, padx=5)
        
        # Marco para información de la función
        info_frame = ttk.Frame(main_frame, style='Info.TFrame')
        self.style.configure('Info.TFrame', background='#2a2a3a', borderwidth=1, relief='solid')
        info_frame.pack(fill=X, pady=10, ipady=5)
        
        self.label_info = ttk.Label(info_frame, 
                                  text="Aquí aparecerán los detalles de la función graficada",
                                  style='Info.TLabel',
                                  font=('Arial', 10))
        self.style.configure('Info.TLabel', background='#2a2a3a', foreground='#ffffff')
        self.label_info.pack(pady=5)
        
        # Configuración inicial del gráfico
        self.configurar_grafico()
        
    def configurar_grafico(self):
        """Configura el aspecto inicial del gráfico"""
        self.ax.clear()
        self.ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
        self.ax.axhline(y=0, color='black', linewidth=1)
        self.ax.axvline(x=0, color='black', linewidth=1)
        self.ax.set_xlabel('Eje X', color='black')
        self.ax.set_ylabel('Eje Y', color='black')
        self.ax.set_title('Gráfico de Función', color='black', pad=20)
        self.canvas.draw()
        
    def insertar_comando(self, comando):
        """Inserta el comando en el campo de entrada"""
        self.entry_funcion.insert(END, comando)
        
    def graficar(self):
        """Grafica la función ingresada por el usuario"""
        funcion = self.entry_funcion.get().strip()
        
        if not funcion:
            messagebox.showwarning("Advertencia", "Por favor ingrese una función matemática.")
            return
            
        try:
            x = np.linspace(-10, 10, 1000)
            
            # Manejar divisiones por cero y valores no definidos
            with np.errstate(divide='ignore', invalid='ignore'):
                y = eval(funcion)
            
            # Configurar el gráfico
            self.configurar_grafico()
            
            # Graficar la función con estilo mejorado
            line, = self.ax.plot(x, y, 
                                label=f"f(x) = {funcion}", 
                                color='#4CAF50', 
                                linewidth=2.5, 
                                linestyle='-',
                                marker='', 
                                markersize=0,
                                alpha=0.9)
            
            # Rellenar el área bajo la curva
            self.ax.fill_between(x, y, color='#4CAF50', alpha=0.2)
            
            # Añadir leyenda con estilo
            legend = self.ax.legend(loc='upper right', framealpha=0.5)
            legend.get_frame().set_facecolor('white')
            legend.get_frame().set_edgecolor('black')
            
            # Calcular información de la función
            y_valid = y[np.isfinite(y)]
            if len(y_valid) > 0:
                info_text = (f"Función: f(x) = {funcion}\n"
                           f"Dominio visualizado: x ∈ [-10, 10]\n"
                           f"Rango en este dominio: [{np.min(y_valid):.2f}, {np.max(y_valid):.2f}]\n"
                           f"Intersección con eje Y: {y[len(y)//2]:.2f}")
            else:
                info_text = f"Función: f(x) = {funcion}\nNo definida en el dominio actual"
            
            self.label_info.config(text=info_text)
            
            # Ajustar los límites del gráfico automáticamente
            self.ax.relim()
            self.ax.autoscale_view()
            
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo graficar la función:\n{str(e)}\n\nRevise la sintaxis y vuelva a intentar.")
            
    def limpiar(self):
        """Limpia el gráfico y los campos de entrada"""
        self.entry_funcion.delete(0, END)
        self.configurar_grafico()
        self.label_info.config(text="Aquí aparecerán los detalles de la función graficada")
        
    def mostrar_ayuda(self):
        """Muestra un mensaje de ayuda al usuario con texto claro"""
        ayuda = """
        INSTRUCCIONES DE USO:
        
        1. INGRESAR FUNCIÓN:
           - Escriba la función usando 'x' como variable
           - Ejemplos válidos:
             * 2*x + 3
             * np.sin(x) + np.cos(x)
             * x**2 + 3*x - 5
             * np.log(x) + 1
        
        2. BOTONES DE FUNCIONES:
           - Use los botones para insertar funciones comunes
           - 'sen(x)', 'cos(x)', etc. para funciones trigonométricas
           - '√x' para raíz cuadrada, 'x²' para potencia
        
        3. ACCIONES:
           - GRAFICAR: Dibuja la función ingresada
           - LIMPIAR TODO: Borra la gráfica y el campo de texto
           - AYUDA: Muestra estas instrucciones
        
        Nota: Las funciones trigonométricas usan radianes.
        Para potencias use x**2 (x al cuadrado) o x**3 (x al cubo).
        """
        messagebox.showinfo("AYUDA - INSTRUCCIONES", ayuda)
        
    def start(self):
        self.window.mainloop()

# Iniciar la aplicación
if __name__ == "__main__":
    app = GraficadorMatematico()
    app.start()
