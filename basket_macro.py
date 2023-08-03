import os
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException


class BasketMacro:
    def __init__(self, stu_no, pw, index):
        self.__driver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'))
        self.__index = index
        self.__stu_no = stu_no
        self.__pw = pw
        self.__LOOP_CNT = 500

    def run(self):
        try:
            self.__open_browser()
            self.__login()
            self.__enter_registration_page()

            if self.__has_remaining_seat():
                self.__register()
                print("Congraturation!")
                current_id = 'mainframe_VFrameSet_WorkFrame_form_div_work_grd_gwam_body_gridrow_' + str(self.__index) + \
                     '_cell_' + str(self.__index) + '_8GridCellTextSimpleContainerElement'
                total_id = 'mainframe_VFrameSet_WorkFrame_form_div_work_grd_gwam_body_gridrow_' + str(self.__index) + \
                        '_cell_' + str(self.__index) + '_9GridCellTextSimpleContainerElement'

                current = self.__driver.find_element_by_id(current_id)
                total = self.__driver.find_element_by_id(total_id)

                current_text = current.text
                total_text = total.text
                
                print("Current:", current_text)
                print("Total:", total_text)
                self.__register()
                return False
            else:
                return True
        except Exception as e:
            print("An error occurred:", e)
            return False
        finally:
            self.close_browser()

    def __open_browser(self):
        self.__driver.implicitly_wait(3)
        self.__driver.get('http://all.jbnu.ac.kr/jbnu/sugang/')
        self.__driver.maximize_window()

    def __login(self):
        stu_no_id = 'mainframe_VFrameSet_LoginFrame_form_div_login_div_form_edt_hakbun_input'
        pw_id = 'mainframe_VFrameSet_LoginFrame_form_div_login_div_form_edt_passwd_input'
        stu_no = self.__driver.find_element_by_id(stu_no_id)
        pw = self.__driver.find_element_by_id(pw_id)

        login_xpath = '//*[@id="mainframe_VFrameSet_LoginFrame_form_div_login_div_form_btn_login"]'
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
        sugang_xpath = '//*[@id="mainframe_VFrameSet_TopFrame_form_div_top_mnu_topmenu_0001TextBoxElement"]'
        try:
            sleep(0.5)
            sugang = self.__driver.find_element_by_xpath(sugang_xpath)
            sugang.click()
        except ElementNotInteractableException:
            ok_xpath = '//*[@id="mainframe_VFrameSet_LoginFrame_COM_ALERT_form_btn_close"]'
            ok = self.__driver.find_element_by_xpath(ok_xpath)
            ok.click()
            login_xpath = '//*[@id="mainframe_VFrameSet_LoginFrame_form_div_login_div_form_btn_login"]'
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

    def __has_remaining_seat(self):
        spinner1, spinner2 = self.__set_spinner()

        for _ in range(self.__LOOP_CNT):
            if self.__get_remaining_seat() > 0:
                return True
            self.__refresh(spinner1, spinner2)
            sleep(0.5)

        return False
    
    # 장바구니 신청할 때 spinner (btns)
    # 장바구니 신청할 때는 장바구니 btn -> (과목이 적은) 군사학 btn -> 장바구니 btn -> 군사학 -> ... 반복하면서 확인
    def __set_spinner(self):
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
                     '_cell_' + str(self.__index) + '_8GridCellTextSimpleContainerElement'
        total_id = 'mainframe_VFrameSet_WorkFrame_form_div_work_grd_gwam_body_gridrow_' + str(self.__index) + \
                   '_cell_' + str(self.__index) + '_9GridCellTextSimpleContainerElement'

        current = self.__driver.find_element_by_id(current_id)
        total = self.__driver.find_element_by_id(total_id)

        current_text = current.text
        total_text = total.text
        
        print("Current:", current_text)
        print("Total:", total_text)
        
        return int(total.text) - int(current.text)

    def __refresh(self, basket_btn, other_btn):
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
