import pygame
from pygame.locals import *
import random
import math
from pygame import mixer  # sonido add

# Inicializar pygame
pygame.init()

# Pantalla
pantalla = pygame.display.set_mode((800, 600))

# Título e Icono
pygame.display.set_caption('img/Invasión Espacial')
icono = pygame.image.load("img/nave.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("img/Fondo.jpg")

# Agregar música
mixer.music.load('sound/MusicaFondo.mp3')
mixer.music.set_volume(0.5)  # volumen de fondo
mixer.music.play(-1)  # se repite cada que termina

# Avatar del jugador
img_jugador = pygame.image.load("img/nave.png")
resized_avatar = pygame.transform.scale(img_jugador, (100, 100))
jugador_x = 330
jugador_y = 450
jugador_x_cambio = 0

# Avatar enemigo
img_enemigo = []
resized_avatar_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("img/enemigo.png"))
    resized_avatar_enemigo.append(pygame.transform.scale(img_enemigo[e], (80, 80)))
    enemigo_x.append(random.randint(0, 720))
    enemigo_y.append(random.randint(50, 150))
    enemigo_x_cambio.append(0.3)
    enemigo_y_cambio.append(50)

# Bala
balas = []
img_bala = pygame.image.load("img/misil.png")
resized_bala = pygame.transform.scale(img_bala, (32, 32))

# Puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 35)
texto_X = 10
texto_y = 10

# Fin del juego
fin = pygame.font.Font('freesansbold.ttf', 35)

# Texto final del juego
def texto_final():
    mi_fuente_final = fuente.render('GAME OVER', True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (300, 250))

# Puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f'Puntaje: {puntaje}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

# Función del jugador
def jugador(x, y):
    pantalla.blit(resized_avatar, (x, y))

# Función del enemigo
def enemigo(x, y, ene):
    pantalla.blit(resized_avatar_enemigo[ene], (x, y))

# Detección de colisión
def hay_colision(x1, y1, x2, y2):
    distancia = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    return distancia < 27

# Loop del juego
se_ejecuta = True
juego_terminado = False

while se_ejecuta:
    pantalla.blit(fondo, (0, 0))  # Fondo

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                jugador_x_cambio = -2.5
            elif evento.key == pygame.K_d:
                jugador_x_cambio = 2.5
            elif evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('sound/disparo.mp3')
                sonido_bala.set_volume(0.1)
                sonido_bala.play()
                nueva_bala = {
                    "x": jugador_x + 34,  # Ajustar para que la bala salga desde el centro superior de la nave
                    "y": jugador_y,
                    "velocidad": -5
                }
                balas.append(nueva_bala)

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_a or evento.key == pygame.K_d:
                jugador_x_cambio = 0

    if not juego_terminado:
        # Movimiento del jugador
        jugador_x += jugador_x_cambio
        if jugador_x <= 0:
            jugador_x = 0
        elif jugador_x >= 736:
            jugador_x = 736

        # Movimiento del enemigo
        for e in range(cantidad_enemigos):
            enemigo_x[e] += enemigo_x_cambio[e]

            # Fin del juego si un enemigo toca la nave del jugador
            colision_jugador = hay_colision(enemigo_x[e], enemigo_y[e], jugador_x, jugador_y)
            if colision_jugador:
                for k in range(cantidad_enemigos):
                    enemigo_y[k] = 1000
                juego_terminado = True
                break

            # mantener dentro de bordes al enemigo    
            if enemigo_x[e] <= 0:
                enemigo_x_cambio[e] = 1
                enemigo_y[e] += enemigo_y_cambio[e]
            elif enemigo_x[e] >= 736:
                enemigo_x_cambio[e] = -1
                enemigo_y[e] += enemigo_y_cambio[e]

            # Colisión con la bala
            for bala in balas:
                colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
                if colision_bala_enemigo:
                    sonido_colision = mixer.Sound("sound/Golpe.mp3")
                    sonido_colision.play()
                    balas.remove(bala)
                    puntaje += 1
                    enemigo_x[e] = random.randint(0, 736)
                    enemigo_y[e] = random.randint(20, 200)
                    break

            enemigo(enemigo_x[e], enemigo_y[e], e)

        # Movimiento de la bala
        for bala in balas:
            bala["y"] += bala["velocidad"]
            pantalla.blit(resized_bala, (bala["x"], bala["y"]))
            if bala["y"] < 0:
                balas.remove(bala)

    jugador(jugador_x, jugador_y)
    mostrar_puntaje(texto_X, texto_y)

    if juego_terminado:
        texto_final()

    pygame.display.update()
