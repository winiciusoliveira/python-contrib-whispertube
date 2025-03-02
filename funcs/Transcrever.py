# Transcrever.py

import os
import whisper


def transcrever_audio(mp3_file, output_dir):
    """Transcreve o áudio usando Whisper e salva em um arquivo TXT, mostrando progresso."""
    if mp3_file is None or not os.path.exists(mp3_file):
        print("Erro: Arquivo MP3 não encontrado!")
        return None

    txt_output_dir = os.path.join(output_dir, "txt")
    if not os.path.exists(txt_output_dir):
        os.makedirs(txt_output_dir)

    transcription_file = os.path.join(txt_output_dir, os.path.basename(mp3_file).rsplit('.', 1)[0] + ".txt")

    print("Carregando modelo Whisper...")
    model = whisper.load_model("small")

    print("Iniciando transcrição...")
    result = model.transcribe(mp3_file, verbose=False)

    total_duration = result['segments'][-1]['end'] if 'segments' in result and result['segments'] else 1
    processed_time = 0

    with open(transcription_file, "w", encoding="utf-8") as f:
        for segment in result.get("segments", []):
            f.write(segment["text"] + " ")
            processed_time = segment["end"]
            progress = (processed_time / total_duration) * 100
            print(f"Progresso: {progress:.2f}% concluído...", end="\r")

    print("\nTranscrição concluída e salva em:", transcription_file)
    return transcription_file
