import os
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException


class Macro:
    def __init__(self, stu_no, pw, grade, index, method):
        self.__driver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'))
        self.__grade = grade
        self.__index = index
        self.__stu_no = stu_no
        self.__pw = pw
        self.__method = method
        self.__LOOP_CNT = 500

    def run(self):
        if not self.__is_valid_params():
            print("params Error")
            return False

        self.__open_browser()
        self.__login()
        self.__enter_registration_page()

        if self.__has_remaining_seat():
            self.__register()
            return False
        else:
            self.close_browser()
            return True
    
    # 유효성 검증
    # 전공 선택, grade 없으면 오류
    def __is_valid_params(self):
        if self.__is_register_major():
            if not self.__grade:
                return False

        return True

    def __open_browser(self):
        self.__driver.implicitly_wait(3)
        self.__driver.get('http://all.jbnu.ac.kr/jbnu/sugang/')
        self.__driver.maximize_window()

    def __login(self):
        stu_no_id = 'mainframe_VFrameSet_LoginFrame_form_div_login_div_form_edt_hakbun_input'
        pw_id = 'mainframe_VFrameSet_LoginFrame_form_div_login_div_form_edt_passwd_input'
        stu_no = self.__driver.find_element_by_id(stu_no_id)
        pw = self.__driver.find_element_by_id(pw_id)

        login_xpath = '//*[@id="mainframe_VFrameSet_LoginFrame_form_div_login_div_form_btn_login"]/div'
        login = self.__driver.find_element_by_xpath(login_xpath)

        try:
            stu_no.click()
            stu_no.send_keys(self.__stu_no)
            pw.click()
            pw.send_keys(self.__pw)
            login.click()
        except AttributeError:  # 가끔 일어나는 js 오류 처리 -> 자세한 확인 필요함
            return True

    def __enter_registration_page(self):
        sugang_xpath = '//*[@id="mainframe_VFrameSet_TopFrame_form_div_top_mnu_topmenu_0001TextBoxElement"]/div'

        try:
            sleep(0.5)
            sugang = self.__driver.find_element_by_xpath(sugang_xpath)
            sugang.click()
        except ElementNotInteractableException:
            ok_xpath = '//*[@id="mainframe_VFrameSet_LoginFrame_COM_ALERT_form_btn_closeTextBoxElement"]'
            ok = self.__driver.find_element_by_xpath(ok_xpath)
            ok.click()
            login_xpath = '//*[@id="mainframe_VFrameSet_LoginFrame_form_div_login_div_form_btn_login"]/div'
            login = self.__driver.find_element_by_xpath(login_xpath)
            login.click()
            sugang = self.__driver.find_element_by_xpath(sugang_xpath)
            sugang.click()
        finally:
            # self.input_code()
            pass

    def __input_code(self):
        code_id = 'mainframe_VFrameSet_TopFrame_COM_CHECK_form_Edit00_input'
        code_okay_id = 'mainframe_VFrameSet_TopFrame_COM_CHECK_form_btnOKTextBoxElement'
        final_okay_id = 'mainframe_VFrameSet_TopFrame_COM_ALERT_form_Static00'
        code = self.__driver.find_element_by_id(code_id)
        code.click()
        code.send_keys(self.__get_code())
        sleep(0.5)
        okay = self.__driver.find_element_by_id(code_okay_id)
        okay.click()
        sleep(0.5)
        self.__driver.find_element_by_id(final_okay_id).click()
        sleep(0.3)

    def __get_code(self):
        html = self.__driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.find('div',
                         {'id': 'mainframe_VFrameSet_TopFrame_COM_CHECK_form_div_pattern_sta_codeTextBoxElement'})
        return divs.div.text

    # 전공 신청 여부 함수
    def __is_register_major(self):
        return self.__method == 0

    def __has_remaining_seat(self):
        # 전공 / 장바구니 신청에 맞는 spinner
        spinner1, spinner2 = self.__set_spinner()

        for _ in range(self.__LOOP_CNT):
            if self.__get_remaining_seat() > 0:
                return True
            self.__refresh(spinner1, spinner2)
            sleep(0.5)

        return False

    def __set_spinner(self):
        if self.__is_register_major():
            return self.__set_spinner_major()
        if not self.__is_register_major():
            return self.__set_spinner_basket()

    # 전공 신청할 때 spinner
    def __set_spinner_major(self):
        spinner1_xpath = '//*[@id="mainframe_VFrameSet_WorkFrame_form_div_work_div_search_cbo_shyr"]/div'
        spinner1 = self.__driver.find_element_by_xpath(spinner1_xpath)
        spinner1.click()

        spinner2_xpath = '//*[@id="mainframe_VFrameSet_WorkFrame_form_div_work_div_search_cbo_shyr_comboedit_input"]'
        spinner2 = self.__driver.find_element_by_xpath(spinner2_xpath)
        for _ in range(self.__grade + 1):
            spinner2.send_keys(Keys.DOWN)
            spinner2.send_keys(Keys.RETURN)

        return spinner1, spinner2

    # 장바구니 신청할 때 spinner (btns)
    # 장바구니 신청할 때는 장바구니 btn -> (과목이 적은) 군사학 btn -> 장바구니 btn -> 군사학 -> ... 반복하면서 확인
    def __set_spinner_basket(self):
        # spinner1 -> 장바구니 btn
        basket_id = 'mainframe_VFrameSet_WorkFrame_form_div_work_btn_rsrvCourTextBoxElement'
        basket_btn = self.__driver.find_element_by_id(basket_id)

        # spinner2 -> 군사학 btn
        other_id = 'mainframe_VFrameSet_WorkFrame_form_div_work_btn_milTextBoxElement'
        other_btn = self.__driver.find_element_by_id(other_id)

        basket_btn.click()
        return basket_btn, other_btn

    def __get_remaining_seat(self):
        current_id = 'mainframe_VFrameSet_WorkFrame_form_div_work_grd_gwam_body_gridrow_' + str(self.__index) + \
                     '_cell_' + str(self.__index) + '_7GridCellTextSimpleContainerElement'
        total_id = 'mainframe_VFrameSet_WorkFrame_form_div_work_grd_gwam_body_gridrow_' + str(self.__index) + \
                   '_cell_' + str(self.__index) + '_8GridCellTextSimpleContainerElement'

        current = self.__driver.find_element_by_id(current_id)
        total = self.__driver.find_element_by_id(total_id)

        return int(total.text) - int(current.text)

    # method에 따른 refresh를 내부에서 다르게 실행
    def __refresh(self, spinner1, spinner2):
        if self.__is_register_major():
            self.__refresh_major(spinner1, spinner2)
        if not self.__is_register_major():
            self.__refresh_basket(basket_btn=spinner1, other_btn=spinner2)

    def __refresh_major(self, spinner1, spinner2):
        spinner1.click()
        spinner2.send_keys(Keys.DOWN)
        spinner2.send_keys(Keys.RETURN)
        spinner1.click()
        spinner2.send_keys(Keys.UP)
        spinner2.send_keys(Keys.RETURN)

    # 장바구니 신청 시 버튼을 번갈아가면서 클릭
    def __refresh_basket(self, basket_btn, other_btn):
        other_btn.click()
        sleep(0.25)
        basket_btn.click()

    def __register(self):
        btn_id = 'mainframe_VFrameSet_WorkFrame_form_div_work_grd_gwam_body_gridrow_' + str(self.__index) + \
                 '_cell_' + str(self.__index) + '_0_controlbuttonTextBoxElement'
        btn = self.__driver.find_element_by_id(btn_id)
        btn.click()

    def close_browser(self):
        self.__driver.quit()
