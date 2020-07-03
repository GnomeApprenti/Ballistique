import arcade
import math
import random
from random import randrange

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Balistique"

DT=0.7

class Vecteur:

#Calculs de vecteurs

	def __init__(self,x,y):
                
		self.x=x
		self.y=y
		
	def norm(self):
                
		valeur = math.sqrt(self.x * self.x + self.y * self.y) 
		return valeur
	
	def __add__(self, v):
                
		cx = self.x + v.x
		cy = self.y + v.y
		c = Vecteur(cx,cy)
		return c

	def __sub__(self, v):
                
		cx = self.x - v.x
		cy = self.y - v.y
		c = Vecteur(cx,cy)
		return c

	def __mul__(self, s):

		cx = self.x * s
		cy = self.y * s
		c = Vecteur(cx,cy)
		return c

	def __truediv__(self, s):

		fs=float(s)
		cx = self.x / fs
		cy = self.y / fs
		c = Vecteur(cx,cy)
		return c


GRAVITE = Vecteur(0,-9.81/30)


class Ball:

#Classe de Ball
        
    def __init__(self, pos_init, vit_init, rayon_init, couleur_init):
            
        self.position = pos_init
        self.vitesse = vit_init
        self.rayon = rayon_init
        self.couleur = couleur_init
        print("init ball vx = ", self.vitesse.x)
        print("init ball vy = ", self.vitesse.y)
        self.rebonds = 0
        self.aire = math.pi * self.rayon * self.rayon
        

    def draw(self):
            
        arcade.draw_circle_filled(self.position.x, self.position.y, self.rayon, self.couleur)

    def update(self, delta_t):
            
        self.vitesse=self.vitesse+GRAVITE*delta_t
        self.position=self.position+self.vitesse*delta_t
        
        aDetruire = False

        if self.position.x < 0 + self.rayon or self.position.x > SCREEN_WIDTH - self.rayon:
                
                aDetruire = True
                    
        elif self.position.y < 0 + self.rayon:
                
            self.vitesse = Vecteur(self.vitesse.x,-1 * self.vitesse.y)
            self.rebonds += 1

        elif self.position.y > SCREEN_HEIGHT - self.rayon:
                
                aDetruire = True

        if self.rebonds == 3:
                
                aDetruire = True

        return aDetruire


class Canon:

#Classe de Canon

        def __init__(self, pos_init, longueur_init, largeur_init, couleur_init, angle_init):
                
                self.position = pos_init
                self.longueur = longueur_init
                self.largeur = largeur_init
                self.couleur = couleur_init
                self.angle = angle_init
                

        def draw(self):
                
                arcade.draw_rectangle_filled(self.position.x, self.position.y, self.longueur, self.largeur, self.couleur, self.angle)

        def update(self, nouvelAngle):
                
                self.angle = nouvelAngle

class Viseur:

        def __init__(self, pos_init, longueur_init, largeur_init, couleur_init, angle_init):
                
                self.position = pos_init
                self.longueur = longueur_init
                self.largeur = largeur_init
                self.couleur = couleur_init
                self.angle = angle_init
                
                

        def draw(self):

                angleRad = self.angle * math.pi / 180 
                Ax = math.cos(angleRad - math.pi / 2) * self.largeur + self.position.x
                Ay = math.sin(angleRad - math.pi / 2) * self.largeur + self.position.y
                Bx = math.cos(angleRad) * self.longueur + self.position.x
                By = math.sin(angleRad) * self.longueur + self.position.y
                Cx = math.cos(math.pi / 2 + angleRad) * self.largeur + self.position.x
                Cy = math.sin(math.pi / 2 + angleRad) * self.largeur + self.position.y
                
                arcade.draw_triangle_filled(Ax, Ay, Bx, By, Cx, Cy, self.couleur)


        def update(self, nouvelAngle):
                
                self.angle = nouvelAngle

class Enemi:

#Classe de Enemi
        
        def __init__(self, pos_init, longueur_init, largeur_init, couleur_init):
                
                self.position = pos_init
                self.longueur = longueur_init
                self.largeur = self.longueur
                self.couleur = couleur_init
                self.vitesse = Vecteur(0,0)
                self.accroche = True
                self.aire = self.longueur * self.largeur



        def draw(self):
                
                arcade.draw_rectangle_filled(self.position.x, self.position.y, self.longueur, self.largeur, self.couleur)

        def update(self, delta_t):

                if self.accroche == False:
                        
                        self.vitesse=self.vitesse+GRAVITE*delta_t
                        
                self.position=self.position+self.vitesse*delta_t

                aDeplacer = False

                if self.position.y < 0 - self.largeur:
                #en bas

                        aDeplacer = True

                if self.position.y > SCREEN_HEIGHT + self.largeur:
                #en haut

                        aDeplacer = True

                if self.position.x < 0 - self.largeur:
                #a gauche

                        aDeplacer = True

                if self.position.x > SCREEN_WIDTH + self.largeur:

                        aDeplacer = True

                if aDeplacer == True:

                        carreCentralX = SCREEN_WIDTH / 2 + 100
                        carreCentralY = SCREEN_HEIGHT / 2 + 100
                
                        enemiX = randrange(0 + self.largeur, carreCentralX)
                        enemiY = randrange(0 + self.largeur, carreCentralY)
                        self.position = Vecteur(enemiX, enemiY)
                        self.vitesse = Vecteur(0,0)
                        self.largeur = randrange(20, 70)
                        self.longueur = self.largeur
                        self.accroche = True
                        

                        
        
        def touche(self, position_Ball, rayon_Ball):
                touch=0
                dMin = self.largeur/2  + rayon_Ball
                posTemp = position_Ball - self.position
                
                if posTemp.y < posTemp.x and posTemp.y > -1 * posTemp.x and posTemp.x < dMin:
                #coté droit
                        touch = 3

                if posTemp.y > posTemp.x and posTemp.y > -1 * posTemp.x and posTemp.y < dMin:
                #coté haut
                        touch = 2

                if posTemp.y > posTemp.x and posTemp.y < -1 * posTemp.x and -1 * posTemp.x < dMin:
                #coté gauche
                        touch = 4

                if posTemp.y < posTemp.x and posTemp.y < -1 * posTemp.x and -1 * posTemp.y < dMin:
                #coté bas
                        touch = 1 
                

                if touch != 0:
                
                        self.accroche = False
                        
                return touch
                


class Balistique(arcade.Window):

#Classe de Balistique
        
    def __init__(self, width, height, title):
            
        self.angle_balle = 5
        self.vitesse_balle = 30
        self.Ball_list = []
        self.testAngle = 0
        self.testVitesse = 0
        self.tps=0.

        self.position_Canon=Vecteur(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        self.largeur_Canon=25
        self.longueur_Canon=70
        self.couleur_Canon=arcade.color.BLUE
        self.canon = Canon(self.position_Canon, self.longueur_Canon, self.largeur_Canon, self.couleur_Canon, 0)

        self.position_Viseur=Vecteur(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        self.largeur_Viseur=25
        self.longueur_Viseur=70
        self.couleur_Viseur=arcade.color.RED
        self.viseur = Viseur(self.position_Viseur, self.longueur_Viseur, self.largeur_Viseur, self.couleur_Viseur, 0)

        self.largeur_Enemi=randrange(20, 70)
        self.longueur_Enemi=self.largeur_Enemi

        enemiX = randrange(0 + self.largeur_Enemi, SCREEN_WIDTH - self.largeur_Enemi)
        enemiY = randrange(0 + self.largeur_Enemi, SCREEN_HEIGHT - self.largeur_Enemi)
        enemiX = SCREEN_WIDTH*0.75
        enemiY =SCREEN_HEIGHT*0.5
        
        
        self.position_Enemi=Vecteur(enemiX, enemiY)
        
        self.couleur_Enemi=arcade.color.BLACK
        self.enemi = Enemi(self.position_Enemi, self.longueur_Enemi, self.largeur_Enemi, self.couleur_Enemi)
                
        super().__init__(width, height, title)
        
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.ASH_GREY)
        pos0=Vecteur(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)

    def on_draw(self):
                
        arcade.start_render()
        output = "Balles: {}".format(len(self.Ball_list))
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 44)
        
        self.angle_balle = str(self.angle_balle)
        self.vitesse_balle = str(self.vitesse_balle)
        arcade.draw_text(self.angle_balle, 200, 70, arcade.color.WHITE, 44)
        arcade.draw_text(self.vitesse_balle, 200, 120, arcade.color.WHITE, 44)

        texteVitesse = "Vitesse:"
        texteAngle = "Angle:"
        arcade.draw_text(texteVitesse, 10, 120, arcade.color.WHITE, 44)
        arcade.draw_text(texteAngle, 10, 70, arcade.color.WHITE, 44)  
        
        for balle in self.Ball_list:
                
                balle.draw()

        self.canon.draw()
        self.viseur.draw()
        self.enemi.draw()
                

    def update(self, delta_time):
            
        self.tps+=DT
       
        self.vitesse_balle = int(self.vitesse_balle)
        self.angle_balle = int(self.angle_balle)

        self.canon.update(self.angle_balle)
        self.viseur.update(self.angle_balle)
        self.enemi.update(DT)

        for balle in self.Ball_list:
        
                aDetruire = balle.update(DT)

                touch = self.enemi.touche(balle.position, balle.rayon)
                
                if aDetruire == True:
                        
                        self.Ball_list.remove(balle)

                if touch == 3:
                        print("Touché à droite")
                        tmp_vit_ba = (2* self.enemi.aire*self.enemi.vitesse.x + (balle.aire - self.enemi.aire) * balle.vitesse.x  )/(balle.aire + self.enemi.aire)
                        tmp_vit_en = (2* balle.aire*balle.vitesse.x + (self.enemi.aire - balle.aire) * self.enemi.vitesse.x  )/(balle.aire + self.enemi.aire)
                        balle.vitesse.x = tmp_vit_ba
                        self.enemi.vitesse.x = tmp_vit_en
                elif touch == 4:
                        print("Touché à gauche")
                        tmp_vit_ba = (2* self.enemi.aire*self.enemi.vitesse.x + (balle.aire - self.enemi.aire) * balle.vitesse.x  )/(balle.aire + self.enemi.aire)
                        tmp_vit_en = (2* balle.aire*balle.vitesse.x + (self.enemi.aire - balle.aire) * self.enemi.vitesse.x  )/(balle.aire + self.enemi.aire)
                        balle.vitesse.x = tmp_vit_ba
                        self.enemi.vitesse.x = tmp_vit_en
                elif touch == 1:
                        print("Touché en bas")
                        tmp_vit_ba = (2* self.enemi.aire*self.enemi.vitesse.y + (balle.aire - self.enemi.aire) * balle.vitesse.y  )/(balle.aire + self.enemi.aire)
                        tmp_vit_en = (2* balle.aire*balle.vitesse.y + (self.enemi.aire - balle.aire) * self.enemi.vitesse.y  )/(balle.aire + self.enemi.aire)
                        balle.vitesse.y = tmp_vit_ba
                        self.enemi.vitesse.y = tmp_vit_en
                elif touch == 2:
                        print("Touché en haut")
                        tmp_vit_ba = (2* self.enemi.aire*self.enemi.vitesse.y + (balle.aire - self.enemi.aire) * balle.vitesse.y  )/(balle.aire + self.enemi.aire)
                        tmp_vit_en = (2* balle.aire*balle.vitesse.y + (self.enemi.aire - balle.aire) * self.enemi.vitesse.y  )/(balle.aire + self.enemi.aire)
                        balle.vitesse.y = tmp_vit_ba
                        self.enemi.vitesse.y = tmp_vit_en
        
        if self.angle_balle < 0:
                
                self.angle_balle += 360

        elif self.angle_balle > 360:
                
                self.angle_balle -= 360

        if self.testVitesse == 5:
                
                self.vitesse_balle = self.vitesse_balle + 5
                print("vitesse = ", self.vitesse_balle)
                
        elif self.testVitesse == -5:
                
                self.vitesse_balle = self.vitesse_balle - 5
                print("vitesse = ", self.vitesse_balle)
                
        elif self.testAngle == 5:
                
                self.angle_balle = self.angle_balle + 5
                print("angle = ", self.angle_balle)
                
        elif self.testAngle == -5:
                
                self.angle_balle = self.angle_balle - 5
                print("angle = ",self.angle_balle)

        if self.vitesse_balle < 0:
                self.vitesse_balle = 0

 
    def on_key_press(self, key, modifiers):
            
        global DT
        
        self.angle_balle = int(self.angle_balle)
        self.vitesse_balle = int(self.vitesse_balle)

        if key == arcade.key.ESCAPE:
                
            arcade.close_window()

        elif key == arcade.key.LEFT:
                
                self.testAngle = -5
                print("touche LEFT")
                
        elif key == arcade.key.RIGHT:
                
                self.testAngle = 5
                print("touche RIGHT")
                
        elif key == arcade.key.UP:
                
            self.testVitesse = 5
            print("touche UP")
            
        elif key == arcade.key.DOWN:
                
            self.testVitesse = -5
            print("touche DOWN")
            
        elif key == arcade.key.SPACE:
                
                pos0=Vecteur(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                alpha = self.angle_balle
                alpha = alpha * math.pi / 180 
                V = self.vitesse_balle
                vitX = math.cos(alpha) * V
                vitY = math.cos( math.pi /2 - alpha) * V
                vit0=Vecteur(vitX,vitY)
                r0=10
                couleur=arcade.color.RED
                balle1 = Ball(pos0,vit0,r0,couleur)
                self.Ball_list.append(balle1)

                print("touche ESPACE")

    def on_key_release(self, key, modifiers):
        
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
                
                self.testAngle = 0
                print("relachement touche LEFT/RIGHT")
                
        elif key == arcade.key.UP or key == arcade.key.DOWN:
                
                self.testVitesse = 0
                print("relachement touche UP/DOWN")
                
        elif key == arcade.key.SPACE:
            print("relachement touche ESPACE")


def main():

    window = Balistique(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()
