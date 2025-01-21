import json
import os

SEPARATOR = "### NOVA_FATURA ###"

prompt_output_path = "prompts/"

def load_extraction_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_invoice_texts(invoice_folder):
    invoices = []
    for filename in sorted(os.listdir(invoice_folder)):
        if filename.endswith(".txt"):
            with open(os.path.join(invoice_folder, filename), "r", encoding="utf-8") as f:
                invoices.append(f"Arquivo: {filename}\n{f.read().strip()}")
    return invoices

def generate_prompt(config_path, invoice_folder):

    extraction_config = load_extraction_config(config_path)
    invoices = load_invoice_texts(invoice_folder)
    
    prompt = f"""
    Você é um assistente especializado em análise de faturas de energia elétrica.
    Sua tarefa é extrair informações de múltiplas faturas com base nos campos fornecidos.
    Cada fatura será separada pelo delimitador "{SEPARATOR}".

    ### Campos a serem extraídos:
    {json.dumps(extraction_config["fields_to_extract"], indent=4)}

    ### Faturas:
    {f"\n{SEPARATOR}\n".join(invoices)}

    Com base nas faturas fornecidas, extraia as informações e devolva um JSON estruturado para cada fatura, separados por "{SEPARATOR}".
    """.replace("{", "{{").replace("}", "}}").strip()
    return prompt.strip()                       

if __name__ == "__main__":
    config_path = "JSON_extract_configuration/Config_1.json"
    invoice_folder = "data/raw/preprocessed_text"
    
    if not os.path.exists(config_path):
        print(f"Erro: Configuração de extração não encontrada em {config_path}")
    elif not os.path.exists(invoice_folder):
        print(f"Erro: Pasta de faturas não encontrada em {invoice_folder}")
    else:
        prompt = generate_prompt(config_path, invoice_folder)
        prompt_output_path = "prompts/generatedprompt.txt"
        
        os.makedirs(os.path.dirname(prompt_output_path), exist_ok=True)
        with open(prompt_output_path, "w", encoding="utf-8") as f:
            f.write(prompt)
        
        print(f"✔ Prompt gerado e salvo em: {prompt_output_path}")
