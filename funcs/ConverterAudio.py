# ConverterAudio.py

import os
import yt_dlp
import subprocess
from funcs.Utils import formatar_nome

def baixar_raw_audio(video_url, output_dir):
    """Baixa somente o áudio no formato original sem conversão e organiza em pastas específicas."""
    webm_output_dir = os.path.join(output_dir, "webm")
    if not os.path.exists(webm_output_dir):
        os.makedirs(webm_output_dir)

    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        title = info_dict.get('title', 'audio')
        ext = info_dict.get('ext', 'webm')
        formatted_title = formatar_nome(title)
        output_file = os.path.join(webm_output_dir, f"{formatted_title}.{ext}")

    ydl_opts = {
        'format': 'bestaudio',    # Pega só o melhor áudio sem extrair
        'outtmpl': output_file,    # Força o nome do arquivo formatado
        'postprocessors': [],     # Nenhum postprocessamento
        'nopart': True,          # Não criar arquivos .part
        'windowsfilenames': True  # Ajusta nomes para Windows
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    return output_file if os.path.exists(output_file) else None

def converter_para_mp3(input_file, output_dir):
    """Converte o áudio baixado para MP3 usando FFmpeg e organiza em pastas específicas."""
    if input_file is None or not os.path.exists(input_file):
        print("Erro: Arquivo de áudio não encontrado!")
        return None

    mp3_output_dir = os.path.join(output_dir, "mp3")
    if not os.path.exists(mp3_output_dir):
        os.makedirs(mp3_output_dir)

    mp3_file = os.path.join(mp3_output_dir, os.path.basename(input_file).rsplit('.', 1)[0] + ".mp3")
    comando = [
        "ffmpeg",
        "-i", input_file,
        "-vn",
        "-ab", "192k",
        "-y", mp3_file  # '-y' para sobrescrever se já existir
    ]
    subprocess.run(comando, check=True)
    return mp3_file