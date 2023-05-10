from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings import random_int


# Конструктор класса. Принимает browser — экземпляр webdriver
class BasePage():
    def __init__(self, browser, url, timeout=5):
        self.browser = browser
        self.url = url
        # команда для неявного ожидания со значением по умолчанию в 5c:
        self.browser.implicitly_wait(timeout)

    # метод find_element ищет один элемент и возвращает его
    def find_element(self, locator, time=10):
        return WebDriverWait(self.browser, time).until(EC.presence_of_element_located(locator),
                                                       message=f"Can't find element by locator {locator}")

    # метод open открывает нужную страницу в браузере, используя метод get()
    def open(self):
        self.browser.get(self.url)

    # метод open_reg_page открывает форму регистрации в браузере, используя метод get()
    def open_reg_page(self):
        self.browser.get(self.url)
        self.find_element(AuthPageLocators.AUTH_REGISTER_LINK).click()

    # метод is_element_present перехватывает исключение
    # будет использоваться для проверки присутствия элемента на странице
    def is_element_present(self, what):
        try:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((what)))
        except (NoSuchElementException):
            return False
        return True

    # метод is_not_element_present будет использоваться для проверки отсутствия элемента на странице
    def is_not_element_present(self, what):
        try:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((what)))
        except (TimeoutException):
            return True
        return False


from settings import valid_phone, valid_email, sql_injection


# from My_pages import BasePage
# from My_pages import AuthPageLocators, ChangePassPageLocators, RejectedRequestPageLocators


class AuthPage(BasePage):
    # RT001 метод проверки перехода на форму авторизации
    def the_authorization_form_is_open(self):
        assert self.is_element_present(AuthPageLocators.AUTH_HEADING)
        assert "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth" in self.browser.current_url, \
            "url do not match"

    # RT002 метод проверки расположения логотипа, слогана и меню выбора типа аутентификации
    def location_of_the_logo_and_slogan(self):
        assert self.is_element_present(AuthPageLocators.AUTH_LOGO), "element not found"
        assert self.is_element_present(AuthPageLocators.AUTH_SLOGAN), "element not found"

    # RT003 метод проверки ссылки на форму восстановления пароля
    def link_to_the_password_recovery_form(self):
        self.find_element(AuthPageLocators.AUTH_FORGOT_PASSWORD_LINK).click()
        assert "https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/reset-credentials" \
               in self.browser.current_url, "url do not match"
        assert self.is_element_present(ChangePassPageLocators.CHANGE_PASS_HEADING), "element not found"

    # RT004 метод проверки ссылки на форму регистрации
    def link_to_the_registration_form(self):
        self.find_element(AuthPageLocators.AUTH_REGISTER_LINK).click()
        assert self.is_element_present(RegPageLocators.REG_HEADING), "element not found"
        assert "https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/registration" \
               in self.browser.current_url, "url do not match"

    # RT005 метод проверки ссылки под кнопкой "Войти" на страницу с пользовательским соглашением
    def link_to_the_user_agreement_page(self):
        original_window = self.browser.current_window_handle
        assert len(self.browser.window_handles) == 1
        self.find_element(AuthPageLocators.AUTH_USER_AGREEMENT_LINK).click()
        for window_handle in self.browser.window_handles:
            if window_handle != original_window:
                self.browser.switch_to.window(window_handle)
            else:
                pass
        assert self.is_element_present(UserAgreementPageLocators.USER_AGREEMENT_HEADING), "element not found"
        assert "https://b2c.passport.rt.ru/sso-static/agreement/agreement.html" in self.browser.current_url, \
            "url do not match"

    # RT006 метод проверки ссылки в футере на страницу с пользовательским соглашением
    def link_fut_to_the_user_agreement_page(self):
        original_window = self.browser.current_window_handle
        assert len(self.browser.window_handles) == 1
        self.find_element(AuthPageLocators.AUTH_PRIVACY_POLICY_LINK).click()
        for window_handle in self.browser.window_handles:
            if window_handle != original_window:
                self.browser.switch_to.window(window_handle)
            else:
                pass
        assert self.is_element_present(UserAgreementPageLocators.USER_AGREEMENT_HEADING), "element not found"
        assert "https://b2c.passport.rt.ru/sso-static/agreement/agreement.html" in self.browser.current_url, \
            "url do not match"

    # RT007 метод проверки ссылки на страницу авторизации с помощью соцсети "ВКонтакте"
    def link_to_social_vk(self):
        self.find_element(AuthPageLocators.AUTH_SOCIAL_VK_LINK).click()
        assert "https://oauth.vk.com/authorize" in self.browser.current_url, "url do not match"

    # RT008 метод проверки авторизации с незаполненными полями
    def authorization_with_blank_fields(self):
        self.find_element(AuthPageLocators.AUTH_TAB_PHONE).click()
        self.find_element(AuthPageLocators.AUTH_ENTER_BUTTON).click()
        assert self.is_element_present(AuthPageLocators.AUTH_ERROR_ENTER_PHONE_NUMBER), "element not found"
        assert "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth" in self.browser.current_url, \
            "url do not match"

    # RT009 метод проверки текстового поля на SQL-инъекции
    def sql_injection_in_a_text_field(self):
        self.find_element(AuthPageLocators.AUTH_USERNAME_INPUT).send_keys(sql_injection())
        self.find_element(AuthPageLocators.AUTH_PASSWORD_INPUT).send_keys(random_int())
        self.find_element(AuthPageLocators.AUTH_ENTER_BUTTON).click()
        assert self.is_element_present(RejectedRequestPageLocators.REJECTED_REQUEST_HEADING), "element not found"
        assert self.is_element_present(RejectedRequestPageLocators.REJECTED_REQUEST_INFO), "element not found"


class ChangePassPage(BasePage):

    # RT010 метод проверки на валидацию поля ввода номера телефона /почты /логина /лицевого счета (ввод валидного номера)
    def phone_field_validation_valid_data(self):
        self.find_element(ChangePassPageLocators.CHANGE_PASS_TAB_PHONE).click()
        phone = valid_phone()
        self.find_element(ChangePassPageLocators.CHANGE_PASS_USERNAME_INPUT).send_keys(phone)
        self.find_element(BaseLocators.BODY).click()
        element = self.find_element(ChangePassPageLocators.CHANGE_PASS_USERNAME_INPUT_VALUE)
        value = element.get_attribute("value")
        assert ("7" + str(phone)) == value, "phone do not match"

    # RT011 метод проверки кнопки на форму авторизации
    def go_back_button(self):
        self.find_element(ChangePassPageLocators.CHANGE_PASS_GO_BACK_BUTTON).click()
        assert self.is_element_present(AuthPageLocators.AUTH_HEADING), "element not found"
        assert "https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/authenticate" in self.browser.current_url, \
            "url do not match"

    # RT012 метод проверки восстановления пароля с незаполненными полями
    def password_recovery_with_blank_fields(self):
        self.find_element(ChangePassPageLocators.CHANGE_PASS_TAB_PHONE).click()
        self.find_element(ChangePassPageLocators.CHANGE_PASS_CONTINUE_BUTTON).click()
        assert "https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/reset-credentials" \
               in self.browser.current_url, "url do not match"
        assert self.is_element_present(ChangePassPageLocators.CHANGE_PASS_ERROR_ENTER_PHONE_NUMBER), \
            "element not found"

    # RT013 метод проверки восстановления пароля с незаполненным значением капчи
    def password_recovery_with_blank_captcha(self):
        self.find_element(ChangePassPageLocators.CHANGE_PASS_TAB_MAIL).click()
        self.find_element(ChangePassPageLocators.CHANGE_PASS_USERNAME_INPUT).send_keys(valid_email())
        self.find_element(ChangePassPageLocators.CHANGE_PASS_CONTINUE_BUTTON).click()
        assert "https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/reset-credentials" \
               in self.browser.current_url, "url do not match"
        assert self.is_element_present(ChangePassPageLocators.CHANGE_PASS_ERROR_INVALID_USERNAME_OR_TEXT), \
            "element not found"


from selenium.webdriver.common.by import By


class BaseLocators:
    BODY = (By.XPATH, "//body")


class AuthPageLocators:
    AUTH_HEADING = (By.XPATH, "//h1[contains(text(),'Авторизация')]")
    AUTH_LOGO = (By.XPATH, "//section[@id='page-left']/*/div[@class='what-is-container__logo-container']/*")
    AUTH_SLOGAN = (By.XPATH,
                   "//section[@id='page-left']/*//p[contains(text(),'Персональный помощник в цифровом мире "
                   "Ростелекома')]")
    AUTH_TAB_MENU = (By.XPATH,
                     "//section[@id='page-right']/*//div[@id='t-btn-tab-phone' or @id='t-btn-tab-mail' or "
                     "@id='t-btn-tab-login' or @id='t-btn-tab-ls']")
    AUTH_USERNAME_INPUT_PLACEHOLDER_TELEPHONE = (By.XPATH, "//span[contains(text(),'Мобильный телефон')]")
    AUTH_USERNAME_INPUT = (By.XPATH, "//input[@id='username']")
    AUTH_USERNAME_INPUT_ACTIV_EMAIL = (By.XPATH, "//span[contains(text(),'Электронная почта')]")
    AUTH_FORGOT_PASSWORD_LINK = (By.XPATH, "//a[@id='forgot_password']")
    AUTH_REGISTER_LINK = (By.XPATH, "//a[@id='kc-register']")
    AUTH_USER_AGREEMENT_LINK = (By.XPATH,
                                "//span[contains(text(),'Нажимая кнопку «Войти», вы принимаете "
                                "условия')]/following-sibling::a")
    AUTH_PRIVACY_POLICY_LINK = (By.XPATH, "//a[@id='rt-footer-agreement-link']")
    AUTH_SOCIAL_VK_LINK = (By.XPATH, "//a[@id='oidc_vk']")
    AUTH_TAB_PHONE = (By.XPATH, "//div[@id='t-btn-tab-phone']")
    AUTH_ENTER_BUTTON = (By.XPATH, "//button[@id='kc-login']")
    AUTH_ERROR_ENTER_PHONE_NUMBER = (By.XPATH, "//span[contains(text(),'Введите номер телефона')]")
    AUTH_PASSWORD_INPUT = (By.XPATH, "//input[@id='password']")


class ChangePassPageLocators:
    CHANGE_PASS_HEADING = (By.XPATH, "//h1[contains(text(),'Восстановление пароля')]")
    CHANGE_PASS_USERNAME_INPUT_PLACEHOLDER_TELEPHONE = (By.XPATH, "//span[contains(text(),'Мобильный телефон')]")
    CHANGE_PASS_TAB_PHONE = (By.XPATH, "//div[@id='t-btn-tab-phone']")
    CHANGE_PASS_USERNAME_INPUT = (By.XPATH, "//input[@id='username']")
    CHANGE_PASS_USERNAME_INPUT_VALUE = (By.XPATH, "//input[@name='username']")
    CHANGE_PASS_TAB_MAIL = (By.XPATH, "//div[@id='t-btn-tab-mail']")
    CHANGE_PASS_GO_BACK_BUTTON = (By.XPATH, "//button[@id='reset-back']")
    CHANGE_PASS_PRIVACY_POLICY_LINK = (By.XPATH, "//a[@id='rt-footer-agreement-link']")
    CHANGE_PASS_CONTINUE_BUTTON = (By.XPATH, "//button[@id='reset']")
    CHANGE_PASS_ERROR_ENTER_PHONE_NUMBER = (By.XPATH, "//span[contains(text(),'Введите номер телефона')]")
    CHANGE_PASS_ERROR_INVALID_USERNAME_OR_TEXT = (
        By.XPATH, "//span[@id='form-error-message' and contains(text(),'Неверный логин или текст с картинки')]")


class RegPageLocators:
    REG_HEADING = (By.XPATH, "//h1[contains(text(),'Регистрация')]")
    REG_FIRST_NAME_INPUT_PAGE_RIGHT = (
        By.XPATH, "//section[@id='page-right']//span[contains(text(),'Имя')]/preceding-sibling::input")
    REG_REGISTER_BUTTON_PAGE_RIGHT = (
        By.XPATH, "//section[@id='page-right']//span[contains(text(),'Зарегистрироваться')]")
    REG_USER_AGREEMENT_LINK_PAGE_RIGHT = (By.XPATH,
                                          "//section[@id='page-right']//span[contains(text(),'Нажимая кнопку "
                                          "«Зарегистрироваться», вы принимаете условия')]/following-sibling::a")
    REG_FIRST_NAME_INPUT = (By.XPATH, "//span[contains(text(),'Имя')]/preceding-sibling::input")
    REG_ERROR_FIRST_NAME_INPUT = (
        By.XPATH, "//span[contains(text(),'Необходимо заполнить поле кириллицей. От 2 до 30 с')]")
    REG_EMAIL_PHONE_INPUT = (By.XPATH, "//input[@id='address']")
    REG_EMAIL_PHONE_INPUT_VALUE = (By.XPATH, "//input[@type='hidden' and @name='address']")
    REG_ERROR_INVALID_EMAIL_OR_PHONE_INPUT = (
        By.XPATH, "//span[contains(text(),'Введите телефон в формате +7ХХХХХХХХХХ или +375XXX')]")
    REG_PASSWORD_INPUT = (By.XPATH, "//input[@id='password']")
    REG_ERROR_INVALID_PASSWORD_INPUT = (
        By.XPATH, "//span[contains(text(),'Пароль должен') or contains(text(),'Длина пароля')]")
    REG_LAST_NAME_INPUT = (By.XPATH, "//span[contains(text(),'Фамилия')]/preceding-sibling::input")
    REG_PASSWORD_CONFIRM_INPUT = (By.XPATH, "//input[@id='password-confirm']")
    REG_ENTER_BUTTON = (
        By.XPATH, "//button[@class='rt-btn rt-btn--orange rt-btn--medium rt-btn--rounded register-form__reg-btn']")
    REG_USER_AGREEMENT_LINK = (By.XPATH,
                               "//span[contains(text(),'Нажимая кнопку «Зарегистрироваться», "
                               "вы принимаете условия')]/following-sibling::a")
    REG_PRIVACY_POLICY_LINK = (By.XPATH, "//a[@id='rt-footer-agreement-link']")
    REG_ERROR_PASSWORD_DONT_MATCH = (By.XPATH, "//span[contains(text(),'Пароли не совпадают')]")


class EmailConfirmPageLocators:
    EMAIL_CONF_HEADING = (By.XPATH, "//p[contains(text(),'Kод подтверждения отправлен')]")


class UserAgreementPageLocators:
    USER_AGREEMENT_HEADING = (By.XPATH, "//h1[contains(text(),'Пользователь')]")


class RejectedRequestPageLocators:
    REJECTED_REQUEST_HEADING = (
        By.XPATH, "//h2[contains(text(),'Ваш запрос был отклонен из соображений безопасности.')]")
    REJECTED_REQUEST_INFO = (By.XPATH, "//div[contains(text(),'Код запроса: ')]")


# from My_pages import BasePage
# from My_pages import BaseLocators, RegPageLocators, EmailConfirmPageLocators, UserAgreementPageLocators


class RegPage(BasePage):

    # RT014 метод проверки валидации текстового поля (ввод валидных данных)
    def text_field_validation_valid_data(self, input_text):
        self.find_element(RegPageLocators.REG_FIRST_NAME_INPUT).send_keys(input_text)
        self.find_element(BaseLocators.BODY).click()
        assert self.is_not_element_present(RegPageLocators.REG_ERROR_FIRST_NAME_INPUT), "element found"

    # RT015 метод проверки на валидацию поля ввода email или мобильного телефона (ввод валидных данных)
    def email_or_phone_field_validation_valid_data(self, input_text):
        self.find_element(RegPageLocators.REG_EMAIL_PHONE_INPUT).send_keys(input_text)
        self.find_element(BaseLocators.BODY).click()
        element = self.find_element(RegPageLocators.REG_EMAIL_PHONE_INPUT_VALUE)
        value = element.get_attribute("value")
        assert input_text == value, "email or phone do not match"
        assert self.is_not_element_present(RegPageLocators.REG_ERROR_INVALID_EMAIL_OR_PHONE_INPUT), "element found"

    # RT016 метод проверки на валидацию поля ввода пароля (ввод валидных данных)
    def password_field_validation_valid_data(self, input_text):
        self.find_element(RegPageLocators.REG_PASSWORD_INPUT).send_keys(input_text)
        self.find_element(BaseLocators.BODY).click()
        assert self.is_not_element_present(RegPageLocators.REG_ERROR_INVALID_PASSWORD_INPUT), "element found"

    # RT017 метод проверки регистрации с валидными данными
    def registration_with_valid_data(self, first_name, last_name, email_phone, password):
        self.find_element(RegPageLocators.REG_FIRST_NAME_INPUT).send_keys(first_name)
        self.find_element(RegPageLocators.REG_LAST_NAME_INPUT).send_keys(last_name)
        self.find_element(RegPageLocators.REG_EMAIL_PHONE_INPUT).send_keys(email_phone)
        self.find_element(RegPageLocators.REG_PASSWORD_INPUT).send_keys(password)
        self.find_element(RegPageLocators.REG_PASSWORD_CONFIRM_INPUT).send_keys(password)
        self.find_element(RegPageLocators.REG_ENTER_BUTTON).click()
        assert self.is_element_present(EmailConfirmPageLocators.EMAIL_CONF_HEADING), "element not found"

    # RT018 метод проверки ссылки под кнопкой "Зарегистрироваться" на страницу с пользовательским соглашением
    def link_to_the_user_agreement_page(self):
        original_window = self.browser.current_window_handle
        assert len(self.browser.window_handles) == 1
        self.find_element(RegPageLocators.REG_USER_AGREEMENT_LINK).click()
        for window_handle in self.browser.window_handles:
            if window_handle != original_window:
                self.browser.switch_to.window(window_handle)
            else:
                pass
        assert self.is_element_present(UserAgreementPageLocators.USER_AGREEMENT_HEADING), "element not found"
        assert "https://b2c.passport.rt.ru/sso-static/agreement/agreement.html" in self.browser.current_url, \
            "url do not match"

    # RT019 метод проверки валидации текстового поля (ввод невалидных данных)
    def text_field_validation_invalid_data(self, input_text):
        self.find_element(RegPageLocators.REG_FIRST_NAME_INPUT).send_keys(input_text)
        self.find_element(BaseLocators.BODY).click()
        assert self.is_element_present(RegPageLocators.REG_ERROR_FIRST_NAME_INPUT), "element not found"

    # RT020 метод проверки валидации поля ввода email или мобильного телефона (ввод невалидных данных)
    def email_or_phone_field_validation_invalid_data(self, input_text):
        self.find_element(RegPageLocators.REG_EMAIL_PHONE_INPUT).send_keys(input_text)
        self.find_element(BaseLocators.BODY).click()
        assert self.is_element_present(RegPageLocators.REG_ERROR_INVALID_EMAIL_OR_PHONE_INPUT), "element not found"

    # RT021 метод проверки валидации поля ввода пароля (ввод невалидных данных)
    def password_field_validation_invalid_data(self, input_text):
        self.find_element(RegPageLocators.REG_PASSWORD_INPUT).send_keys(input_text)
        self.find_element(BaseLocators.BODY).click()
        assert self.is_element_present(RegPageLocators.REG_ERROR_INVALID_PASSWORD_INPUT), "element not found"

    # RT022 метод проверки заполнения поля подтверждения пароля данными, отличными от введенных в поле ввода пароля
    def entering_data_in_the_password_confirmation_field(self, password1, password2):
        self.find_element(RegPageLocators.REG_PASSWORD_INPUT).send_keys(password1)
        self.find_element(RegPageLocators.REG_PASSWORD_CONFIRM_INPUT).send_keys(password2)
        self.find_element(RegPageLocators.REG_ENTER_BUTTON).click()
        assert self.is_element_present(RegPageLocators.REG_ERROR_PASSWORD_DONT_MATCH), "element not found"


def auth_page():
    return None
