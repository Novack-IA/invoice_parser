import os
import re

data_folder = "data/raw/extracted_text/"
output_folder = "data/raw/preprocessed_text/"

os.makedirs(output_folder, exist_ok=True)

def clean_text(text):
    """Remove caracteres invisíveis e padroniza o texto sem remover quebras de linha."""
    text = text.replace("\xa0", " ")  # Remove espaços não quebráveis
    text = text.replace("\u200b", "")  # Remove caracteres invisíveis
    text = re.sub(r'[ ]{2,}', ' ', text)  # Substitui múltiplos espaços por um único
    return text.strip()

def normalize_numbers(text):
    """Padroniza números no formato correto (exemplo: vírgulas para pontos decimais)."""
    return re.sub(r'(\d+),(\d+)', r'\1.\2', text)

def preprocess_file(input_path, output_path):
    """Processa um arquivo de texto extraído, limpando e normalizando os dados sem remover quebras de linha."""
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    processed_lines = [normalize_numbers(clean_text(line)) for line in lines]
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines("\n".join(processed_lines))
    
    print(f"✔ Texto preprocessado salvo em: {output_path}")

def process_all_files():
    """Processa todos os arquivos na pasta de extração e salva os textos preprocessados."""
    for filename in os.listdir(data_folder):
        if filename.endswith(".txt"):
            input_path = os.path.join(data_folder, filename)
            output_path = os.path.join(output_folder, filename)
            preprocess_file(input_path, output_path)

if __name__ == "__main__":
    process_all_files()
