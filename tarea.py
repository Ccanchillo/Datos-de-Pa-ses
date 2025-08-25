import sys
import requests
from PIL import Image
from io import BytesIO
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QRunnable, QThreadPool, Signal, QObject

# Señal personalizada para comunicar el resultado de la descarga
class DataLoaderSignals(QObject):
    data_loaded = Signal(dict)
    error = Signal(str)

class DataLoader(QRunnable):
    """Tarea para descargar datos de países de la API sin congelar la UI."""
    def __init__(self):
        super().__init__()
        self.signals = DataLoaderSignals()

    def run(self):
        try:
            url = "https://restcountries.com/v3.1/all?fields=name,flags,population,currencies,translations"
            response = requests.get(url)
            response.raise_for_status()
            paises_data = response.json()
            
            datos_paises = {}
            for pais in paises_data:
                nombre_espanol = pais.get("translations", {}).get("spa", {}).get("common", "Nombre no disponible")
                
                moneda_info = list(pais.get("currencies", {}).values())
                moneda_nombre = "No disponible"
                if moneda_info:
                    moneda_nombre = moneda_info[0].get("name", "No disponible")
                
                poblacion_raw = pais.get("population", None)
                poblacion_formateada = "No disponible"
                if poblacion_raw is not None:
                    poblacion_millones = poblacion_raw / 1_000_000
                    poblacion_formateada = f"{poblacion_millones:.2f} millones"
                
                bandera_url = pais.get("flags", {}).get("png", None)
                
                datos_paises[nombre_espanol] = {
                    "moneda": moneda_nombre,
                    "poblacion": poblacion_formateada,
                    "bandera": bandera_url,
                }
            
            self.signals.data_loaded.emit(datos_paises)
        except Exception as e:
            self.signals.error.emit(str(e))

class BanderaLoader(QRunnable):
    """Tarea para descargar la bandera de un país sin congelar la UI."""
    def __init__(self, url, callback):
        super().__init__()
        self.url = url
        self.callback = callback

    def run(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            img_pil = Image.open(img_data)
            img_pil = img_pil.resize((150, 100), Image.LANCZOS)
            
            img_bytes = BytesIO()
            img_pil.save(img_bytes, format="PNG")
            pixmap = QPixmap()
            pixmap.loadFromData(img_bytes.getvalue())
            self.callback(pixmap)
        except Exception as e:
            print(f"Error al descargar o procesar la bandera: {e}")
            self.callback(None)


### 💻 Estructura de la Aplicación

class PaisApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Datos de Países del Mundo")
        self.setGeometry(100, 100, 450, 500)
        self.setStyleSheet(self.get_stylesheet())
        self.thread_pool = QThreadPool()
        self.datos_paises = {}
        self.setup_ui()
        self.cargar_datos_iniciales()

    def get_stylesheet(self):
        return """
            QWidget {
                background-color: #2e2e2e;
                color: #ffffff;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
            }
            QLineEdit, QComboBox {
                background-color: #3c3c3c;
                border: 2px solid #555555;
                border-radius: 8px;
                padding: 8px;
                color: #ffffff;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #1e90ff;
            }
            QComboBox::drop-down {
                border-left: 1px solid #555555;
            }
            QComboBox::down-arrow {
                image: url(data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><path fill="white" d="M8 12L2 4h12z"/></svg>);
            }
            QComboBox QAbstractItemView {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555555;
                selection-background-color: #1e90ff;
            }
        """

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.label_instruccion = QLabel("Cargando datos...")
        self.label_instruccion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # QLineEdit para la búsqueda
        self.entry_busqueda = QLineEdit()
        self.entry_busqueda.setPlaceholderText("Escribe un país...")
        self.entry_busqueda.setEnabled(False) 
        
        # QComboBox para la selección manual
        self.combobox = QComboBox()
        self.combobox.setEnabled(False) 
        
        self.label_bandera = QLabel()
        self.label_bandera.setFixedSize(150, 100)
        self.label_bandera.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_bandera.setStyleSheet("border: 2px solid #555555; border-radius: 8px;")
        
        self.label_moneda = QLabel("Moneda:")
        self.label_moneda.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.label_poblacion = QLabel("Población:")
        self.label_poblacion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.label_instruccion)
        layout.addWidget(self.entry_busqueda)
        layout.addWidget(self.combobox)
        layout.addStretch(1)
        layout.addWidget(self.label_bandera, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)
        layout.addWidget(self.label_moneda)
        layout.addWidget(self.label_poblacion)
        
        self.setLayout(layout)
        
        # Conexiones: El QComboBox y QLineEdit funcionan de forma independiente
        self.combobox.activated.connect(self.mostrar_detalles_combobox)
        self.entry_busqueda.returnPressed.connect(self.buscar_por_enter)

    def cargar_datos_iniciales(self):
        data_loader = DataLoader()
        data_loader.signals.data_loaded.connect(self.on_data_loaded)
        data_loader.signals.error.connect(self.on_data_error)
        self.thread_pool.start(data_loader)

    def on_data_loaded(self, datos_paises):
        self.datos_paises = datos_paises
        paises_nombres = sorted(list(self.datos_paises.keys()))
        self.combobox.addItems(paises_nombres)
        self.label_instruccion.setText("Busca un país o selecciónalo:")
        self.entry_busqueda.setEnabled(True)
        self.combobox.setEnabled(True)
        print("Datos de países cargados exitosamente.")

    def on_data_error(self, error_message):
        self.label_instruccion.setText(f"Error al cargar datos: {error_message}")
        print(f"Error: {error_message}")

    def mostrar_detalles_combobox(self):
        pais_seleccionado = self.combobox.currentText()
        self.mostrar_datos(pais_seleccionado)
    
    def mostrar_datos(self, pais_seleccionado):
        datos = self.datos_paises.get(pais_seleccionado, {"moneda": "No disponible", "poblacion": "No disponible", "bandera": None})
        moneda = datos["moneda"]
        poblacion = datos["poblacion"]
        bandera_url = datos["bandera"]
        self.label_moneda.setText(f"Moneda: {moneda}")
        self.label_poblacion.setText(f"Población: {poblacion}")
        if bandera_url:
            self.cargar_bandera(bandera_url)
        else:
            self.label_bandera.clear()

    def buscar_por_enter(self):
        pais_buscado = self.entry_busqueda.text().strip()
        if pais_buscado in self.datos_paises:
            self.mostrar_datos(pais_buscado)
        else:
            self.label_moneda.setText("Moneda: País no encontrado")
            self.label_poblacion.setText("Población: -")
            self.label_bandera.clear()

    def cargar_bandera(self, url):
        loader = BanderaLoader(url, self.actualizar_bandera)
        self.thread_pool.start(loader)

    def actualizar_bandera(self, pixmap):
        if pixmap:
            self.label_bandera.setPixmap(pixmap)
        else:
            self.label_bandera.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaisApp()
    window.show()
    sys.exit(app.exec())