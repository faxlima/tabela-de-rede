import ipaddress

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

    return list(network.subnets(new_prefix=novo_prefixo))

ip_entrada = "192.168.1.10/24"
cidr_entrada = 26
subredes = listarSubredes(ip_entrada,cidr_entrada)

# Criando o arquivo com a primeira página
markdown_text = f"""
# Tabela de Rede/Sub-rede
> Importante!  
> Não existe sub-rede ímpar, nem broadcast par.  

IP de Entrada: `{ip_entrada}`  
Novo pré-fixo: `{cidr_entrada}`

"""
saveMarkdown("README.MD", markdown_text,"w")

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
|Qtd IPs|{tabela['total_ips']}|

    """

    saveMarkdown("README.MD", markdown_text, 'a')