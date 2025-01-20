import os
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import threading
import subprocess

# Inicializar corretamente o TkinterDnD
root = TkinterDnD.Tk()  # IMPORTANTE: Inicializar TkinterDnD corretamente
root.title("Processador de Faturas")
root.geometry("1000x500")

# Criar as pastas caso não existam
data_folder = "data/raw/invoices/"
processed_folder = "data/raw/processed/"
os.makedirs(data_folder, exist_ok=True)
os.makedirs(processed_folder, exist_ok=True)

def process_files():
    """Executa o pipeline para processar os PDFs e gerar JSONs."""
    try:
        messagebox.showinfo("Processamento", "Iniciando extração de texto...")
        subprocess.run(["python", "scripts/extract_text.py"], check=True)

        messagebox.showinfo("Processamento", "Preprocessando texto extraído...")
        subprocess.run(["python", "scripts/preprocess_text.py"], check=True)

        messagebox.showinfo("Processamento", "Gerando prompts e enviando para GPT-4o...")
        subprocess.run(["python", "scripts/llm_api_requester.py"], check=True)

        messagebox.showinfo("Sucesso", "Faturas processadas com sucesso! Os JSONs foram gerados em data/raw/processed/")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro no processamento: {str(e)}")

def on_drop(event):
    """Manipula arquivos arrastados para a interface."""
    files = root.tk.splitlist(event.data)  # Correção para capturar múltiplos arquivos
    for file_path in files:
        file_path = file_path.strip('{}')  # Remover {} ao redor do caminho (Windows)
        if file_path.lower().endswith(".pdf"):
            shutil.move(file_path, data_folder)
            messagebox.showinfo("Arquivo Recebido", f"Fatura movida para {data_folder}")

    threading.Thread(target=process_files).start()

def open_processed_folder():
    """Abre a pasta onde os JSONs processados são salvos."""
    os.startfile(processed_folder) if os.name == 'nt' else subprocess.call(["open", processed_folder])

# Criar interface gráfica
label = tk.Label(root, text="Arraste e solte os PDFs aqui", font=("Arial", 14))
label.pack(pady=20)

frame = tk.Frame(root, width=400, height=100, bg="#ddd")
frame.pack(pady=10)
frame.drop_target_register(DND_FILES)  # Registrar como alvo de arrastar e soltar
frame.dnd_bind("<<Drop>>", on_drop)  # Correção: usar "<<Drop>>" ao invés de "<Drop>"

button = tk.Button(root, text="Abrir Pasta de JSONs", command=open_processed_folder)
button.pack(pady=20)

root.mainloop()
