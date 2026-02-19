# 🤖 Clarence AI - O assistente Clippy ATUALIZADO 100% 2026 
Clarence é um widget flutuante desenvolvido em **Python** e **PyQt6**, integrado à API da **OpenAI**. O projeto foca em uma interface minimalista, responsiva e com processamento assíncrono.

## ✨ Funcionalidades
- **Interface Adaptável**: Alterna entre um ícone circular minimalista e uma janela de chat completa.
- **Non-blocking UI**: Uso de `QThread` para garantir que a interface nunca trave durante as requisições.
- **Glassmorphism Design**: Estilo moderno com transparências e bordas arredondadas.
- **Draggable**: Pode ser movido para qualquer canto da tela.

## 🚀 Tecnologias
- Python 3.x
- PyQt6 (Interface Gráfica)
- OpenAI API (Inteligência Artificial)
- Python-dotenv (Gestão de variáveis de ambiente)

## 🛠️ Como instalar
1. Clone o repositório: `git clone https://github.com/seu-usuario/clarence-ai.git`
2. Instale as dependências: `pip install -r requirements.txt`
3. Crie um arquivo `.env` e adicione sua `OPENAI_API_KEY`.
4. Execute: `python main.py`