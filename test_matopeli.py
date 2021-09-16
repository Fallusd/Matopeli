import unittest
import matopeli
from matopeli import mato
from matopeli import palikka
import pygame


class TestMatopeli(unittest.TestCase):

    def setUp(self):
        self.m = mato(8,8)

#testataan että mato lähtee oikeasta paikasta liikkeelle
    def test_mato_oikeassa_paikassa(self):
        madon_sijainti = self.m.getSijainti()
        self.assertEqual(madon_sijainti,(8,8))

#tarkastaa muodostaako peli "ruudukon" oikein
    def test_valit(self):
       result = self.m.getValit(400, 16)
       self.assertEqual(result, 25)

if __name__ == '__main__':
    unittest.main()