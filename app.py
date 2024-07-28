
import streamlit as st
import yt_dlp
import os
import shutil

# Funciones
def extraer_audio(url):
    """Extrae el audio de un video de YouTube y lo convierte a MP3."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [download_progress_hook],  # Hook para el progreso
        'verbose': True,   # Muestra información detallada del proceso
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            st.info("Iniciando descarga...")
            ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        st.error(f"Error al extraer el audio: {e}")

def download_progress_hook(d):
    """Función hook para monitorizar el progreso de descarga."""
    if d['status'] == 'downloading':
        st.write(f"Descargando: {d['_percent_str']} - Velocidad: {d['_speed_str']} - Tiempo restante: {d['_eta_str']}")
    elif d['status'] == 'finished':
        st.write(f"Descarga completada, archivo guardado en: {d['filename']}")
    elif d['status'] == 'error':
        st.error("Error durante la descarga")

def obtener_nombre_disponible(ruta):
    """Devuelve un nombre de archivo disponible añadiendo un sufijo numérico si es necesario."""
    if not os.path.exists(ruta):
        return ruta
    base, extension = os.path.splitext(ruta)
    counter = 1
    new_ruta = f"{base}_{counter}{extension}"
    while os.path.exists(new_ruta):
        counter += 1
        new_ruta = f"{base}_{counter}{extension}"
    return new_ruta

# Configuración de la interfaz de Streamlit
st.title("Descargar Audio de YouTube")

# Ruta de la carpeta local donde se guardarán los archivos
carpeta_local = './audios'

# Crear la carpeta si no existe
if not os.path.exists(carpeta_local):
    os.makedirs(carpeta_local)

# Solicitar la URL del video
url = st.text_input("Introduce la URL del video de YouTube:")

if st.button("Descargar Audio"):
    if url:
        st.write(f"Procesando URL: {url}")
        # Extraer el audio
        extraer_audio(url)

        # Verificar el directorio de trabajo actual
        current_directory = os.getcwd()
        st.write(f"Directorio de trabajo actual: {current_directory}")

        # Verificar que el archivo de audio se haya descargado
        st.write("Verificando archivos en el directorio actual...")
        archivos = os.listdir()
        for file in archivos:
            st.write(file)

        # Encontrar el archivo de audio descargado
        audio_file = None
        for file in archivos:
            if file.endswith(".mp3"):
                audio_file = file
                break

        # Mover el archivo de audio a la carpeta local
        if audio_file:
            destino_audio = os.path.join(carpeta_local, audio_file)
            destino_audio = obtener_nombre_disponible(destino_audio)
            st.write(f"Moviendo archivo {audio_file} a {destino_audio}...")
            shutil.move(audio_file, destino_audio)
            st.success(f"Archivo de audio movido a {destino_audio}")

            # Crear un enlace de descarga
            with open(destino_audio, "rb") as file:
                btn = st.download_button(
                    label="Descargar archivo de audio",
                    data=file,
                    file_name=os.path.basename(destino_audio),
                    mime="audio/mpeg"
                )
        else:
            st.error("No se encontró el archivo de audio.")
    else:
        st.warning("Por favor, introduce una URL de YouTube válida.")
