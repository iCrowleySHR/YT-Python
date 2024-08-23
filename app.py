import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp as ytdlp
import moviepy.editor as mp
import os

def download_video():
    url = url_entry.get()
    output_format = format_var.get()
    
    if not url:
        messagebox.showwarning("Aviso", "Por favor, insira o link do YouTube.")
        return
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best' if output_format == 'mp3' else 'best',
            'outtmpl': os.path.join(os.getcwd(), '%(title)s.%(ext)s'),
        }
        
        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info_dict)
            
            if output_format == 'mp3' and not file_name.endswith('.mp3'):
                mp4_file_path = file_name
                mp3_file_path = mp4_file_path.replace('.mp4', '.mp3')
                
                audio_clip = mp.AudioFileClip(mp4_file_path)
                audio_clip.write_audiofile(mp3_file_path)
                audio_clip.close()
                
                os.remove(mp4_file_path)
                
                messagebox.showinfo("Sucesso", f'Áudio MP3 baixado com sucesso: {mp3_file_path}')
            else:
                messagebox.showinfo("Sucesso", f'Vídeo baixado com sucesso: {file_name}')
    
    except Exception as e:
        messagebox.showerror("Erro", f'Erro ao baixar o vídeo: {e}')

# Configurando a interface gráfica
root = tk.Tk()
root.title("YouTube Video Downloader")

# Link do YouTube
tk.Label(root, text="Link do YouTube:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Opções de formato
tk.Label(root, text="Formato:").grid(row=1, column=0, padx=10, pady=10)
format_var = tk.StringVar(value="mp4")
tk.Radiobutton(root, text="MP4", variable=format_var, value="mp4").grid(row=1, column=1, sticky="w", padx=10)
tk.Radiobutton(root, text="MP3", variable=format_var, value="mp3").grid(row=1, column=1, padx=10)

# Botão para baixar
download_button = tk.Button(root, text="Baixar", command=download_video)
download_button.grid(row=2, column=0, columnspan=2, pady=20)

# Inicia o loop principal
root.mainloop()
