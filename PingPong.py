import pygame
import sys
import random

pygame.init()

pygame.display.set_icon(pygame.Surface([1, 1], pygame.SRCALPHA))

largura_tela = 1000
altura_tela = 700
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Ping-Pong Digital")

branco = (255, 255, 255)
preto = (0, 0, 0)

largura_raquete = 15
altura_raquete = 100
velocidade_raquete = 7

raquete_1 = pygame.Rect(50, altura_tela // 2 - altura_raquete // 2, largura_raquete, altura_raquete)
raquete_2 = pygame.Rect(largura_tela - 50 - largura_raquete, altura_tela // 2 - altura_raquete // 2, largura_raquete, altura_raquete)

tamanho_bola = 20
bola = pygame.Rect(largura_tela // 2 - tamanho_bola // 2, altura_tela // 2 - tamanho_bola // 2, tamanho_bola, tamanho_bola)

velocidade_bola_x = 5 * random.choice([1, -1])
velocidade_bola_y = 5 * random.choice([1, -1])

placar_1 = 0
placar_2 = 0
pontuacao_maxima = 10
fonte_placar = pygame.font.Font(None, 74)
fonte_vencedor = pygame.font.Font(None, 90)

relogio = pygame.time.Clock()
fps = 60

estado_jogo = 'JOGANDO'
vencedor = None


def reiniciar_bola_e_raquetes():
    global bola, velocidade_bola_x, velocidade_bola_y, raquete_1, raquete_2

    bola.center = (largura_tela // 2, altura_tela // 2)

    raquete_1.x = 50
    raquete_1.y = altura_tela // 2 - altura_raquete // 2

    raquete_2.x = largura_tela - 50 - largura_raquete
    raquete_2.y = altura_tela // 2 - altura_raquete // 2

    velocidade_bola_x = 5 * random.choice([1, -1])
    velocidade_bola_y = 5 * random.choice([1, -1])

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if estado_jogo == 'FIM_DE_JOGO' and evento.key == pygame.K_r:
                placar_1 = 0
                placar_2 = 0
                reiniciar_bola_e_raquetes()
                estado_jogo = 'JOGANDO'

    if estado_jogo == 'JOGANDO':
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w] and raquete_1.top > 0:
            raquete_1.y -= velocidade_raquete
        if teclas[pygame.K_s] and raquete_1.bottom < altura_tela:
            raquete_1.y += velocidade_raquete
        if teclas[pygame.K_UP] and raquete_2.top > 0:
            raquete_2.y -= velocidade_raquete
        if teclas[pygame.K_DOWN] and raquete_2.bottom < altura_tela:
            raquete_2.y += velocidade_raquete

        bola.x += velocidade_bola_x
        bola.y += velocidade_bola_y

        if bola.top <= 0 or bola.bottom >= altura_tela:
            velocidade_bola_y *= -1

        if bola.left <= 0:
            placar_2 += 1
            reiniciar_bola_e_raquetes()
        if bola.right >= largura_tela:
            placar_1 += 1
            reiniciar_bola_e_raquetes()

        if bola.colliderect(raquete_1):
            if velocidade_bola_x < 0: 
                bola.left = raquete_1.right 
                velocidade_bola_x *= -1
                if raquete_1.centery > bola.centery:
                    velocidade_bola_y -= 1
                elif raquete_1.centery < bola.centery:
                    velocidade_bola_y += 1
        if bola.colliderect(raquete_2):
            if velocidade_bola_x > 0: 
                bola.right = raquete_2.left 
                velocidade_bola_x *= -1
                if raquete_2.centery > bola.centery:
                    velocidade_bola_y -= 1
                elif raquete_2.centery < bola.centery:
                    velocidade_bola_y += 1

        if placar_1 >= pontuacao_maxima:
            vencedor = 1
            estado_jogo = 'FIM_DE_JOGO'
        elif placar_2 >= pontuacao_maxima:
            vencedor = 2
            estado_jogo = 'FIM_DE_JOGO'

    tela.fill(preto)

    if estado_jogo == 'JOGANDO':
        pygame.draw.rect(tela, branco, raquete_1)
        pygame.draw.rect(tela, branco, raquete_2)
        pygame.draw.rect(tela, branco, bola)

        for i in range(0, altura_tela, 20):
            pygame.draw.rect(tela, branco, (largura_tela // 2 - 2, i, 4, 10))

        texto_placar_1 = fonte_placar.render(str(placar_1), True, branco)
        texto_placar_2 = fonte_placar.render(str(placar_2), True, branco)
        tela.blit(texto_placar_1, (largura_tela // 4 - texto_placar_1.get_width() // 2, 20))
        tela.blit(texto_placar_2, (largura_tela * 3 // 4 - texto_placar_2.get_width() // 2, 20))

    elif estado_jogo == 'FIM_DE_JOGO':
        mensagem = f"JOGADOR {vencedor} VENCEU!"
        texto_vencedor = fonte_vencedor.render(mensagem, True, branco)
        tela.blit(texto_vencedor, (largura_tela // 2 - texto_vencedor.get_width() // 2, altura_tela // 2 - texto_vencedor.get_height() // 2))

        mensagem_reiniciar = "Pressione R para Reiniciar"
        texto_reiniciar = fonte_placar.render(mensagem_reiniciar, True, branco)
        tela.blit(texto_reiniciar, (largura_tela // 2 - texto_reiniciar.get_width() // 2, altura_tela // 2 + texto_vencedor.get_height()))

    pygame.display.flip()

    relogio.tick(fps)

pygame.quit()
sys.exit()