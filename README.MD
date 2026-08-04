# Gerador de Tabelas de Redes e Sub-redes IPv4

Um script utilitário em Python para calcular e listar informações detalhadas sobre redes e sub-redes IPv4. A ferramenta recebe um IP com seu prefixo CIDR e gera automaticamente um relatório em Markdown contendo a máscara de rede, IP da rede, intervalo de hosts válidos e endereço de broadcast.

## Funcionalidades

- Cálculo automático dos parâmetros da rede (Network, Broadcast, Range de Hosts).
- Suporte para divisão de redes (Subnetting) especificando um novo prefixo CIDR.
- Exportação automatizada dos resultados para um documento Markdown.

## Pré-requisitos

- **Python 3.x** instalado no seu sistema.
- O script utiliza exclusivamente bibliotecas nativas do Python (`ipaddress`, `argparse`, `sys`), dispensando a instalação de pacotes de terceiros (não precisa de `pip install`).

## Como utilizar

O script é uma aplicação de interface de linha de comando (CLI). Navegue até a pasta do projeto no seu terminal e execute:

```bash
python nome_do_script.py <IP_CIDR> [--novo_cidr NOVO_PREFIXO]
```

*(Substitua `nome_do_script.py` pelo nome real do arquivo Python, como `ip-address-test.py`)*

### Argumentos da Linha de Comando

- `ip_entrada` (**Obrigatório**): Endereço IP base acompanhado do seu prefixo CIDR. 
  - *Exemplo:* `172.16.0.1/12`
- `--novo_cidr` (**Opcional**): Um valor inteiro representando a nova máscara de rede. Deve ser obrigatoriamente **maior** que o prefixo original. É usado para fazer o cálculo de múltiplas sub-redes.

---

### Exemplos Práticos

**1. Mapeamento de uma rede padrão:**
Para calcular as informações de uma única rede `/24`:
```bash
python ip-address-test.py 192.168.0.1/24
```

**2. Subnetting (Dividindo a rede):**
Para pegar a super-rede `172.16.0.0/12` e descobrir todas as sub-redes que cabem nela usando a máscara `/16`:
```bash
python ip-address-test.py 172.16.0.1/12 --novo_cidr 16
```

**3. Visualizando a Ajuda:**
Para ver as orientações de uso direto no terminal:
```bash
python ip-address-test.py -h
```

## Sobre o Arquivo de Saída

As tabelas geradas pelo script são salvas automaticamente em um arquivo de formato Markdown (`.md`) no diretório de execução. 

> **Aviso ao Desenvolvedor:** Como as versões anteriores deste script utilizavam o arquivo `README.MD` como destino de gravação, certifique-se de alterar as linhas de salvamento no código para algo como `saida_redes.md` ou `relatorio.md`. Dessa forma, o programa não vai sobrescrever as instruções deste documento a cada execução!