# 🌍 Aplicación de Datos de Países del Mundo

## 📋 Descripción
Aplicación de escritorio desarrollada en Python utilizando PySide6 que permite consultar información detallada de países del mundo, incluyendo banderas, monedas y población.

## ✨ Características Principales
- **Interfaz gráfica moderna** con diseño oscuro y elegante
- **Búsqueda en tiempo real** de países por nombre
- **Selector desplegable** con lista completa de países
- **Descarga automática de banderas** desde la API
- **Información detallada** de monedas y población
- **Procesamiento asíncrono** que no congela la interfaz
- **Diseño responsive** y fácil de usar

## 🛠️ Tecnologías Utilizadas
- **Python 3.8+**
- **PySide6** - Framework de interfaz gráfica
- **Requests** - Cliente HTTP para APIs
- **Pillow (PIL)** - Procesamiento de imágenes
- **REST Countries API** - Fuente de datos de países

## 📦 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación
1. **Clona el repositorio:**
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd tarea3
   ```

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta la aplicación:**
   ```bash
   python tarea.py
   ```

## 🚀 Uso de la Aplicación

### Funcionalidades
1. **Carga Inicial**: La aplicación descarga automáticamente datos de todos los países
2. **Búsqueda**: Escribe el nombre de un país en el campo de búsqueda
3. **Selección**: Usa el menú desplegable para elegir un país
4. **Visualización**: Observa la bandera, moneda y población del país seleccionado

### Interfaz de Usuario
- **Campo de búsqueda**: Búsqueda por nombre de país
- **Selector desplegable**: Lista completa de países disponibles
- **Área de bandera**: Muestra la bandera del país seleccionado
- **Información**: Moneda y población del país

## 🔧 Estructura del Código

### Clases Principales
- **`DataLoader`**: Descarga datos de países desde la API
- **`BanderaLoader`**: Procesa y descarga banderas de países
- **`PaisApp`**: Interfaz principal de la aplicación
- **`DataLoaderSignals`**: Sistema de señales para comunicación entre hilos

### Arquitectura
- **Patrón MVC**: Separación clara entre lógica y presentación
- **Hilos asíncronos**: Uso de QThreadPool para operaciones no bloqueantes
- **Manejo de errores**: Sistema robusto de manejo de excepciones
- **API REST**: Integración con REST Countries API

## 📱 Capturas de Pantalla
*[Aquí puedes agregar capturas de pantalla de tu aplicación]*

## 🤝 Contribución
Este proyecto fue desarrollado como parte de una tarea académica. Para contribuir:

1. Fork del repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📝 Historial de Commits
- **Commit inicial**: Implementación base de la aplicación
- **Feature**: Sistema de búsqueda y selección de países
- **Feature**: Descarga asíncrona de banderas
- **Feature**: Interfaz gráfica moderna con PySide6
- **Refactor**: Optimización del código y manejo de errores

## 🐛 Reporte de Errores
Si encuentras algún error o tienes sugerencias, por favor:
1. Revisa si el problema ya está reportado en Issues
2. Crea un nuevo Issue con descripción detallada
3. Incluye pasos para reproducir el error
4. Adjunta logs o capturas de pantalla si es posible

## 📄 Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor
**Desarrollado por:** [Tu Nombre]
**Fecha:** [Fecha de Desarrollo]
**Asignatura:** [Nombre de la Asignatura]

## 🙏 Agradecimientos
- **REST Countries API** por proporcionar datos de países
- **PySide6** por el framework de interfaz gráfica
- **Comunidad Python** por las librerías utilizadas

---

⭐ **¡Si te gusta este proyecto, dale una estrella al repositorio!**
