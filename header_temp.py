import pygame
import sys
import random
import math

# --- CONFIGURAÇÕES GERAIS ---
# Pre-init mixer for better buffer size and lower latency
pygame.mixer.pre_init(44100, -16, 2, 512)
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
