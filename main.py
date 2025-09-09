from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import network
import urequests
import ujson
import time

# --- DEFINIÇÃO DOS PINOS ---
# (Seu código aqui permanece igual)
I2C_SDA_PIN = 14
I2C_SCL_PIN = 15
BUTTON_A_PIN = 5
BUTTON_B_PIN = 6
JOYSTICK_X_PIN = 26
JOYSTICK_Y_PIN = 27
LED_PIN = 12

ledR = Pin(13, Pin.OUT)
ledG = Pin(11, Pin.OUT)
ledB = Pin(12, Pin.OUT)

WIFI_SSID = "Reinan"
WIFI_PASSWORD = "rree1517"
API_KEY = "insira sua chave aqui"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

# --- Funções ---

def connect_wifi():
    # (Sua função aqui permanece igual)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        print("Conectando ao Wi-Fi...")
        time.sleep(1)
    print("Conectado! IP:", wlan.ifconfig()[0])
    ledR.on()
    time.sleep(0.5)
    ledR.off()
    return wlan

### NOVO ###
# --- PASSO 1: A FUNÇÃO PARA EXIBIR TEXTO LONGO ---
def display_multiline_text(text):
    """Quebra um texto longo em várias linhas e exibe no display OLED."""
    display.fill(0)
    
    # Configurações: 16 caracteres por linha, 10 pixels de altura por linha
    max_chars_per_line = 16
    y = 0 # Posição Y inicial
    
    palavras = text.split(' ') # Quebra o texto em uma lista de palavras
    linha_atual = ""
    
    for palavra in palavras:
        # Verifica se a palavra cabe na linha atual
        if len(linha_atual) + len(palavra) + 1 <= max_chars_per_line:
            linha_atual += palavra + " "
        else:
            # Se não cabe, desenha a linha atual e começa uma nova
            display.text(linha_atual, 0, y)
            y += 10 # Move para a próxima linha
            linha_atual = palavra + " "
            
            # Se a tela encher, para de desenhar
            if y >= 60:
                break
                
    # Desenha a última linha que sobrou
    display.text(linha_atual, 0, y)
    
    display.show()


### MODIFICADO ###
# --- PASSO 2: MODIFICAR ASK_GEMINI PARA RETORNAR A RESPOSTA ---
def ask_gemini(prompt):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.2  # <-- AJEITE A TEMPERATURA AQUI
        }
    }
    print("Enviando pergunta para o Gemini...")
    
    try:
        json_string_para_enviar = ujson.dumps(data)
        response = urequests.post(URL, headers=headers, data=json_string_para_enviar)
        
        if response.status_code == 200:
            response_json = response.json()
            content = response_json['candidates'][0]['content']['parts'][0]['text']
            print("\n--- Resposta do Gemini ---")
            print(content)
            print("--------------------------")
            response.close()
            return content  # <-- MUDANÇA IMPORTANTE: Retorna o texto
        else:
            print(f"Erro na API: {response.status_code}")
            print(response.text)
            response.close()
            return "Erro de API." # <-- Retorna uma mensagem de erro
            
    except Exception as e:
        print(f"Ocorreu um erro na requisição: {e}")
        return "Erro de conexao." # <-- Retorna uma mensagem de erro
def sincronizar_relogio():
    try:
        ntptime.settime()
        time.sleep(2)
    except Exception as e:
        print("Erro ao sincronizar relogio:", e)
       

# --- Execução ---
connect_wifi()
time.sleep(2)

# (Sua inicialização de hardware permanece a mesma)
i2c = I2C(1, sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN))
display = SSD1306_I2C(128, 64, i2c)
button_a = Pin(BUTTON_A_PIN, Pin.IN, Pin.PULL_UP)
button_b = Pin(BUTTON_B_PIN, Pin.IN, Pin.PULL_UP)
adc_x = ADC(Pin(JOYSTICK_X_PIN))
adc_y = ADC(Pin(JOYSTICK_Y_PIN))
led = Pin(LED_PIN, Pin.OUT)

# --- VARIÁVEIS DO PROGRAMA ---
alfabeto = "QWERTYUIOPASDFGHJKLZXCVBNM-+*/0123456789<"
tamanho_alfabeto = len(alfabeto)
cursor = 0
frase = ""
M = 0
seta = 0
pontos = 0

display.fill(0)
display.text("MicroCelular",15,20)
display.text("Por Gabriel ",15,30)
display.show()
time.sleep(0.1)
while True:
    if M == 5:
        M = 0
    if button_a.value() == 0:
        M = M + 1
        time.sleep(0.2)
    display.fill(0)
        
    display.text(f"{M}",110,10*M)
    display.text("<-",90,10*M)
    display.text("Modo Livre",0,0)
    display.text("Horario",0,10)
    display.text("Tradutor",0,20)
    display.text("Quiz STEM",0,30)
    display.text("LED",0,40)
    display.show()
    if button_b.value() == 0:
        break
    if button_b.value() == 0:
        break
while M == 0:
    display.fill(0)
    # --- LÓGICA DO JOYSTICK E BOTÕES (Permanece a mesma) ---
    x_val = adc_x.read_u16()
    y_val = adc_y.read_u16()
    dead_zone = 5000
    centro = 32768
    
    # Movimento do cursor com o joystick (eixo Y)
    if abs(y_val - centro) > (dead_zone + 20000):
        cursor = (cursor + 1) % tamanho_alfabeto
        time.sleep(0.05)
    if y_val < (centro - dead_zone - 20000):
        cursor = (cursor - 2) % tamanho_alfabeto
        time.sleep(0.05)
    if abs(x_val - centro) > (dead_zone + 20000):
        cursor = (cursor - 10) % tamanho_alfabeto
        time.sleep(0.05)
        

    # Lógica do botão B (Adicionar letra)
    if button_b.value() == 0:
        frase += alfabeto[cursor]
        time.sleep(0.2)
        if alfabeto[cursor] == '<':
            frase = frase[:-1]
            display.show()
            

    # Lógica do botão A (Enviar para a IA)
    if button_a.value() == 0:
        if frase: # Apenas envia se a frase não estiver vazia
            display.fill(0)
            display.text("Enviando...", 28, 28)
            display.show()
            
            resposta_ia = ask_gemini(f"responda em poucas palavras sem acentuacao {frase}")
            
            display_multiline_text(resposta_ia)
            
            time.sleep(10)
            frase = "" # Limpa a frase
    
    # --- NOVA LÓGICA DE DESENHO DO TECLADO E CURSOR ---

    # 1. Definições da geometria do teclado
    start_x = 5       # Posição X inicial
    start_y = 5       # Posição Y inicial
    char_width = 11   # Espaçamento horizontal entre as letras
    char_height = 12  # Espaçamento vertical entre as linhas
    
    # 2. Desenha todas as letras do teclado
    for index, letra in enumerate(alfabeto):
        # Define as quebras de linha com base no índice da letra
        if index < 10:  # Primeira linha (QWERTYUIOP) - 10 letras
            row = 0
            col = index
        elif index < 20: # Segunda linha (ASDFGHJKLZ) - 9 letras
            row = 1
            col = index - 10
        elif index < 30: # Terceira linha (XCVBNM) - 7 letras
            row = 2
            col = index - 20
        else:       
            row = 3
            col = index - 30

        # Calcula a posição x, y da letra
        pos_x = start_x + (col * char_width)
        pos_y = start_y + (row * char_height)
        
        display.text(letra, pos_x, pos_y)
        
        # 3. Se a letra atual for a selecionada pelo cursor, guarda a sua posição
        if index == cursor:
            cursor_x = pos_x
            cursor_y = pos_y

    display.rect(cursor_x - 2, cursor_y - 2, 10, 11, 1)

    # --- EXIBIÇÃO DA FRASE E ATUALIZAÇÃO DA TELA ---
    display.text(frase[-16:], 0, 57)
    display.show()
    time.sleep(0.05)

while M == 3:
    # --- PASSO 1: PEDIR UM LOTE DE PERGUNTAS DE UMA SÓ VEZ ---
    prompt_lote_quiz = "Crie uma lista de 10 perguntas unicas sobre ciencia, computacao, engenharia e matematica com 2 opcoes (A e B) sem acentuacao. Use o formato: Pergunta? A) Opcao1 B) Opcao2 | Resposta: LetraCorreta. Separe cada pergunta completa com '$$'."
    
    display.fill(0)
    display.text("Buscando 10", 10, 20)
    display.text("perguntas...", 10, 30)
    display.show()
    
    lote_respostas_ia = ask_gemini(prompt_lote_quiz)
    
    if "Erro" in lote_respostas_ia:
        display_multiline_text(lote_respostas_ia)
        time.sleep(3)
        break

    # --- PASSO 2: PROCESSAR O LOTE E CRIAR A LISTA ---
    lista_de_perguntas = lote_respostas_ia.split('$$')
    pontos = 0 # Reinicia a pontuação a cada novo quiz
    
    # --- PASSO 3: LOOP PARA EXIBIR CADA PERGUNTA ---
    for numero_da_pergunta, pergunta_atual in enumerate(lista_de_perguntas, 1):
        
        if not pergunta_atual.strip():
            continue
            
        try:
            partes = pergunta_atual.split('|')
            texto_pergunta = partes[0].strip()
            resposta_correta = partes[1].split(':')[1].strip().upper()
        except Exception as e:
            print(f"Erro ao processar uma pergunta do lote: {e}")
            continue

        # --- CORREÇÃO PRINCIPAL ESTÁ AQUI ---
        # Faltava esta parte para mostrar a pergunta na tela
        display_multiline_text(texto_pergunta) 
        display.show()

        # Espera pela resposta do usuário
        escolha_usuario = None
        while escolha_usuario is None:
            if button_a.value() == 0 and button_b.value() == 0:
                M = -1
                while button_a.value() == 0 or button_b.value() == 0: time.sleep(0.01)
                break
            if button_a.value() == 0:
                escolha_usuario = "A"
                while button_a.value() == 0: time.sleep(0.01)
            if button_b.value() == 0:
                escolha_usuario = "B"
                while button_b.value() == 0: time.sleep(0.01)
            time.sleep(0.02)
        
        if M == -1: break

        # Verifica a resposta e mostra o resultado
        display.fill(0)
        if escolha_usuario == resposta_correta:
            pontos += 1
            display.text("Correto!", 30, 28)
            display.text(f"Placar:{pontos}/10", 30, 40)
            ledG.on()
        else:
            display.text("Incorreto!", 25, 20)
            display.text(f"Era: {resposta_correta}", 40, 35)
            display.text(f"Placar:{pontos}/10", 30, 40)
            ledR.on()
        
        display.show()
        time.sleep(2.5)
        ledG.off()
        ledR.off()

    # --- PASSO 4: FIM DA RODADA ---
    display.fill(0)
    display.text("Fim de Jogo!", 20, 20)
    display.text(f"Placar: {pontos}/10", 20, 35)
    display.show()
    time.sleep(4)
    
    break
while M == 4:
    display.fill(0)
    display.text("VERMELHO: A",20,20)
    display.text("AZUL: B",20, 30)
    display.text("ROSA: A + B",20, 40)
    display.show()
    if button_a.value() == 0:
        ledR.on()
    else:
        ledR.off()
    display.show()
    if button_b.value() == 0:
        ledB.on()
    else:
        ledB.off()
    
    
    
    
    
    
    