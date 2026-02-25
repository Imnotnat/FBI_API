from datetime import datetime
import logging
import re
from datetime import date
from typing import Any, Dict, List, Optional
from playwright.sync_api import sync_playwright, TimeoutError
from fbi_api.utils.pdfExtractor import _extract_data_from_pdf

from fbi_api.utils.utils import _format_date_for_input

logger = logging.getLogger(__name__)

FBI_BASE_URL="https://extranet.ffbb.com/fbi"
FBI_LOGIN_URL="https://extranet.ffbb.com/fbi/connexion.fbi"
FBI_DESIGNATION_URL="https://extranet.ffbb.com/fbi/rechercherRepartitionSaisieOfficiel.fbi"

# Timeouts in milliseconds
NAVIGATION_TIMEOUT = 30000
LOGIN_TIMEOUT = 10000
DOWNLOAD_TIMEOUT = 30000  # Temps max pour télécharger un PDF

"""
Browser class to handle Playwright interactions with the FBI website, including login and data retrieval.
"""
class Browser:

    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None

    def start_browser(self):
        """Start the Playwright browser"""
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(
                headless=self.headless
            )
            context = self.browser.new_context()
            self.page = context.new_page()
            logger.info("FBI scraper browser started")
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            raise
    
    def close_browser(self):
        """Close the browser and cleanup."""
        if self.browser:
            try:
                self.browser.close()
                logger.info("FBI scraper browser closed")
            except Exception as e:
                logger.warning(f"Error closing browser: {e}")
        
        # Stop the playwright instance to clean up the event loop
        if self.playwright:
            try:
                self.playwright.stop()
                self.playwright = None
                logger.debug("FBI scraper playwright instance stopped")
            except Exception as e:
                logger.warning(f"Error stopping playwright: {e}")

    def __enter__(self):
        """Context manager entry - starts the browser."""
        self.start_browser()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes the browser."""
        self.close_browser()

    def login(self,user) -> bool:
        """
        Log in to the FBI website using stored credentials.
        """
        if not self.page:
            logger.error("Browser not initialized")
            return False

        try:
            logger.info(f"Navigating to FBI login page: {FBI_LOGIN_URL}")
            self.page.goto(FBI_LOGIN_URL, timeout=NAVIGATION_TIMEOUT)

            # Wait for login form
            self.page.wait_for_selector('input[name="username"], input[type="email"], input#username, input[id="materialLoginFormEmail"]',
                                       timeout=LOGIN_TIMEOUT)

            # Fill username
            username_selectors = [
                'input[name="username"]', 'input[type="email"]', 'input#username',
                'input#email', 'input[name="email"]', 'input[id="materialLoginFormEmail"]'
            ]
            username_filled = False
            for selector in username_selectors:
                if self.page.locator(selector).count() > 0:
                    self.page.fill(selector, user.username)
                    username_filled = True
                    break

            if not username_filled:
                logger.error("Could not find username input field")
                return False

            # Fill password
            password_selectors = ['input[name="password"]', 'input[type="password"]', 'input#password']
            password_filled = False
            for selector in password_selectors:
                if self.page.locator(selector).count() > 0:
                    self.page.fill(selector, user.password)
                    password_filled = True
                    break

            if not password_filled:
                logger.error("Could not find password input field")
                return False

            # Submit
            submit_selectors = [
                'button[type="submit"]', 'input[type="submit"]',
                'button:has-text("Login")', 'button:has-text("Sign in")', 'button:has-text("Connexion")'
            ]
            for selector in submit_selectors:
                if self.page.locator(selector).count() > 0:
                    self.page.click(selector)
                    break

            self.page.wait_for_load_state('networkidle', timeout=NAVIGATION_TIMEOUT)

            # Check errors
            error_indicators = ['.text-danger']
            for indicator in error_indicators:
                if self.page.locator(indicator).count() > 0:
                    logger.error("Login failed: Invalid credentials")
                    return False

            logger.info("FBI login successful")
            return True
        except TimeoutError as e:
            logger.error(f"Timeout during login: {e}")
            return False
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False

"""
BrowserDownload extends Browser to add specific methods for navigating the FBI designations page and applying date filters.
"""
class BrowserDownload(Browser):

    def start_browserDownload(self):
        """Start the Playwright browser with download capabilities."""
        try:
            self.playwright = sync_playwright().start()
            # On configure le dossier de téléchargement temporaire
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                downloads_path="./temp_downloads"
            )
            # Important : accept_downloads=True
            context = self.browser.new_context(accept_downloads=True)
            self.page = context.new_page()
            logger.info("FBI scraper browser started")
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            raise
    
    def navigate_to_designations(self) -> bool:
        """
        Navigate to the referee designation page and click Search.
        """
        if not self.page:
            raise Exception("Browser not initialized")

        try:
            logger.info(f"Navigating to designations page: {FBI_DESIGNATION_URL}")
            self.page.goto(FBI_DESIGNATION_URL, timeout=NAVIGATION_TIMEOUT)
            self.page.wait_for_load_state('networkidle', timeout=NAVIGATION_TIMEOUT)

        except Exception as e:
            logger.error(f"Error navigating to designations: {e}")
            return False

    def _apply_date_filters(self, start_date: str, end_date: str):
        """
        Fill the date filters on the FBI search page before triggering the search.
        """
        if not self.page:
            return

        start_date = _format_date_for_input(start_date)
        end_date = _format_date_for_input(end_date)

        if not start_date and not end_date:
            return

        try:
            if start_date:
                self.page.evaluate("""
                (value) => {
                    const input = document.querySelector(
                        'input[name="repartitionOfficielForm.rechercherRepartitionSaisieOfficielsBean.dateDebutPeriode"]'
                    );
                    input.value = value;
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                }
                 """, start_date)

                logger.info(f"Set FBI start date filter to {start_date}")
            if end_date:
                self.page.evaluate("""
                (value) => {
                    const input = document.querySelector(
                        'input[name="repartitionOfficielForm.rechercherRepartitionSaisieOfficielsBean.dateFinPeriode"]'
                    );
                    input.value = value;
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                }
                """, end_date)
                logger.info(f"Set FBI end date filter to {end_date}")
        except Exception as exc:
            logger.warning(f"Unable to apply date filters on FBI page: {exc}")

    def provideGames(self):
        # Click Search button
        search_selectors = ['button[id="rechercher"]', 'button[name="search"]']
        search_clicked = False
        for selector in search_selectors:
            if self.page.locator(selector).count() > 0:
                self.page.click(selector)
                search_clicked = True
                logger.debug(f"Clicked search using selector: {selector}")
                break

        if not search_clicked:
            logger.warning("Search button not found, checking if table exists anyway...")

        # Wait for table
        try:
            self.page.wait_for_selector('table', timeout=LOGIN_TIMEOUT)
            logger.info("Designation table found")
            return True
        except:
            logger.warning("Could not find designation table immediately")
            return True
        
    def getGames(self) -> List[Dict[str, Any]]:
        """
        Scrape toutes les pages en se basant sur le nombre total d'entrées affiché
        dans le div 'dataTables_info'.
        """
        if not self.page:
            return []

        matches = []
        failed_matches = []  # Track failed scraping attempts

        # 1. On attend que le tableau et l'info de pagination soient chargés
        print("\n⏳ Attente du chargement du tableau...")
        try:
            # On attend que le texte "Affichage de..." soit visible
            # Note : J'utilise l'ID que tu m'as donné
            info_selector = "#rechercherRepartitionSaisieOfficielAjax_info"
            self.page.wait_for_selector(info_selector, state="visible", timeout=10000)
            self.page.wait_for_selector('tr:has(.imgPrint)', state="visible", timeout=5000)
        except Exception as e:
            print("⚠️ Le tableau ou le texte d'info n'est pas apparu.")
            logger.error(f"Table load error: {e}")
            return []

        # 2. On récupère le nombre TOTAL de matchs à scrapper
        try:
            info_text = self.page.locator(info_selector).inner_text()
            # Ex: "Affichage de 21 à 25 sur 25 entrées"
            print(f"ℹ️ Texte détecté : {info_text}")

            # Regex pour trouver le nombre après "sur" et avant "entrées"
            # On cherche "sur", des espaces, des chiffres (\d+), des espaces, "entrées"
            match_count = re.search(r"sur\s+(\d+)\s+entrées", info_text)

            if match_count:
                total_matches_expected = int(match_count.group(1))
                print(f"🎯 Objectif : Récupérer {total_matches_expected} matchs au total.")
            else:
                print("⚠️ Impossible de lire le nombre total d'entrées. Arrêt.")
                return []

        except Exception as e:
            print(f"💥 Erreur lors de la lecture du nombre de matchs : {e}")
            return []

        page_number = 1

        # 3. Boucle principale - count both successes and failures
        while len(matches) + len(failed_matches) < total_matches_expected:
            print(
                f"\n📄 Traitement de la page {page_number} (Matchs récupérés : {len(matches)}/{total_matches_expected}, Échecs : {len(failed_matches)})")

            # Récupération des lignes
            rows = self.page.locator('tr:has(.imgPrint)').all()

            # Traitement des lignes de la page actuelle
            for idx, row in enumerate(rows):
                # Petite sécurité pour ne pas scrapper des doublons si la pagination déconne
                # (Optionnel, dépend de la robustesse de ton _process_row_pdf)
                try:
                    match_data = self._process_row_pdf(row, idx)
                    if match_data:
                        matches.append(match_data)
                    else:
                        # If _process_row_pdf returns None, count it as a failure
                        print("⚠️ Aucune donnée extraite de cette ligne.")
                        #TODO self._track_failed_match(failed_matches, idx, page_number, "No data extracted")
                except Exception as e:
                    print("TODO")
                    # Log the error and track the failure
                    #TODO self._track_failed_match(failed_matches, idx, page_number, str(e))

            # Condition de sortie : Si on a tout récupéré (succès + échecs)
            if len(matches) + len(failed_matches) >= total_matches_expected:
                print(f"✅ Traitement terminé ! {len(matches)} matchs récupérés, {len(failed_matches)} échecs.")
                break

            # 4. Changement de page
            print("➡️ Passage à la page suivante...")

            # Sélecteur pour le bouton suivant.
            # Dans DataTables, le bouton suivant a souvent la classe 'next' ou le texte 'Suivant'
            # On essaie de cliquer sur le lien qui contient le texte "Suivant"
            try:
                # On cherche un lien (<a>) qui a la classe "next" (standard DataTables)
                # OU un lien qui contient le texte "Suivant"
                next_btn = self.page.locator(".paginate_button.next")

                # Si le sélecteur par classe ne marche pas, essaye :
                # next_btn = self.page.get_by_text("Suivant", exact=True)

                if next_btn.is_visible():
                    next_btn.click()
                    page_number += 1

                    # IMPORTANT : Attendre que le tableau change.
                    # On attend une petite seconde pour laisser l'AJAX se faire
                    self.page.wait_for_timeout(1000)
                else:
                    print("⚠️ Bouton suivant non trouvé mais total non atteint.")
                    break

            except Exception as e:
                print(f"⚠️ Erreur lors du clic sur Suivant : {e}")
                break

        # Log failed matches if any
        if failed_matches:
            logger.warning(f"Failed to scrape {len(failed_matches)} matches:")
            for i, failure in enumerate(failed_matches[:20], 1):
                logger.warning(f"  {i}. {failure}")
            if len(failed_matches) > 20:
                logger.warning(f"  ... and {len(failed_matches) - 20} more.")

        # Update stats for notification
        # TODO self.scrape_stats['successes'] = len(matches)
        #TODO self.scrape_stats['failures'] = len(failed_matches)

        logger.info(f"Successfully scraped {len(matches)} matches, {len(failed_matches)} failures")
        return matches

    def _process_row_pdf(self, row, index: int) -> Optional[Dict[str, Any]]:
        """
        Click the PDF button using JS evaluation to bypass viewport issues.
        """
        pdf_path = None
        try:
            # Sélecteur basé sur tes infos (.imgPrint)
            print_btn = row.locator('.imgPrint').first

            # On vérifie juste la présence dans le DOM, pas la visibilité
            if print_btn.count() == 0:
                return None

            logger.debug(f"Row {index}: Triggering download...")

            # Gestion du téléchargement
            with self.page.expect_download(timeout=DOWNLOAD_TIMEOUT) as download_info:
                # CORRECTION ICI :
                # Au lieu de .click(force=True) qui échoue parfois sur les éléments hors vue,
                # on utilise .evaluate() pour exécuter le clic directement en JavaScript dans le navigateur.
                # Cela contourne les problèmes de viewport, de scroll et d'overlay.
                print_btn.evaluate("element => element.click()")

            download = download_info.value
            pdf_path = download.path()

            # Parsing du fichier téléchargé
            match_data = _extract_data_from_pdf(pdf_path)

            if match_data and not hasattr(match_data, 'unique_id'):
                match_data.unique_id = f"FBI_PDF_ROW_{index}_{date.today()}"

            return match_data

        except Exception as e:
            logger.error(f"Error processing PDF for row {index}: {e}")
            return None