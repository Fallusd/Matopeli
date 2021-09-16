import math
import pygame
import random
import tkinter as tk
from tkinter import messagebox

#luokka mato koostuu palikoista
class palikka(object):

#pelialueen mitat 400px/16 = 1 kuutio
    rivit = 16
    leveys = 400

#määritellään pelissä käytettävät värit
    valkoinen = (255, 255, 255)
    musta = (0, 0, 0)
    vihrea = (51, 255, 51)
    oranssi = (255, 153, 51)

#konstruktori
    def __init__(self, start, suuntax = 1, suuntay = 0, vari = (vihrea)):

        self.sijainti = start
        self.suuntax = 1
        self.suuntay = 0
        self.vari = vari

#liikkumis metodi
    def liiku(self, suuntax, suuntay):

        self.suuntax = suuntax
        self.suuntay = suuntay
        self.sijainti = (self.sijainti[0] + self.suuntax, self.sijainti[1] + self.suuntay)

    def piirra(self, pinta, silmat = False):

        jako = self.leveys // self.rivit
        i = self.sijainti[0]
        j = self.sijainti[1]

        pygame.draw.rect(pinta, self.vari, (i*jako+1, j*jako+1, jako-2, jako-2))

#piirtää silmät ensimmäiselle kuutiolle
        if silmat:
            keski = jako // 2
            sade = 2
            keskiYmpyra = (i*jako+keski-sade,j*jako+8)
            keskiYmpyra2 = (i*jako + jako -sade*2, j*jako+8)
#piirtää ympyrät silmiksi
            pygame.draw.circle(pinta, (5,200,5), keskiYmpyra, sade)
            pygame.draw.circle(pinta, (5,200,5), keskiYmpyra2, sade)


class mato(object):

    body = []
    kaannokset = {}

#konstruktori
    def __init__(self, vari, sijainti):

        self.vari = vari
        self.paa = palikka(sijainti)
        self.body.append(self.paa)
        self.suuntax = 0
        self.suuntay = 1

    def getValit(self, leveys, rivit):
        valit = leveys // rivit
        return valit

    def getSijainti(self):
        sijainti = self.body[0]
        return sijainti.sijainti

#metodi madon liikkumiselle ja ohjaamiselle   
    def liiku(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()

#asetetaan ohjaimiksi wasd ja nuolinäppäimet

        for key in keys:
            if keys[pygame.K_LEFT]:
                self.suuntax = -1
                self.suuntay = 0
                self.kaannokset[self.paa.sijainti[:]] = [self.suuntax, self.suuntay]

#elif että ei voi painaa enempää kuin yhteen suuntaan samanaikaisesti, aiheuttaa priorisoinnin nappuloissa
            elif keys[pygame.K_a]:
                self.suuntax = -1
                self.suuntay = 0
                self.kaannokset[self.paa.sijainti[:]] = [self.suuntax, self.suuntay]

            elif keys[pygame.K_RIGHT]:
                self.suuntax = 1
                self.suuntay = 0
                self.kaannokset[self.paa.sijainti[:]] = [self.suuntax, self.suuntay]

            elif keys[pygame.K_d]:
                self.suuntax = 1
                self.suuntay = 0
                self.kaannokset[self.paa.sijainti[:]] = [self.suuntax, self.suuntay]

            elif keys[pygame.K_UP]:
                self.suuntax = 0
                self.suuntay = -1
                self.kaannokset[self.paa.sijainti[:]] = [self.suuntax, self.suuntay]

            elif keys[pygame.K_w]:
                self.suuntax = 0
                self.suuntay = -1
                self.kaannokset[self.paa.sijainti[:]] = [self.suuntax, self.suuntay]

            elif keys[pygame.K_DOWN]:
                self.suuntax = 0
                self.suuntay = 1
                self.kaannokset[self.paa.sijainti[:]] = [self.suuntax, self.suuntay]

            elif keys[pygame.K_s]:
                self.suuntax = 0
                self.suuntay = 1
                self.kaannokset[self.paa.sijainti[:]] = [self.suuntax, self.suuntay]

        for i, c in enumerate(self.body):
            p = c.sijainti[:]
            if p in self.kaannokset:
                turn = self.kaannokset[p]
                c.liiku(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.kaannokset.pop(p)

#tarkastetaan ollaanko pelialueen reunalla ja tarvittavat toimenpiteet

            else:
                if c.suuntax == -1 and c.sijainti[0] <= 0: c.sijainti = (c.rivit-1, c.sijainti[1])
                elif c.suuntax == 1 and c.sijainti[0] >= c.rivit-1: c.sijainti = (0,c.sijainti[1])
                elif c.suuntay == 1 and c.sijainti[1] >= c.rivit-1: c.sijainti = (c.sijainti[0], 0)
                elif c.suuntay == -1 and c.sijainti[1] <= 0: c.sijainti = (c.sijainti[0], c.rivit-1)
                else: c.liiku(c.suuntax, c.suuntay)

    def reset(self, sijainti):

        self.paa = palikka(sijainti)
        self.body = []
        self.body.append(self.paa)
        self.kaannokset = {}
        self.suuntax = 0
        self.suuntay = 1

#kun herkku on syöty onnistuneesti lisää palikan madon pituuteen
    def lisaaKuutio(self):

        tail = self.body[-1]
        dx = tail.suuntax
        dy = tail.suuntay

        if dx == 1 and dy == 0:
            self.body.append(palikka((tail.sijainti[0]-1, tail.sijainti[1])))
        elif dx == -1 and dy == 0:
            self.body.append(palikka((tail.sijainti[0]+1, tail.sijainti[1])))
        elif dx == 0 and dy == 1:
            self.body.append(palikka((tail.sijainti[0], tail.sijainti[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(palikka((tail.sijainti[0], tail.sijainti[1]+1)))

        self.body[-1].suuntax = dx
        self.body[-1].suuntay = dy

    def piirra(self, pinta):

        for i, c in enumerate(self.body):
            if i == 0:
                c.piirra(pinta, True)
            else:
                c.piirra(pinta)
    
def alue(leveys, rivit, pinta):

    valit = leveys // rivit

    x = 0
    y = 0

    for i in range(rivit):
        x = x + valit
        y = y + valit


def piirraIkkuna(pinta):

    valkoinen = (255, 255, 255)
    global rivit, leveys, m, herkku
    pinta.fill((valkoinen))
    m.piirra(pinta)
    herkku.piirra(pinta)
    alue(leveys, rivit, pinta)
    pygame.display.update()

def randomHerkku(rivit, item):

    sijainti = item.body

    while True:
        x = random.randrange(rivit)
        y = random.randrange(rivit)

#varmistetaan että herkku ei synny madon sisälle

        if len(list(filter(lambda z:z.sijainti == (x,y), sijainti))) > 0:
            continue
        else:
            break
        
    return (x,y)


def ilmoitus(kohde, sisalto):

    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(kohde, sisalto)
    try:
        root.destroy()
    except:
        pass

def main():

    global leveys, rivit, m, herkku
    leveys = 400
    rivit = 16
    vihrea = (51, 255, 51)
    oranssi = (255, 153, 51)
#pelialue on kuutio joten voidaan käyttää leveyttä korkeuden määrittelyssä
    win = pygame.display.set_mode((leveys, leveys))
    m = mato((vihrea), (8,8))
    herkku = palikka(randomHerkku(rivit, m), vari = (oranssi))
    lippu = False

    clock = pygame.time.Clock()

    while lippu:
#rajoitetaan pelin vauhtia
        pygame.time.delay(40)
        clock.tick(8)
        m.liiku()
#tarkistetaan osuuko madon pää herkkuun
        if m.body[0].sijainti == herkku.sijainti:
            m.lisaaKuutio()
            herkku = palikka(randomHerkku(rivit, m), vari = (oranssi))

        for x in range(len(m.body)):
            if m.body[x].sijainti in list(map(lambda z:z.sijainti, m.body[x+1:])):
                print('Tulos: ', len(m.body))
                ilmoitus('Hävisit', 'Pelaa uudelleen')
                m.reset((10, 10))
                break


        piirraIkkuna(win)

main()