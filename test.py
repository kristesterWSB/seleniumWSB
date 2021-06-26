import unittest
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

valid_first_name = "Krzys"
valid_last_name = "Nowak"
country_code = "+48"
gender = "male"
obywatelstwo = 'polska'
invalid_email = 'asddsa.com'
password = '1qaz2wsx'
valid_country = 'Polska'


class WizzairRegistration(unittest.TestCase):
    # Warunki wstępne:
    def setUp(self):
        # 1. Uruchomiona przeglądarka
        self.driver = webdriver.Chrome()
        # 2. Na stronie https://wizzair.com/pl-pl#/
        self.driver.get('https://wizzair.com/pl-pl#/')
        self.driver.maximize_window()
        # wlaczenie implicity wait - mechanizm czekania na elementy
        self.driver.implicitly_wait(60)

        # Przypadek testowy 001:
        # Rejestracja przy użyciu błędnego adresu e-mail

    def testInvalidEmail(self):
        # kroki
        driver = self.driver
        # Metoda odszuka element i zwraca WebElement
        # 1.Kliknij przycisk ZALOGUJ SIĘ
        zaloguj_btn = driver.find_element_by_xpath('//button[@data-test="navigation-menu-signin"]')
        zaloguj_btn.click()
        # 2. Kliknij REJESTRACJA
        rejestracja_btn = driver.find_element_by_xpath('//button[@data-test="registration"]')
        rejestracja_btn.click()
        # 3. Wpisz imię
        input_imie = driver.find_element_by_xpath('//input[@name="firstName"]')
        input_imie.send_keys(valid_first_name)
        # 4. Wpisz nazwisko
        input_nazwisko = driver.find_element_by_xpath('//input[@name="lastName"]')
        input_nazwisko.send_keys(valid_last_name)
        # 5. Wybierz płeć
        if gender == "male":
            input_imie.click()
            driver.find_element_by_xpath('//label[@data-test="register-gendermale"]').click()
        else:
            input_nazwisko.click()
            driver.find_element_by_xpath('//label[@data-test="register-genderfemale"]').click()
        # 6. Wpisz kod kraju
        driver.find_element_by_xpath('//div[@class="phone-number__calling-code-selector__empty"]').click()
        kod_kraju_input = driver.find_element_by_xpath('//input[@name="phone-number-country-code"]')
        kod_kraju_input.send_keys(country_code, Keys.RETURN)
        # 7. Wpisz nr telefonu
        input_telefon = driver.find_element_by_xpath('//input[@type="tel"]')
        input_telefon.send_keys('555654456')
        # 8. Wpisz nieprawidłowy zdres e-mail (brak znku '@')
        input_email = driver.find_element_by_xpath('//input[@type="email"]')
        input_email.send_keys(invalid_email)
        # 9. Wpisz hasło
        input_haslo = driver.find_element_by_xpath('//input[@type="password"]')
        input_haslo.send_keys(password)
        # 10. Wybierz narodowość
        wybierz_obywatelstwo = driver.find_element_by_xpath('//input[@data-test="booking-register-country"]')
        wybierz_obywatelstwo.click()
        obywatelstwa = driver.find_elements_by_xpath(
            '//div[@class="register-form__country-container__locations"]/label')
        # Iterujemy po liscie WebElementow
        for label in obywatelstwa:
            # szukamy wewnatrz WebElementu
            option = label.find_element_by_tag_name('strong')
            # Debugowy print - pobranie atrybutu innerText
            # print(option.get_attribute('innerText'))
            # jesli tekst elementu kraju to kraj ktory chcemy wybrac
            if option.get_attribute('innerText') == valid_country:
                # Przewiń do tego kraju
                option.location_once_scrolled_into_view
                # Kliknij w niego
                option.click()
                # Przerwij pętle
                break

        # UWAGA tutaj bedzie prawdziwy test
        # wyszukuje wszystkie bledy
        error_messages = driver.find_elements_by_xpath('//span[@class="input-error__message"]/span')
        # tworze liste widocznych bledow
        visible_error_notices = list()
        for error in error_messages:
            # jesli komunikat jest widoczny
            if error.is_displayed():
                # dodajemy ten komunikat do listy widocznych
                visible_error_notices.append(error)
        # Sprawdzam czy lista widocznych komunikatow zawiera tylko jeden blad
        # assercja czysty PYTHON
        assert len(visible_error_notices) == 1, "liczba widocznych komunikatow nie zgadza sie"
        # Z wykorzystaniem unittest
        self.assertEqual(len(visible_error_notices), 1, msg="liczba widocznych komunikatow nie zgadza sie")
        # Sprawdzam tresc bledu
        self.assertEqual(visible_error_notices[0].text, "Nieprawidłowy adres e-mail")

        # Zarejestruj
        zarejestruj_btn = driver.find_element_by_xpath(
            '//button[@class="base-button base-button--medium base-button--primary base-button--full-width"]')
        zarejestruj_btn.click()
        sleep(5)

    def tearDown(self):
        # zakonczenie testu
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)
