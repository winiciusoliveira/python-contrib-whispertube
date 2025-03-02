import os
import tkinter as tk
import threading
import subprocess
from tkinter import filedialog, messagebox, scrolledtext, ttk
from funcs.ConverterAudio import baixar_raw_audio, converter_para_mp3
from funcs.PDF import txt_to_pdf
import whisper

def convert_to_mp3(audio_file):
    """Converte arquivos de áudio para MP3 caso não estejam nesse formato."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    audios_dir = os.path.join(base_dir, "audios")
    mp3_output_dir = os.path.join(audios_dir, "mp3")

    if not os.path.exists(mp3_output_dir):
        os.makedirs(mp3_output_dir)

    if not audio_file.lower().endswith(".mp3"):
        mp3_file = os.path.join(mp3_output_dir, os.path.basename(audio_file).rsplit('.', 1)[0] + ".mp3")

        comando = ["ffmpeg", "-i", audio_file, "-vn", "-ab", "192k", "-y", mp3_file]
        try:
            subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return mp3_file
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erro", f"Erro ao converter para MP3:\n{e.stderr.decode()}")
            return None
    return audio_file

def process_audio():
    """Executa o processamento do áudio em uma thread separada para evitar congelamento da interface."""
    threading.Thread(target=process_audio_thread, daemon=True).start()

def process_audio_thread():
    """Processa o áudio para transcrição e atualiza o progresso na interface."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    audios_dir = os.path.join(base_dir, "audios")
    transcribes_dir = os.path.join(base_dir, "transcribes")

    if use_file_var.get():
        audio_file = file_path_var.get()
        video_url = ""
    else:
        audio_file = ""
        video_url = url_var.get()

    if not audio_file and not video_url:
        messagebox.showerror("Erro", "Selecione um arquivo de áudio ou insira uma URL de vídeo.")
        return

    log_text.insert(tk.END, "Iniciando processo...\n")
    log_text.yview(tk.END)

    if video_url:
        log_text.insert(tk.END, "Baixando áudio...\n")
        log_text.yview(tk.END)
        raw_audio_path = baixar_raw_audio(video_url, audios_dir)

        if raw_audio_path:
            log_text.insert(tk.END, "Convertendo para MP3...\n")
            mp3_file = converter_para_mp3(raw_audio_path, os.path.join(audios_dir, "mp3"))
        else:
            messagebox.showerror("Erro", "Falha ao baixar o áudio.")
            return
    else:
        mp3_file = convert_to_mp3(audio_file)

    if mp3_file:
        log_text.insert(tk.END, "Carregando modelo Whisper...\n")
        log_text.yview(tk.END)
        top.update_idletasks()  # Atualiza a interface
        model = whisper.load_model("small")

        log_text.insert(tk.END, "Iniciando transcrição...\n")
        log_text.yview(tk.END)
        top.update_idletasks()

        result = model.transcribe(mp3_file)
        total_duration = result["segments"][-1]["end"] if "segments" in result and result["segments"] else 1

        txt_file = os.path.join(transcribes_dir, os.path.basename(mp3_file).rsplit('.', 1)[0] + ".txt")

        progress_bar["value"] = 0
        for segment in result.get("segments", []):
            progress = int((segment["end"] / total_duration) * 100)
            log_text.insert(tk.END, f"Transcrição em andamento: {progress}%\n")
            log_text.yview(tk.END)
            top.update_idletasks()  # Atualiza a interface

            progress_bar["value"] = progress
            top.update_idletasks()

            with open(txt_file, "a", encoding="utf-8") as f:
                f.write(segment["text"] + "\n")

        log_text.insert(tk.END, "Gerando PDF...\n")
        txt_to_pdf(txt_file)

        progress_bar["value"] = 100
        top.update_idletasks()

        messagebox.showinfo("Sucesso", "Processo concluído com sucesso!")
        log_text.insert(tk.END, "Processo concluído com sucesso!\n")
        log_text.yview(tk.END)

def select_file():
    """Abre o seletor de arquivos para escolher um arquivo de áudio."""
    filename = filedialog.askopenfilename(filetypes=[("Arquivos de áudio", "*.mp3;*.m4a;*.wav;*.ogg;*.flac")])
    if filename:
        file_path_var.set(filename)

def toggle_file_entry():
    """Habilita ou desabilita os campos de entrada dependendo do checkbox."""
    if use_file_var.get():
        file_entry.config(state="normal")
        url_entry.config(state="disabled")
    else:
        file_entry.config(state="disabled")
        url_entry.config(state="normal")

def on_enter(event):
    """Executa a função ao pressionar Enter."""
    process_audio()

def on_mouse_scroll(event):
    """Permite rolagem com o scroll do mouse."""
    log_text.yview_scroll(-1 if event.delta > 0 else 1, "units")

# Criando interface
top = tk.Tk()
top.title("Transcritor de Áudio")
top.geometry("500x500")
top.resizable(False, False)

tk.Label(top, text="Escolha um arquivo de áudio ou insira uma URL").pack(pady=5)

# Checkbox para escolher entre arquivo e URL
use_file_var = tk.BooleanVar(value=False)
file_checkbox = tk.Checkbutton(top, text="Usar arquivo de áudio", variable=use_file_var, command=toggle_file_entry)
file_checkbox.pack()

# Input para arquivo de áudio
file_path_var = tk.StringVar()
file_entry = tk.Entry(top, textvariable=file_path_var, width=40, state="disabled")
file_entry.pack(pady=5)
tk.Button(top, text="Selecionar Arquivo", command=select_file).pack()

# Input para URL
url_var = tk.StringVar()
url_entry = tk.Entry(top, textvariable=url_var, width=40)
url_entry.pack(pady=5)

# Dica para diretório
tk.Label(top, text="Dica: Selecione um arquivo de áudio ou use uma URL", fg="gray").pack(pady=2)

# Botão de processar
tk.Button(top, text="Iniciar Transcrição", command=process_audio).pack(pady=10)

# Barra de progresso
progress_bar = ttk.Progressbar(top, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

# Área de log
log_text = scrolledtext.ScrolledText(top, height=10, width=55)
log_text.pack(pady=10)

# Bind para Enter e Scroll
top.bind("<Return>", on_enter)
top.bind("<MouseWheel>", on_mouse_scroll)

# Iniciar GUI
top.mainloop()
