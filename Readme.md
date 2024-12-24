# Conversor de Código-Fonte para PDF

## Descrição
Uma aplicação simples e intuitiva para converter arquivos de código-fonte em PDFs organizados e estilizados. Ideal para documentação, revisão de código ou apresentação.

## Funcionalidades
- Conversão de arquivos `.py`, `.java`, `.html`, entre outros, para PDF.
- Destaque de sintaxe para melhor visualização do código.
- Interface gráfica para seleção de pastas e arquivos.
- Opções de geração: texto simples ou indentado.

## Requisitos
- **Python 3.8 ou superior**
- Bibliotecas Python:
  - `ttkbootstrap`
  - `reportlab`
  - `pygments`
  - `pdfkit`

## Instalação
1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/conversor-pdf.git
   cd conversor-pdf
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure o ambiente:
   - Certifique-se de que o `wkhtmltopdf` está instalado para o uso do `pdfkit`.

   #### Instruções para instalar o `wkhtmltopdf`:
   - **Windows**: Baixe o instalador em [wkhtmltopdf.org](https://wkhtmltopdf.org/).
   - **Linux (Ubuntu/Debian)**:
     ```bash
     sudo apt install wkhtmltopdf
     ```
   - **macOS**:
     ```bash
     brew install wkhtmltopdf
     ```

## Uso
1. Inicie a aplicação:
   ```bash
   python src/main.py
   ```
2. Use a interface gráfica para:
   - Selecionar uma pasta.
   - Escolher os arquivos e pastas a incluir.
   - Gerar o PDF no formato desejado.

## Estrutura do Projeto
```plaintext
source-code-to-pdf/
├── src/                       # Código-fonte principal da aplicação
│   ├── config/                # Configurações gerais e constantes
│   ├── core/                  # Lógica de negócio e manipulação de arquivos
│   ├── pdf/                   # Lógica de geração de PDFs
│   └── ui/                    # Interface gráfica da aplicação
├── tests/                     # Testes automatizados
├── requirements.txt           # Dependências do projeto
├── README.md                  # Documentação principal do projeto
├── CONTRIBUTING.md            # Guia para contribuir no projeto
└── LICENSE                    # Licença do projeto
```

## Contribuição
Veja o arquivo [CONTRIBUTING.md](./CONTRIBUTING.md) para instruções detalhadas.

## Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](./LICENSE) para mais informações.

