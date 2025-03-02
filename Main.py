import os
import sys
from funcs.ConverterAudio import baixar_raw_audio, converter_para_mp3
from funcs.PDF import txt_to_pdf
from funcs.Transcrever import transcrever_audio

if __name__ == "__main__":
    audios_dir = "audios"
    transcribes_dir = "transcribes"
    local_audio_dir = os.path.join(audios_dir, "local")
    mp3_audio_dir = os.path.join(audios_dir, "mp3")

    # Verifica se o usuário passou um argumento (arquivo ou URL)
    if len(sys.argv) > 1:
        input_data = sys.argv[1]
    else:
        input_data = input("Digite a URL do vídeo ou o caminho do arquivo de áudio: ").strip()

    # Caso seja um arquivo local
    if os.path.exists(input_data):
        audio_file = input_data
        print(f"Processando arquivo local: {audio_file}")
        mp3_final = converter_para_mp3(audio_file, mp3_audio_dir)
    else:
        video_url = input_data
        print(f"Baixando áudio do vídeo: {video_url}")
        raw_audio_path = baixar_raw_audio(video_url, audios_dir)
        if raw_audio_path:
            print("Convertendo para MP3...")
            mp3_final = converter_para_mp3(raw_audio_path, mp3_audio_dir)
        else:
            print("Erro no download do áudio.")
            sys.exit(1)

    # Se a conversão ou download funcionou, inicia a transcrição
    if mp3_final:
        print("Iniciando transcrição...")
        txt_file = transcrever_audio(mp3_final, transcribes_dir)

        if txt_file:
            print("Gerando PDF...")
            txt_to_pdf(txt_file)
            print("Processo concluído com sucesso!")
        else:
            print("Erro na transcrição.")
    else:
        print("Erro ao converter o arquivo para MP3.")
