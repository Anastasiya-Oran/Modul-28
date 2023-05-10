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

class RejectedRequestPageLocators:
    REJECTED_REQUEST_HEADING = (
        By.XPATH, "//h2[contains(text(),'Ваш запрос был отклонен из соображений безопасности.')]")
    REJECTED_REQUEST_INFO = (By.XPATH, "//div[contains(text(),'Код запроса: ')]")
