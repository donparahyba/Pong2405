#IMPORTAÇÃO E INICIALIZAÇÃO
import pygame
 
pygame.init()
 
# Fonte usada
font20 = pygame.font.Font('freesansbold.ttf', 20)
 
# Valores das cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
 
# Informações da tela
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
#Framerate
clock = pygame.time.Clock()    
FPS = 60
 
# Classe do jogador
class Raquete:
        # Função __init__ que pega a posição, dimensões, velocidade e cor iniciais do objeto
    def __init__(self, posx, posy, width, height, speed, cor):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.cor = cor
        # Controlar a posição e a colisão do objeto
        self.RectJogador = pygame.Rect(posx, posy, width, height)
        # Desenha o retângulo na tela especificada com a cor especificada
        self.Jogador = pygame.draw.rect(screen, self.cor, self.RectJogador)
 
    # Atualiza a raquete sempre que necessário (como após um movimento)
    def display(self):
        self.Jogador = pygame.draw.rect(screen, self.cor, self.RectJogador)
    
    # Essa função define o movimento da bola
    # A posição é somada com a velocidade, que é multiplicada com o verti. Dependendo do valor ele muda a direção.
    # Se verti for -1, vai para cima; se for 1, vai para baixo; se for 0, está parado)
    def update(self, Verti):
        self.posy = self.posy + self.speed*Verti
 
        # Faz com que a raquete nao ultrapasse a borda superior
        if self.posy <= 0:
            self.posy = 0
        # Faz com que a raquete nao ultrapasse a borda inferior
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT-self.height
        # Atualiza a rect com os novos valores
        self.RectJogador = (self.posx, self.posy, self.width, self.height)
    
    # Mostra a pontuação (score) na tela
    # Cria o objeto texto
    def displayScore(self, text, score, x, y, cor):
        text = font20.render(text+str(score), True, cor)
        textRect = text.get_rect()
        textRect.center = (x, y)
        screen.blit(text, textRect)
 
    # Retorna o retãngulo que representa o tamanho e posição da raquete
    def getRect(self):
        return self.RectJogador
 
# Classe da bola
class Bola:
    def __init__(self, posx, posy, radius, speed, cor):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.cor = cor
        self.hori = 1
        self.verti = -1
        self.bola = pygame.draw.circle(
            screen, self.cor, (self.posx, self.posy), self.radius)
        self.firstTime = 1
 
    def display(self):
        self.bola = pygame.draw.circle(
            screen, self.cor, (self.posx, self.posy), self.radius)
    
    def update(self):
        self.posx += self.speed*self.hori
        self.posy += self.speed*self.verti
 
        # Faz a bola refletir quando bate em alguma borda, invertendo o Verti
        if self.posy <= 0 or self.posy >= HEIGHT:
            self.verti *= -1

        # 
        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0
 
    #Reseta a posição da bola para o meio
    def reset(self):
        self.posx = WIDTH//2
        self.posy = HEIGHT//2
        self.hori *= -1
        self.firstTime = 1
 
    # Reflete a bola horizontalmente
    def bate(self):
        self.hori *= -1
    # Realiza detecção de colisão entre a bola e outros objetos na tela.
    def getRect(self):
        return self.bola
 
# Loop e eventos
def main():
    running = True
 
    # Definindo nossos objetos
    jogador1 = Raquete(20, 0, 10, 100, 10, VERDE)
    jogador2 = Raquete(WIDTH-30, 0, 10, 100, 10, VERDE)
    bola = Bola(WIDTH//2, HEIGHT//2, 7, 7, BRANCO)
 
    lista_jogadores = [jogador1, jogador2]
 
    # Parâmetros iniciais dos jogadores, zerados
    jogador1Score, jogador2Score = 0, 0
    jogador1Verti, jogador2Verti = 0, 0
 
    while running:
        screen.fill(PRETO)
 
        # Muda o Verti dependendo da tecla apertada, produzindo movimento
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    jogador2Verti = -1
                if event.key == pygame.K_DOWN:
                    jogador2Verti = 1
                if event.key == pygame.K_w:
                    jogador1Verti = -1
                if event.key == pygame.K_s:
                    jogador1Verti = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    jogador2Verti = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    jogador1Verti = 0
 
        # Checa se a bola colidiu com alguma raquete, e reflete
        for jogador in lista_jogadores:
            if pygame.Rect.colliderect(bola.getRect(), jogador.getRect()):
                bola.bate()
 
        # Atualizando o objetos
        jogador1.update(jogador1Verti)
        jogador2.update(jogador2Verti)
        ponto = bola.update()
 
        # Ele checa se a bola ultrapassou a borda esquerda (-1) ou direita (1)
        # Se for -1, o primeiro jogador fez ponto, se for +1, o jogador 2 faz o ponto, e se for 0 nenhum deles fez ponto.
        if ponto == -1:
            jogador1Score += 1
        elif ponto == 1:
            jogador2Score += 1
 
        # A bola reseta a posição quando alguém faz ponto
        if ponto:   
            bola.reset()
 
        # Mostra os objetos de antes na tela com a função de antes
        jogador1.display()
        jogador2.display()
        bola.display()
 
        # Placar dos jogadores, chamando a função lá de antes
        jogador1.displayScore("Primeiro Jogador: ", 
                           jogador1Score, 100, 20, BRANCO)
        jogador2.displayScore("Segundo Jogador: ", 
                           jogador2Score, WIDTH-100, 20, BRANCO)
        pygame.display.update()
        # Ajustando frame rate
        clock.tick(FPS)     
 
 #Encerramento do jogo
if __name__ == "__main__":
    main()
    pygame.quit()