# Gemini AI na Raspberry Pi Pico W

Utilização da API Gemini 1.5 Flash na Raspberry Pi Pico W para criação de módulos como tradutor, quiz personalizado e chat aberto com o próprio Gemini. Este código também possui uma interface de teclado QWERTY virtual.

## 🚀 Funcionalidades

- **Tradutor**: Tradução de texto entre diversos idiomas usando Gemini AI
- **Quiz Personalizado**: Geração de perguntas personalizadas sobre qualquer tópico
- **Chat Aberto**: Conversação livre com o Gemini AI
- **Teclado QWERTY**: Interface de entrada de texto simulada
- **WiFi Manager**: Gerenciamento automático de conexão WiFi
- **Sistema Modular**: Arquitetura modular para fácil manutenção

## 📋 Requisitos

### Hardware
- Raspberry Pi Pico W
- Conexão WiFi ativa
- (Opcional) Display para melhor visualização

### Software
- MicroPython instalado no Pico W
- Biblioteca `urequests` para requisições HTTP
- Chave API do Google Gemini

## 🔧 Instalação

1. **Instale o MicroPython no Pico W**
   - Baixe o firmware MicroPython para Pico W
   - Instale usando o Thonny IDE ou outro método preferido

2. **Clone/baixe este repositório**
   ```bash
   git clone https://github.com/GabrielLazuli/IA-na-Raspberry-pi-pico-w-.git
   ```

3. **Configure as credenciais**
   - Copie `config_example.py` para `config.py`
   - Edite `config.py` com suas credenciais:
     - WIFI_SSID: Nome da sua rede WiFi
     - WIFI_PASSWORD: Senha da sua rede WiFi
     - GEMINI_API_KEY: Sua chave API do Gemini

4. **Obtenha a chave API do Gemini**
   - Visite [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Crie uma conta e gere sua chave API
   - Cole a chave no arquivo `config.py`

5. **Transfira os arquivos para o Pico W**
   - Use Thonny IDE ou outra ferramenta para copiar todos os arquivos `.py` para o Pico W

6. **Instale dependências (se necessário)**
   ```python
   import upip
   upip.install('urequests')
   ```

## 🎮 Como Usar

1. **Conecte o Pico W ao computador**
2. **Execute o arquivo principal**:
   ```python
   exec(open('main.py').read())
   ```
3. **Siga as instruções no terminal**:
   - O sistema irá conectar ao WiFi automaticamente
   - Testará a conexão com a API Gemini
   - Apresentará o menu principal

### Menu Principal
- **1. Tradutor**: Traduzir texto entre idiomas
- **2. Quiz Personalizado**: Gerar e responder quiz sobre qualquer tópico  
- **3. Chat com Gemini**: Conversar livremente com a IA
- **4. Status do Sistema**: Ver informações do sistema
- **5. Configurações**: Acessar configurações avançadas

## 📁 Estrutura do Projeto

```
IA-na-Raspberry-pi-pico-w-/
├── main.py                 # Aplicação principal
├── config.py               # Configurações (crie a partir do exemplo)
├── config_example.py       # Exemplo de configuração
├── wifi_manager.py         # Gerenciador de WiFi
├── gemini_client.py        # Cliente da API Gemini
├── qwerty_keyboard.py      # Interface de teclado QWERTY
├── translator.py           # Módulo tradutor
├── quiz_module.py          # Módulo de quiz
├── chat_module.py          # Módulo de chat
├── requirements.txt        # Dependências
└── README.md              # Este arquivo
```

## 🔍 Módulos Detalhados

### Tradutor
- Tradução automática entre 10+ idiomas
- Detecção automática do idioma de origem
- Modo de tradução rápida para pares comuns
- Interface intuitiva

### Quiz Personalizado
- Geração de perguntas sobre qualquer tópico
- 3 níveis de dificuldade (fácil, médio, difícil)
- Sistema de pontuação
- Histórico de perguntas
- Explicações detalhadas

### Chat com Gemini
- Conversação contextual com memória
- Modo simples sem contexto
- Perguntas rápidas predefinidas
- Exportação de conversas
- Estatísticas da sessão

### Teclado QWERTY
- Layout QWERTY completo
- Suporte a maiúsculas/minúsculas
- Teclas especiais (Shift, Caps Lock, etc.)
- Simulação para testes

## ⚙️ Configurações Avançadas

### WiFi
- Reconexão automática
- Status detalhado da conexão
- Teste de conectividade

### API Gemini
- Configuração de temperatura da IA
- Limites de tokens
- Configurações de segurança
- Teste de conectividade

### Sistema
- Modo debug
- Gerenciamento de memória
- Monitoramento de status
- Reinicialização remota

## 🐛 Solução de Problemas

### Erro de Conexão WiFi
- Verifique SSID e senha em `config.py`
- Confirme que o Pico W está dentro do alcance
- Teste com outras redes WiFi

### Erro da API Gemini
- Verifique se a chave API está correta
- Confirme que a API está ativa na sua conta Google
- Teste a conectividade com a internet

### Falta de Memória
- Use `gc.collect()` regularmente
- Reduza o limite de histórico de conversas
- Reinicie o sistema se necessário

### Biblioteca urequests não encontrada
```python
import upip
upip.install('urequests')
```

## 📊 Especificações Técnicas

- **Linguagem**: MicroPython
- **Plataforma**: Raspberry Pi Pico W
- **API**: Google Gemini 1.5 Flash
- **Protocolos**: HTTP/HTTPS, WiFi
- **Memória**: Otimizado para microcontroladores
- **Interface**: Terminal/Serial

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📝 Licença

Este projeto é open source. Veja o arquivo LICENSE para detalhes.

## 👥 Autor

- **Gabriel Lazuli** - Desenvolvimento inicial

## 🙏 Agradecimentos

- Google AI Studio pela API Gemini
- Comunidade MicroPython
- Raspberry Pi Foundation
- Contribuidores do projeto

## 📞 Suporte

Para suporte, abra uma issue no GitHub ou entre em contato através dos canais oficiais do projeto.

---

**Nota**: Este projeto é educacional e demonstrativo. Use responsavelmente e respeite os limites da API Gemini.  
