# Projeto docstring\_pdf\_converter

O `docstring\_pdf\_converter` é uma ferramenta que gera um PDF a partir das docstrings de um módulo Python. Ele extrai as docstrings de classes e funções e as organiza em um documento PDF formatado, facilitando a documentação e a leitura das descrições do código.

## Funcionalidades

- Extrai docstrings de classes e funções de um módulo Python.
- Gera um PDF formatado com as docstrings extraídas.
- Cria uma capa personalizada para o PDF com título, subtítulo, instituição, cidade e ano.

## Pacotes Utilizados

- `fpdf`: Biblioteca para geração de PDFs em Python.
- `setuptools`: Utilizado para empacotamento e distribuição do projeto.

## Benefícios

- Facilita a documentação de projetos Python, gerando um PDF com as descrições das classes e funções.
- Melhora a legibilidade e a organização das docstrings.
- Automatiza o processo de criação de documentação, economizando tempo e esforço.

## Instalação

Você pode instalar o `docstring\_pdf\_converter` diretamente do PyPI usando o `pip`:

```sh
pip install docstring_pdf_converter
```

## Uso

Após a instalação, você pode usar a ferramenta diretamente da linha de comando:

```sh
docstring-pdf-converter
```

O comando acima irá solicitar algumas informações para a capa do PDF, como título, subtítulo, instituição e cidade. Em seguida, ele irá gerar um PDF com as docstrings extraídas do módulo especificado.

## Exemplo de Uso

1. Execute o comando:

    ```sh
    docstring-pdf-converter
    ```

2. Insira as informações solicitadas:

    ```sh
    Digite o título do documento: Documentação do projeto
    Digite o subtítulo do documento: Conversão de docstring para PDF
    Digite a instituição (deixe em branco se não houver): Minha Instituição
    Digite a cidade: São Paulo
    ```

3. O PDF `documentacao_completa.pdf` será gerado no diretório atual com as docstrings extraídas e formatadas.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests no repositório do projeto.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
