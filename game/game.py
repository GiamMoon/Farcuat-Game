import pygame, sys, random,os
from .config import *
from .plataforma import Plataforma
from .jugador import Jugador
from .pared import Pared
from .moneda import Moneda


class Game():

    
    
    def __init__(self):
        pygame.init()
        self.ventana = pygame.display.set_mode((ANCHO,ALTO))
        pygame.display.set_caption(TITULO)
        
        #Atributo para saber si el juego se esta ejecutando
        self.ejecutando = True

        
        
        self.clock = pygame.time.Clock()

        self.directorio = os.path.dirname(__file__)
        self.directorio_sonidos = os.path.join(self.directorio,"sounds") 

        self.dirrectorio_imagenenes = os.path.join(self.directorio,"imagenes")
        
       

    def iniciar(self):
        self.menu()
        self.musica()
        self.nuevo()
        
    def musica(self):
        
            sonido  = pygame.mixer.Sound(os.path.join(self.directorio_sonidos,"musicaprincipal.wav"))
            sonido.play(-1) 
            sonido.set_volume(0.3)
            

    def nuevo(self):
        self.puntuacion = 0
        self.niveles  = 0
        self.jugando = True 
        self.fondo = pygame.image.load(os.path.join(self.dirrectorio_imagenenes,"paisaje.jpg"))
        self.velocidad = 5
        self.generar_elementos()
        self.ejecutar()
        
        

    def generar_elementos(self):
        self.plataforma = Plataforma()
        self.jugador = Jugador(100,self.plataforma.rect.top-400,self.dirrectorio_imagenenes)
        

        #Generamos los elementos
        self.sprites = pygame.sprite.Group()
        self.paredes = pygame.sprite.Group()
        self.monedas = pygame.sprite.Group()
        self.sprites.add(self.plataforma)
        self.sprites.add(self.jugador)
        self.generar_paredes()
        
    
    def generar_paredes(self):

        ultima_posicion = ANCHO +150
        

        if not len(self.paredes) > 0:

            for w in range(0,10+self.niveles):

                left = random.randrange(ultima_posicion +200,ultima_posicion+400)
                pared = Pared(left, self.plataforma.rect.top,5+self.niveles,self.dirrectorio_imagenenes)
                

                ultima_posicion = pared.rect.right

                self.sprites.add(pared)
                self.paredes.add(pared) 

            self.niveles += 1
            
            self.generar_monedas()    

    def generar_monedas(self):
        ultima_posicion = ANCHO +120
        for c in range(random.randint(5,20)):
            pos_x = random.randrange(ultima_posicion+180, ultima_posicion+300)
            moneda = Moneda(pos_x,270,4.5+0.5,self.dirrectorio_imagenenes)
            ultima_posicion = moneda.rect.right
            self.sprites.add(moneda)
            self.monedas.add(moneda)

    def ejecutar(self):
         
        while self.ejecutando:
            self.clock.tick(FPS)
            self.eventos()
            self.update()
            self.dibujar()
            

    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False
                pygame.quit()
                sys.exit()

        tecla = pygame.key.get_pressed()

        if tecla[pygame.K_SPACE]:
            self.jugador.salto()  

        if tecla[pygame.K_e] and not self.jugando:
            self.nuevo()     

    def dibujar(self):
        self.ventana.blit(self.fondo,(0,0))
        self.pintar_texto()
        self.sprites.draw(self.ventana)
        #Actualiza la pantalla
        pygame.display.flip()

    def update(self):

        if not self.jugando: 
            return
             
        
        pared = self.jugador.colision(self.paredes)
        if pared:
            if self.jugador.colision_bottom(pared):
                self.jugador.surfear(pared)
                
            else:        
                self.parar()
                
            
        moneda = self.jugador.colision(self.monedas)
        if moneda: 
            self.puntuacion += 1
            moneda.kill()

            sonido  = pygame.mixer.Sound(os.path.join(self.directorio_sonidos,"coin.wav"))
            sonido.play()

        self.sprites.update()

        self.jugador.validar_plataforma(self.plataforma)


        self.actualizar_elementos(self.paredes)
        self.actualizar_elementos(self.monedas)
        self.generar_paredes()
        
            


    def actualizar_elementos(self,elementos):
        for elemento in elementos:
            if not elemento.rect.right > 0:
                elemento.kill()        

    def parar(self):
        sonido  = pygame.mixer.Sound(os.path.join(self.directorio_sonidos,"perder.wav"))
        sonido.play()
        

        self.jugador.parar()
        self.parar_elementos(self.paredes)
        self.jugando = False
        

    def parar_elementos(self,elementos):

        for elemento in elementos:
            elemento.parar()

    def formato_puntuacion(self):
        return "Puntuación: {}".format(self.puntuacion)
    
    def formato_nivel(self):
        return "Nivel: {}".format(self.niveles)

    def pintar_texto(self):
        self.mostrar_texto(self.formato_puntuacion(),40,BLANCO, ANCHO//2,TEXTO_POSY)
        self.mostrar_texto(self.formato_nivel(),40,NEGRO, 90,TEXTO_POSY)

        if not self.jugando:
            self.mostrar_texto("Perdiste",50,NEGRO, ANCHO//2,200)
            self.mostrar_texto("Presiona E para comenzar de nuevo",40,NEGRO, ANCHO//2,100)
            

    def mostrar_texto(self,texto,size,color,pos_x,pos_y):

        fuente = pygame.font.Font("fuentes/oldnewspapertypes/OldNewspaperTypes.ttf",size)
        texto = fuente.render(texto, True,color) 
        rectangulo = texto.get_rect()
        rectangulo.midtop = (pos_x,pos_y)
        self.ventana.blit(texto,rectangulo) 

    def menu(self):
        self.fondo2 = pygame.image.load(os.path.join(self.dirrectorio_imagenenes,"menuimagen.jpg"))
        self.ventana.blit(self.fondo2,(0,0))
        pygame.display.flip()
        self.esperar()

   

    def esperar(self):
        esperar = True 
        musicamenu = pygame.mixer.Sound(os.path.join(self.directorio_sonidos,"musicamenu.wav"))
        musicamenu.play(-1)
        musicamenu.set_volume(0.5)
        
        while esperar:
            self.clock.tick(FPS)
            
            

            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    esperar = False
                    self.ejecutando = False
                    pygame.quit()
                    sys.exit()

                if evento.type ==  pygame.KEYUP:
                    musicamenu.stop()
                    esperar = False    