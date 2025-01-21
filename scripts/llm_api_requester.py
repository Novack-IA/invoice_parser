import os
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence

SEPARATOR = "### NOVA_FATURA ###"

llm = ChatOpenAI(model_name="o1-mini", temperature=0.2, max_tokens=3000)

def process_llm_response(prompt_path, output_folder):
    """Processa o prompt, envia a requisição ao LLM e salva os JSONs de saída."""

    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_text = f.read()
    
    prompt = PromptTemplate(template=prompt_text, input_variables=[])

    chain = prompt | llm

    response = chain.invoke({})

    json_blocks = response.split(SEPARATOR)

    os.makedirs(output_folder, exist_ok=True)

    for i, json_text in enumerate(json_blocks):
        json_text = json_text.strip()
        if json_text:
            try:
                parsed_json = json.loads(json_text) 
                file_name = f"{output_folder}/invoice_{i+1}.json"
                with open(file_name, "w", encoding="utf-8") as f:
                    json.dump(parsed_json, f, indent=4)
                print(f"✔ JSON salvo: {file_name}")
            except json.JSONDecodeError:
                print(f"⚠ Erro ao processar JSON da fatura {i+1}: {json_text}")

if __name__ == "__main__":
    prompt_path = "prompts/generatedprompt.txt"
    output_folder = "data/raw/processed"
    
    if not os.path.exists(prompt_path):
        print(f"Erro: Arquivo de prompt não encontrado em {prompt_path}")
    else:
        process_llm_response(prompt_path, output_folder)
