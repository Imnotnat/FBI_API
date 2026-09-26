import unittest

from fbi_api.utils.pdfExtractor import _extract_venue


class ExtractVenueTests(unittest.TestCase):
    def test_full_address_without_phone(self):
        text = ("Adresse de la salle :SALLE OMNISPORTS 67 Av. de Provence 06130 GRASSE (Tél:0493401849)\n"
                "B. GROUPEMENT SPORTIF VISITEUR : US CAGNES SUR MER - 1\n")
        self.assertEqual(_extract_venue(text), "SALLE OMNISPORTS 67 Av. de Provence 06130 GRASSE")

    def test_truncated_phone(self):
        text = "Adresse de la salle :GYMNASE ANDRE CARTON 212 AVENUE DU 11 NOVEMBRE 06700 SAINT-LAURENT-DU-VAR (Tél:06\nB. X"
        self.assertEqual(_extract_venue(text), "GYMNASE ANDRE CARTON 212 AVENUE DU 11 NOVEMBRE 06700 SAINT-LAURENT-DU-VAR")

    def test_no_phone(self):
        text = "Adresse de la salle :AZURARENA ANTIBES 250 RUE EMILE HUGUES 06600 ANTIBES\nB. GROUPEMENT SPORTIF VISITEUR : X"
        self.assertEqual(_extract_venue(text), "AZURARENA ANTIBES 250 RUE EMILE HUGUES 06600 ANTIBES")

    def test_fallback_to_zip_and_city(self):
        text = "Salle quelque part\n06600 ANTIBES\nB. GROUPEMENT"
        self.assertEqual(_extract_venue(text), "06600 ANTIBES")

    def test_nothing_found(self):
        self.assertIsNone(_extract_venue("pas d'adresse ici"))


if __name__ == "__main__":
    unittest.main()
