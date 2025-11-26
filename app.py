import pygame
import sys
import random
import math

# --- CONFIGURAÇÕES GERAIS ---
pygame.init()
pygame.mixer.init()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL_CEU = (135, 206, 235)
CHAO_COR = (100, 100, 100)
PELE = (117, 70, 40)
ROUPA_COR = (255, 0, 0)
CALCA_COR = (0, 0, 150)
VERDE_QUADRO = (34, 139, 34)
AMARELO_OURO = (255, 215, 0)
ROXO_XP = (138, 43, 226)

# Tela
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("A Jornada de Willblackinho - Rumo à COP 30")

# Carregar Background
try:
    img_fundo = pygame.image.load("background.png")
    img_fundo = pygame.transform.scale(img_fundo, (LARGURA_TELA, ALTURA_TELA))
except Exception as e:
    print(f"Erro ao carregar background: {e}")
    img_fundo = None

# Clock para controlar FPS
relogio = pygame.time.Clock()
FPS = 60

# Fontes
fonte_pixel = pygame.font.SysFont('arial', 20, bold=True)
fonte_titulo = pygame.font.SysFont('arial', 30, bold=True)
fonte_pergunta = pygame.font.SysFont('arial', 18)
fonte_input = pygame.font.SysFont('arial', 32, bold=True)
fonte_hud = pygame.font.SysFont('impact', 24)

# Sons
sons = {}
def carregar_som(nome, arquivo):
    try:
        sons[nome] = pygame.mixer.Sound(arquivo)
        sons[nome].set_volume(1.0)
    except Exception as e:
        print(f"Erro ao carregar som {nome}: {e}")
        sons[nome] = None

def tocar_som(nome):
    if sons.get(nome):
        sons[nome].play()

# Carregando sons gerados
carregar_som('pulo', 'pulo.wav')
carregar_som('moeda', 'moeda.wav')
carregar_som('acerto', 'acerto.wav')
carregar_som('levelup', 'levelup.wav')
carregar_som('erro', 'erro.wav')

# Música de fundo
try:
    pygame.mixer.music.load('music.wav')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
except Exception as e:
    print(f"Erro ao carregar música: {e}")

# --- BANCO DE QUESTÕES ---
BANCO_QUESTOES = [
    {
        "pergunta": "Sobre a origem do Petróleo e do Carvão Mineral, é correto dizer que:",
        "opcoes": [
            "A) Vieram de rochas vulcânicas recentes.",
            "B) São formados por restos de matéria orgânica de milhões de anos.",
            "C) São criados em laboratório para abastecer carros.",
            "D) Vêm da energia solar concentrada nas plantas."
        ],
        "correta": pygame.K_b
    },
    {
        "pergunta": "Os combustíveis fósseis são chamados assim porque:",
        "opcoes": [
            "A) São feitos de ossos de dinossauros apenas.",
            "B) Levam milhões de anos para se formar no subsolo.",
            "C) São fontes de energia infinitas e limpas.",
            "D) Podem ser plantados e colhidos rapidamente."
        ],
        "correta": pygame.K_b
    },
    {
        "pergunta": "Qual destes grupos contém APENAS combustíveis fósseis?",
        "opcoes": [
            "A) Carvão Mineral, Petróleo e Gás Natural.",
            "B) Energia Solar, Petróleo e Lenha.",
            "C) Gás Natural, Lítio e Vento.",
            "D) Água, Carvão e Urânio."
        ],
        "correta": pygame.K_a
    },

    # TEMA: COP 30 / TRANSIÇÃO ENERGÉTICA
    {
        "pergunta": "A COP 30 no Brasil discutirá a 'Transição Energética'. O objetivo principal é:",
        "opcoes": [
            "A) Aumentar o uso de carvão para gerar empregos.",
            "B) Trocar gradualmente fontes poluentes por energias limpas.",
            "C) Proibir o uso de energia elétrica nas cidades.",
            "D) Substituir a energia solar por petróleo."
        ],
        "correta": pygame.K_b
    },
    {
        "pergunta": "Por que é urgente diminuir o uso do petróleo no mundo?",
        "opcoes": [
            "A) Porque ele esfria demais o planeta.",
            "B) Para evitar que os carros fiquem muito rápidos.",
            "C) Porque sua queima libera gases que aquecem o planeta (Estufa).",
            "D) Porque o petróleo atrai meteoros."
        ],
        "correta": pygame.K_c
    },
    {
        "pergunta": "O que significa dizer que uma fonte de energia é 'Limpa'?",
        "opcoes": [
            "A) Que ela precisa ser lavada antes de usar.",
            "B) Que ela não emite (ou emite poucos) poluentes na atmosfera.",
            "C) Que ela é transparente como a água.",
            "D) Que ela não custa dinheiro."
        ],
        "correta": pygame.K_b
    },

    # TEMA: LÍTIO
    {
        "pergunta": "O Lítio ganhou destaque mundial recentemente. Qual sua principal função hoje?",
        "opcoes": [
            "A) Ser queimado em usinas termoelétricas.",
            "B) Servir de adubo para plantações de soja.",
            "C) Fabricação de baterias para carros elétricos e celulares.",
            "D) Construção de paredes de casas sustentáveis."
        ],
        "correta": pygame.K_c
    },
    {
        "pergunta": "Embora essencial para a tecnologia verde, o Lítio é classificado como:",
        "opcoes": [
            "A) Um recurso mineral não renovável (finito).",
            "B) Um combustível fóssil poluente.",
            "C) Um vegetal que cresce em árvores.",
            "D) Uma energia inesgotável como o vento."
        ],
        "correta": pygame.K_a
    },

    # TEMA: FONTES RENOVÁVEIS
    {
        "pergunta": "Fontes renováveis são aquelas que não acabam com o uso. Um exemplo é:",
        "opcoes": [
            "A) O Gás Natural.",
            "B) O Urânio.",
            "C) A força dos ventos (Eólica).",
            "D) O Carvão Mineral."
        ],
        "correta": pygame.K_c
    },
    {
        "pergunta": "Qual alternativa apresenta a melhor solução para um futuro sustentável?",
        "opcoes": [
            "A) Energia Solar e Eólica.",
            "B) Carvão e Diesel.",
            "C) Queima de lixo e Plástico.",
            "D) Petróleo e Gás de Xisto."
        ],
        "correta": pygame.K_a
    }
]

# Sorteia 4 perguntas aleatórias do banco a cada vez que inicia
# Para garantir que não repita a mesma pergunta no mesmo jogo
QUESTOES = random.sample(BANCO_QUESTOES, 4)

# --- CLASSES ---

class VirtualButton:
    def __init__(self, x, y, w, h, text, color=(100, 100, 100)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.is_pressed = False
        self.shadow_rect = pygame.Rect(x, y+5, w, h)

    def draw(self, surface):
        # Efeito 3D simples (sombra deslocada)
        if not self.is_pressed:
            pygame.draw.rect(surface, (50, 50, 50), self.shadow_rect, border_radius=10)
            offset = 0
        else:
            offset = 5 # Botão desce
        
        # Botão principal
        draw_rect = pygame.Rect(self.rect.x, self.rect.y + offset, self.rect.width, self.rect.height)
        
        # Cor muda se estiver pressionado
        draw_color = (min(self.color[0] + 30, 255), min(self.color[1] + 30, 255), min(self.color[2] + 30, 255))
        
        pygame.draw.rect(surface, draw_color, draw_rect, border_radius=10)
        pygame.draw.rect(surface, BRANCO, draw_rect, 2, border_radius=10)
        
        text_surf = fonte_pixel.render(self.text, True, BRANCO)
        text_rect = text_surf.get_rect(center=draw_rect.center)
        surface.blit(text_surf, text_rect)

    def check_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                tocar_som('pulo') # Som de clique genérico
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_pressed = False
            
    # Para resetar caso o mouse saia do botão enquanto pressionado (opcional, mas bom pra touch)
    def update(self):
        if self.is_pressed:
            if not pygame.mouse.get_pressed()[0]: # Se o botão do mouse não está mais clicado
                self.is_pressed = False

class Particula(pygame.sprite.Sprite):
    def __init__(self, x, y, cor):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(cor)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = random.uniform(-3, 3)
        self.vel_y = random.uniform(-3, 3)
        self.vida = 30
    
    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.vida -= 1
        if self.vida <= 0:
            self.kill()

class Moeda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, AMARELO_OURO, (10, 10), 10)
        pygame.draw.circle(self.image, (255, 255, 200), (7, 7), 3) # Brilho
        self.rect = self.image.get_rect(center=(x, y))
        self.y_inicial = y
        self.timer = 0
    
    def update(self):
        self.timer += 0.1
        self.rect.y = self.y_inicial + math.sin(self.timer) * 5 # Flutuar

class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Criando o Willblackinho desenhando na superfície
        self.image = pygame.Surface((50, 70)) 
        self.image.set_colorkey(PRETO) # Transparencia
        
        # Desenho do Personagem
        # Cabelo Black Power
        pygame.draw.circle(self.image, (20, 20, 20), (25, 15), 18) 
        # Cabeça
        pygame.draw.circle(self.image, PELE, (25, 25), 10)
        # Corpo (Camiseta Hip Hop)
        pygame.draw.rect(self.image, ROUPA_COR, (10, 35, 30, 20))
        # Calça larga
        pygame.draw.rect(self.image, CALCA_COR, (10, 55, 30, 15))
        # Detalhe corrente de ouro (pixel amarelo)
        pygame.draw.rect(self.image, (255, 215, 0), (22, 38, 6, 6))

        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = ALTURA_TELA - 150
        
        self.vel_y = 0
        self.pulo = False
        self.velocidade = 5
        
        # Gamification
        self.xp = 0
        self.nivel = 1
        self.xp_para_proximo = 100

    def ganhar_xp(self, quantidade):
        self.xp += quantidade
        if self.xp >= self.xp_para_proximo:
            self.xp -= self.xp_para_proximo
            self.nivel += 1
            tocar_som('levelup') # Placeholder
            return True # Level Up
        return False

    def update(self, comandos, plataformas):
        # Movimentação Horizontal
        dx = 0
        dy = 0

        if comandos['esquerda']:
            dx = -self.velocidade
        if comandos['direita']:
            dx = self.velocidade
        
        # Pulo
        if comandos['pulo'] and not self.pulo:
            self.vel_y = -15
            self.pulo = True
            tocar_som('pulo')
        
        # Gravidade
        self.vel_y += 1
        dy += self.vel_y

        # Colisão Horizontal
        self.rect.x += dx
        
        # Manter na tela
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > LARGURA_TELA: self.rect.right = LARGURA_TELA

        # Colisão Vertical (Chão simples)
        self.rect.y += dy
        
        # Checar chão/plataformas
        for plat in plataformas:
            if self.rect.colliderect(plat.rect):
                if self.vel_y > 0: # Caindo
                    self.rect.bottom = plat.rect.top
                    self.vel_y = 0
                    self.pulo = False

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        # Estilo 3D / Futurista
        self.image.fill((50, 50, 60)) # Cor base escura
        
        # Borda brilhante neon
        pygame.draw.rect(self.image, (0, 255, 255), (0, 0, w, h), 2)
        
        # Grade tecnológica
        for i in range(0, w, 20):
            pygame.draw.line(self.image, (70, 70, 80), (i, 0), (i, h), 1)
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class QuadroNegro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 80))
        self.image.fill(VERDE_QUADRO)
        pygame.draw.rect(self.image, (139, 69, 19), (0,0,60,80), 3) # Moldura
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# --- FUNÇÕES DE TEXTO ---

def desenhar_texto_multilinha(texto, fonte, cor, superficie, x, y, largura_max):
    palavras = texto.split(' ')
    linhas = []
    linha_atual = ""
    
    for palavra in palavras:
        teste_linha = linha_atual + palavra + " "
        largura_teste, _ = fonte.size(teste_linha)
        if largura_teste < largura_max:
            linha_atual = teste_linha
        else:
            linhas.append(linha_atual)
            linha_atual = palavra + " "
    linhas.append(linha_atual)
    
    y_offset = 0
    for linha in linhas:
        img_texto = fonte.render(linha, True, cor)
        superficie.blit(img_texto, (x, y + y_offset))
        y_offset += 25

def mostrar_pergunta(id_pergunta):
    dados = QUESTOES[id_pergunta]
    rodando_pergunta = True
    
    fundo_pergunta = pygame.Surface((700, 500))
    fundo_pergunta.fill((20, 20, 40)) # Azul muito escuro
    border = pygame.Rect(0,0,700,500)
    
    # Botões de resposta (áreas clicáveis)
    opcoes_rects = []
    y_opt = 220
    for i in range(4):
        rect = pygame.Rect(70, y_opt, 650, 50)
        opcoes_rects.append({'rect': rect, 'key': [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d][i]})
        y_opt += 60

    while rodando_pergunta:
        tela.blit(fundo_pergunta, (50, 50))
        pygame.draw.rect(tela, BRANCO, (50, 50, 700, 500), 2)
        
        # Título
        titulo = fonte_titulo.render(f"Enigma do Willblackinho {id_pergunta + 1}/4", True, (255, 215, 0))
        tela.blit(titulo, (70, 70))
        
        # Pergunta
        desenhar_texto_multilinha(dados["pergunta"], fonte_pixel, BRANCO, tela, 70, 120, 650)
        
        # Opções
        y_opt = 220
        mouse_pos = pygame.mouse.get_pos()
        
        for i, opt in enumerate(dados["opcoes"]):
            # Highlight se mouse em cima
            cor_texto = (200, 200, 200)
            if opcoes_rects[i]['rect'].collidepoint(mouse_pos):
                cor_texto = (255, 255, 0)
                pygame.draw.rect(tela, (50, 50, 80), opcoes_rects[i]['rect']) # Fundo highlight
            
            desenhar_texto_multilinha(opt, fonte_pergunta, cor_texto, tela, 70, y_opt, 650)
            y_opt += 60
            
        instrucao = fonte_pixel.render("Clique ou pressione A, B, C, D", True, AZUL_CEU)
        tela.blit(instrucao, (70, 480))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            resposta_usuario = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: resposta_usuario = pygame.K_a
                if event.key == pygame.K_b: resposta_usuario = pygame.K_b
                if event.key == pygame.K_c: resposta_usuario = pygame.K_c
                if event.key == pygame.K_d: resposta_usuario = pygame.K_d
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Clique esquerdo
                    for item in opcoes_rects:
                        if item['rect'].collidepoint(event.pos):
                            resposta_usuario = item['key']
            
            if resposta_usuario:
                if resposta_usuario == dados["correta"]:
                    # Feedback Positivo
                    return True
                else:
                    # Feedback Negativo (Tenta de novo)
                    aviso = fonte_titulo.render("Ops! Tente de novo!", True, (255, 0, 0))
                    tela.blit(aviso, (250, 250))
                    pygame.display.flip()
                    pygame.time.delay(1000)

def tela_final(nome_jogador):
    tela.fill(PRETO)
    msg1 = fonte_titulo.render("PARABÉNS!", True, (255, 215, 0))
    msg2 = fonte_pixel.render(f"{nome_jogador} completou o ano letivo!", True, BRANCO)
    msg3 = fonte_pixel.render("Você domina a Transição Energética!", True, AZUL_CEU)
    
    tela.blit(msg1, (LARGURA_TELA//2 - msg1.get_width()//2, 200))
    tela.blit(msg2, (LARGURA_TELA//2 - msg2.get_width()//2, 250))
    tela.blit(msg3, (LARGURA_TELA//2 - msg3.get_width()//2, 300))
    
    pygame.display.flip()
    pygame.time.delay(5000)

def tela_inicial():
    rodando_inicio = True
    nome = ""
    
    while rodando_inicio:
        tela.fill(AZUL_CEU)
        
        # Título
        titulo = fonte_titulo.render("A Jornada de Willblackinho", True, PRETO)
        subtitulo = fonte_pixel.render("Digite seu nome para começar:", True, PRETO)
        
        tela.blit(titulo, (LARGURA_TELA//2 - titulo.get_width()//2, 150))
        tela.blit(subtitulo, (LARGURA_TELA//2 - subtitulo.get_width()//2, 250))
        
        # Caixa de input
        input_rect = pygame.Rect(LARGURA_TELA//2 - 150, 300, 300, 50)
        pygame.draw.rect(tela, BRANCO, input_rect)
        pygame.draw.rect(tela, PRETO, input_rect, 2)
        
        texto_nome = fonte_input.render(nome, True, PRETO)
        tela.blit(texto_nome, (input_rect.x + 10, input_rect.y + 5))
        
        # Instrução
        instrucao = fonte_pixel.render("Pressione ENTER para jogar", True, (50, 50, 50))
        tela.blit(instrucao, (LARGURA_TELA//2 - instrucao.get_width()//2, 400))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(nome) > 0:
                        return nome
                elif event.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                else:
                    # Limita tamanho do nome
                    if len(nome) < 15:
                        nome += event.unicode

# --- LOOP PRINCIPAL DO JOGO ---

def main():
    nome_jogador = tela_inicial()
    
    jogador = Jogador()
    
    # Grupos de Sprites
    todos_sprites = pygame.sprite.Group()
    todos_sprites.add(jogador)
    
    plataformas = pygame.sprite.Group()
    
    # Chão principal
    chao = Plataforma(0, ALTURA_TELA - 40, LARGURA_TELA, 40)
    plataformas.add(chao)
    todos_sprites.add(chao)
    
    # Plataformas flutuantes (Obstáculos do sistema)
    plat1 = Plataforma(200, 450, 150, 20)
    plat2 = Plataforma(450, 350, 150, 20)
    plat3 = Plataforma(100, 250, 150, 20)
    plataformas.add(plat1, plat2, plat3)
    todos_sprites.add(plat1, plat2, plat3)
    
    # Moedas / Energia
    moedas = pygame.sprite.Group()
    m1 = Moeda(250, 420)
    m2 = Moeda(500, 320)
    m3 = Moeda(150, 220)
    m4 = Moeda(600, 450)
    moedas.add(m1, m2, m3, m4)
    todos_sprites.add(m1, m2, m3, m4)
    
    particulas = pygame.sprite.Group()
    
    # Objetivo (Quadro Negro / Portal)
    quadro = QuadroNegro(700, ALTURA_TELA - 120)
    todos_sprites.add(quadro)
    
    # Controles Virtuais (Mobile/Mouse)
    btn_esq = VirtualButton(20, ALTURA_TELA - 100, 80, 80, "<", (50, 50, 150))
    btn_dir = VirtualButton(120, ALTURA_TELA - 100, 80, 80, ">", (50, 50, 150))
    btn_pulo = VirtualButton(LARGURA_TELA - 100, ALTURA_TELA - 100, 80, 80, "PULA", (150, 50, 50))
    
    botoes = [btn_esq, btn_dir, btn_pulo]

    fase_atual = 0
    rodando = True
    
    while rodando:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            
            # Input para botões virtuais
            for btn in botoes:
                btn.check_input(event)
        
        # Atualiza estado dos botões (pra soltar se arrastar pra fora)
        for btn in botoes:
            btn.update()

        # Input Combinado (Teclado + Virtual)
        teclas = pygame.key.get_pressed()
        
        comandos = {
            'esquerda': teclas[pygame.K_LEFT] or btn_esq.is_pressed,
            'direita': teclas[pygame.K_RIGHT] or btn_dir.is_pressed,
            'pulo': teclas[pygame.K_SPACE] or btn_pulo.is_pressed
        }

        jogador.update(comandos, plataformas)
        moedas.update()
        particulas.update()
        
        # Coleta de moedas
        hits = pygame.sprite.spritecollide(jogador, moedas, True)
        for hit in hits:
            jogador.ganhar_xp(10)
            tocar_som('moeda')
            # Efeito de particulas
            for _ in range(5):
                p = Particula(hit.rect.centerx, hit.rect.centery, AMARELO_OURO)
                particulas.add(p)
                todos_sprites.add(p)
        
        # Checar se chegou no quadro negro (Fim da fase)
        if jogador.rect.colliderect(quadro.rect):
            # Lança o desafio
            if fase_atual < len(QUESTOES):
                # Pequeno delay pra não entrar clicando
                pygame.time.delay(200)
                sucesso = mostrar_pergunta(fase_atual)
                if sucesso:
                    fase_atual += 1
                    jogador.ganhar_xp(50)
                    tocar_som('acerto')
                    
                    # Reinicia posição do jogador para a esquerda
                    jogador.rect.x = 50 
                    jogador.rect.y = ALTURA_TELA - 150
                    
                    # Se acabou as perguntas
                    if fase_atual >= len(QUESTOES):
                        tela_final(nome_jogador)
                        rodando = False

        # Desenhar
        if img_fundo:
            tela.blit(img_fundo, (0, 0))
        else:
            tela.fill(AZUL_CEU) # Fallback
        
        todos_sprites.draw(tela)
        
        # Desenhar botões virtuais
        for btn in botoes:
            btn.draw(tela)

        # Desenhar HUD (XP e Nível)
        # Barra de XP
        pygame.draw.rect(tela, (50, 50, 50), (10, 40, 200, 20), border_radius=5)
        pct_xp = jogador.xp / jogador.xp_para_proximo
        if pct_xp > 1: pct_xp = 1
        pygame.draw.rect(tela, ROXO_XP, (10, 40, 200 * pct_xp, 20), border_radius=5)
        pygame.draw.rect(tela, BRANCO, (10, 40, 200, 20), 2, border_radius=5)
        
        texto_xp = fonte_pixel.render(f"XP: {jogador.xp}/{jogador.xp_para_proximo}", True, BRANCO)
        tela.blit(texto_xp, (220, 38))
        
        texto_nivel = fonte_hud.render(f"NÍVEL {jogador.nivel}", True, AMARELO_OURO)
        tela.blit(texto_nivel, (10, 65))

        info = fonte_pixel.render(f"Ano Letivo - Fase: {fase_atual + 1}/4", True, PRETO)
        tela.blit(info, (10, 10))
        
        pygame.display.flip()
        relogio.tick(FPS)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()