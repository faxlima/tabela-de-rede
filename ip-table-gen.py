import ipaddress
import argparse # Biblioteca adicionada para gerenciar os argumentos via linha de comando
import sys
import itertools


OUTPUT_FILE = '../../05-tabela-subrede.md'
TRAVA_SEGURANCA = 7 # Quantidade máxima de tabelas que podem ser geradas

def tabelaDeRede(ip_cidr: str):
    network = ipaddress.ip_network(ip_cidr, strict=False)

    return {
        "IP":ip_cidr,
        "rede": str(network.network_address),
        "broadcast": str(network.broadcast_address),
        "prefixo": network.prefixlen,
        "mascara": str(network.netmask),
        "total_ips": network.num_addresses,
        "hosts_validos": (
            str(next(network.hosts())),
            str(list(network.hosts())[-1])
        ) if network.num_addresses > 2 else None
    }

def saveMarkdown(filename, content, modo):
    """Saves a string of Markdown content to a file."""
    try:
        # w - grava um arquivo novo
        # a - adiciona linhas
        with open(filename, mode=modo, encoding='utf-8') as f:
            f.write(content)
            #print(f"Successfully saved content to {filename}")
    except IOError as e:
        print(f"Error saving file: {e}")

def listarSubredes(ip_cidr: str, novo_prefixo: int):
    network = ipaddress.ip_network(ip_cidr, strict=False)

    if novo_prefixo < network.prefixlen:
        raise ValueError("O novo prefixo deve ser maior que o prefixo original.")

    return network.subnets(new_prefix=novo_prefixo)

# Colocar a execução principal dentro do bloco __main__ é uma boa prática em Python
if __name__ == "__main__":
    # 1. Inicializa o parser
    parser = argparse.ArgumentParser(description="Gera tabelas em Markdown para Redes e Sub-redes IPv4.")

    # 2. Define o argumento obrigatório (ip_entrada)
    parser.add_argument(
        "ip_entrada", 
        type=str, 
        help="Endereço IP com seu prefixo CIDR. Ex: 172.16.0.1/12"
    )

    # 3. Define um argumento opcional para o caso de querer calcular sub-redes menores
    parser.add_argument(
        "--novo_cidr", 
        type=int, 
        help="Opcional: Novo prefixo (maior que o original) para calcular sub-redes.",
        default=None
    )

    # 4. Processa os argumentos da linha de comando
    args = parser.parse_args()
    ip_entrada = args.ip_entrada

    try:
        rede_base = ipaddress.ip_network(ip_entrada, strict=False)
        cidr_entrada = args.novo_cidr if args.novo_cidr is not None else rede_base.prefixlen

        # 1. Calcula a quantidade total de redes esperadas
        qtd_esperada = 2 ** (cidr_entrada - rede_base.prefixlen) if cidr_entrada > rede_base.prefixlen else 1
        houve_corte = qtd_esperada > TRAVA_SEGURANCA

        # 2. Gera o iterador de sub-redes
        iterador_subredes = listarSubredes(ip_entrada, cidr_entrada)

        # 3. Puxa no máximo as primeiras X (TRAVA_SEGURANCA) redes usando o islice de forma segura
        subredes = list(itertools.islice(iterador_subredes, TRAVA_SEGURANCA))

    except ValueError as e:
        print(f"Erro ao processar o IP ou CIDR: {e}")
        sys.exit(1)

    # Criando o arquivo com a primeira página
    markdown_text = f"""
Gerado pelo `app/tabela-de-rede/ip-table-gen.py`.  
# Tabela de Rede/Sub-rede
> Importante!  
> Não existe sub-rede ímpar, nem broadcast par.  

IP de Entrada: `{ip_entrada}`  
Novo pré-fixo: `{cidr_entrada}`

Total de tabelas de redes solicitadas: `{2 ** (cidr_entrada - rede_base.prefixlen)}`.
Total de tabelas de redes geradas pela trava de segurança: `{TRAVA_SEGURANCA}`.

"""
    saveMarkdown(OUTPUT_FILE, markdown_text, "w")

    for index, s in enumerate(subredes):
        tabela = tabelaDeRede(s)
        print(f"IP: {tabela['IP']}")

        if(len(subredes)==1):
            tipo = "Rede"
        else:
            tipo = "Sub-rede"

        markdown_text = f"""
## {tipo} {index}
|Item      |Valor           |
|----------|----------------|
|IP        |{tabela['IP']}  |
|Máscara da Rede|{tabela['mascara']}|
|IP da Rede|{tabela['rede']}|
|Hosts|{tabela['hosts_validos'][0]} até {tabela['hosts_validos'][1]}|
|Broadcast|{tabela['broadcast']}|
|Qtd IPs|{tabela['total_ips']:,}|

"""
        saveMarkdown(OUTPUT_FILE, markdown_text, 'a')