# Aplicación Multimodal OCR y LLMs

Esta aplicación combina **reconocimiento óptico de caracteres (OCR)** con **modelos de lenguaje (LLM)** para procesar texto a partir de imágenes.  
Permite subir imágenes con texto, extraer su contenido usando **EasyOCR**, y luego analizarlo o resumirlo mediante un modelo de lenguaje integrado.

Desarrollado con **Python** y **Streamlit**.

---

## Integrantes del equipo:
- Alejandra Suarez Sepulveda
- Cesar Augusto Montoya
- Isabella Mendoza

---

## Demo en línea

Puedes usar la app directamente en Streamlit Cloud aquí:

[https://aplicaci-nmultimodalocryllms-ugqvmhbpfgwhvtzrvn4zs5.streamlit.app](https://aplicaci-nmultimodalocryllms-ugqvmhbpfgwhvtzrvn4zs5.streamlit.app)

---

## Requisitos previos

- Python 3.9 o superior instalado  
- Git instalado (para clonar el repositorio)  

---

## Instalación y ejecución local

Sigue estos pasos en tu terminal o consola de comandos:

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/aplicacion-multimodal-ocr-llms.git
cd aplicacion-multimodal-ocr-llms
```

### 2. Crear un entorno virtual
```bash
python -m venv env
```

### 3. Activar el entorno virtual 
```bash
En Windows:env\Scripts\activateEn Mac/Linux: source env/bin/activate
```

### 4. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 5. Ejecutar la aplicación
```bash
streamlit run app.py
```
Luego abre el enlace local que te muestra la consola, algo como:Local URL: http://localhost:8501
