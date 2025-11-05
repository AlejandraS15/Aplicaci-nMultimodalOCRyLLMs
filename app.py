import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import easyocr
import cv2
from dotenv import load_dotenv

# Carga variables de entorno
load_dotenv()

st.set_page_config(page_title="Taller IA: OCR + LLM", layout="centered")

# ---------------------------
# Helpers
# ---------------------------

@st.cache_resource
def load_ocr_reader(lang_list=None, use_gpu=False):
    """
    Carga el modelo easyocr.Reader y lo cachea en memoria.
    lang_list: lista de códigos de idiomas (ej: ['en','es'])
    use_gpu: True si quieres usar GPU (si tu torch lo soporta)
    """
    if lang_list is None:
        lang_list = ['en']  # por defecto inglés; puedes cambiar o pasar ['es','en']
    reader = easyocr.Reader(lang_list, gpu=use_gpu)
    return reader

def pil_to_cv2(image: Image.Image):
    """Convierte PIL Image a arreglo cv2 (BGR)"""
    rgb = np.array(image.convert('RGB'))
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

def draw_boxes_on_image(pil_img: Image.Image, results):
    """
    Dibuja recuadros sobre la imagen.
    results: salida de reader.readtext -> lista de (bbox, text, confidence)
    """
    img = pil_img.convert("RGBA")
    overlay = Image.new('RGBA', img.size, (255,255,255,0))
    draw = ImageDraw.Draw(overlay)
    for (bbox, text, conf) in results:
        # bbox es lista de 4 puntos: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
        xs = [int(p[0]) for p in bbox]
        ys = [int(p[1]) for p in bbox]
        draw.polygon([(xs[0], ys[0]), (xs[1], ys[1]), (xs[2], ys[2]), (xs[3], ys[3])],
                     outline=(255,0,0,180), width=2)
    combined = Image.alpha_composite(img, overlay)
    return combined.convert("RGB")

def ocr_to_text(results):
    """Convierte la salida de easyocr a texto concatenado legible."""
    lines = []
    for (bbox, text, conf) in results:
        lines.append(text)
    return "\n".join(lines)

# ---------------------------
# Interfaz
# ---------------------------

st.title("Taller IA: OCR + LLM")
st.header("Módulo 1 — Lector de Imágenes (OCR)")

# Panel lateral para opciones
with st.sidebar:
    st.subheader("Opciones OCR")
    langs = st.multiselect("Idiomas para OCR (orden preferido):", 
                           options=['en','es','pt','fr','de','it','ru'], 
                           default=['es','en'])
    use_gpu = st.checkbox("Usar GPU (si está disponible)", value=False)
    show_boxes = st.checkbox("Mostrar recuadros detectados en la imagen", value=True)
    st.write("Consejo: la primera ejecución descarga modelos y puede tardar.")

# Carga de archivo de imagen
uploaded_file = st.file_uploader("Sube una imagen (.png, .jpg, .jpeg)", 
                                 type=['png','jpg','jpeg'])

# Inicializar session_state para persistencia del texto
if 'ocr_text' not in st.session_state:
    st.session_state['ocr_text'] = ""
if 'last_image_bytes' not in st.session_state:
    st.session_state['last_image_bytes'] = None

# Cargar el reader (cacheado)
with st.spinner("Cargando motor OCR (si es la primera vez, esto puede tardar)..."):
    reader = load_ocr_reader(lang_list=langs, use_gpu=use_gpu)

if uploaded_file is not None:
    # Leer imagen con PIL
    image = Image.open(uploaded_file).convert("RGB")

    # Mostrar la imagen
    st.image(image, caption="Imagen subida", use_column_width=True)

    # Guardar bytes en session_state para posibles interacciones futuras
    st.session_state['last_image_bytes'] = uploaded_file.getvalue()

    # Botón para ejecutar OCR
    if st.button("Extraer texto (OCR)"):
        # Preprocesamiento opcional: convierte a cv2 y realiza mejoras simples
        with st.spinner("Procesando imagen y ejecutando OCR..."):
            try:
                # Convertir a numpy para posible preprocesamiento
                img_cv = pil_to_cv2(image)

                # Ejemplo de preprocesamiento liviano que puede mejorar OCR:
                gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
                # opcional: aplicar umbral adaptativo si la imagen es ruidosa
                # thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                #                                cv2.THRESH_BINARY,11,2)
                # Aquí enviamos la imagen original (RGB) al reader:
                results = reader.readtext(np.array(image))

                extracted_text = ocr_to_text(results)
                st.session_state['ocr_text'] = extracted_text

                # Mostrar recuadros si el usuario lo pidió
                if show_boxes:
                    boxed_img = draw_boxes_on_image(image, results)
                    st.image(boxed_img, caption="Detecciones OCR", use_column_width=True)

                st.success("OCR completado.")
            except Exception as e:
                st.error(f"Ocurrió un error al ejecutar OCR: {e}")
else:
    st.info("Sube una imagen para comenzar. Puedes usar fotos de documentos, capturas de pantalla o fotos tomadas con el celular.")

# Mostrar texto extraído (persistente)
st.subheader("Texto extraído")
txt = st.text_area("Texto detectado por OCR (puedes editarlo):", value=st.session_state.get('ocr_text', ''), height=240)

# Guardar cambios manuales del text_area en session_state
if txt != st.session_state.get('ocr_text', ''):
    st.session_state['ocr_text'] = txt

# Botones utilitarios
col1, col2 = st.columns(2)
with col1:
    if st.button("Copiar texto al portapapeles (navegador)"):
        # Streamlit no tiene API nativa para portapapeles; indicamos al usuario que copie manualmente.
        st.info("Selecciona el texto en el área anterior y usa Ctrl+C / Cmd+C para copiarlo.")
with col2:
    if st.button("Limpiar texto extraído"):
        st.session_state['ocr_text'] = ""
        st.success("Texto limpiado. Sube otra imagen o vuelve a extraer.")

st.markdown("---")
st.caption("Módulo 1 listo. El texto extraído se guarda en st.session_state['ocr_text'] para usarlo en módulos posteriores.")
