import os
from time import sleep

from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException

class Macro:
    def __init__(self, stu_no, pw, grade, index):
        self.driver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'))

        self.grade = grade
        self.index = index

        self.stu_no = stu_no
        self.pw = pw


    def refresh(self, spinner1, spinner2):
        spinner1.click()
        spinner2.send_keys(Keys.DOWN)
        spinner2.send_keys(Keys.DOWN)
        spinner2.send_keys(Keys.DOWN)
        spinner2.send_keys(Keys.RETURN)
        spinner1.click()
        spinner2.send_keys(Keys.UP)
        spinner2.send_keys(Keys.UP)
        spinner2.send_keys(Keys.UP)
        spinner2.send_keys(Keys.RETURN)

    def getCode(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.find('div', {'id':'mainframe_VFrameSet_TopFrame_COM_CHECK_form_div_pattern_sta_codeTextBoxElement'})
        return divs.div.text
    
    def inputCode(self):
        code_id = 'mainframe_VFrameSet_TopFrame_COM_CHECK_form_Edit00_input'
        code_okay_id = 'mainframe_VFrameSet_TopFrame_COM_CHECK_form_btnOKTextBoxElement'
        final_okay_id = 'mainframe_VFrameSet_TopFrame_COM_ALERT_form_Static00'
        code = self.driver.find_element_by_id(code_id)
        code.click()
        code.send_keys(self.getCode())
        sleep(0.5)
        okay = self.driver.find_element_by_id(code_okay_id)
        okay.click()
        sleep(0.5)
        self.driver.find_element_by_id(final_okay_id).click()
        sleep(0.3)

    def run(self):
        self.driver.implicitly_wait(3)
        self.driver.get('http://all.jbnu.ac.kr/jbnu/sugang/')
        self.driver.maximize_window()

        stu_no_id = 'mainframe_VFrameSet_LoginFrame_form_div_login_div_form_edt_hakbun_input'
        pw_id = 'mainframe_VFrameSet_LoginFrame_form_div_login_div_form_edt_passwd_input'
        stu_no = self.driver.find_element_by_id(stu_no_id)
        pw = self.driver.find_element_by_id(pw_id)

        login_xpath = '//*[@id="mainframe_VFrameSet_LoginFrame_form_div_login_div_form_btn_login"]/div'
        login = self.driver.find_element_by_xpath(login_xpath)

        
        stu_no.click()
        stu_no.send_keys(self.stu_no)
        pw.click()
        pw.send_keys(self.pw)
        login.click()       

        sugang_xpath = '//*[@id="mainframe_VFrameSet_TopFrame_form_div_top_mnu_topmenu_0001TextBoxElement"]/div'

        try:
            sleep(0.5)
            sugang = self.driver.find_element_by_xpath(sugang_xpath)
            sugang.click()
            sleep(0.5)
            # self.inputCode()

        except ElementNotInteractableException:
            ok_xpath = '//*[@id="mainframe_VFrameSet_LoginFrame_COM_ALERT_form_btn_closeTextBoxElement"]'
            ok = self.driver.find_element_by_xpath(ok_xpath)
            ok.click()
            login.click()
            sugang = self.driver.find_element_by_xpath(sugang_xpath)
            sugang.click()
            # self.inputCode()

        spinner1_xpath = '//*[@id="mainframe_VFrameSet_WorkFrame_form_div_work_div_search_cbo_shyr"]/div'
        spinner1 = self.driver.find_element_by_xpath(spinner1_xpath)
        spinner1.click()

        spinner2_xpath = '//*[@id="mainframe_VFrameSet_WorkFrame_form_div_work_div_search_cbo_shyr_comboedit_input"]'
        spinner2 = self.driver.find_element_by_xpath(spinner2_xpath)
        for _ in range(self.grade + 1):
            spinner2.send_keys(Keys.DOWN)
            spinner2.send_keys(Keys.RETURN)

        current_id = 'mainframe_VFrameSet_WorkFrame_form_div_work_grd_gwam_body_gridrow_' + str(self.index) + \
                     '_cell_' + str(self.index) + '_7GridCellTextSimpleContainerElement'
        total_id = 'mainframe_VFrameSet_WorkFrame_form_div_work_grd_gwam_body_gridrow_' + str(self.index) + \
                   '_cell_' + str(self.index) + '_8GridCellTextSimpleContainerElement'

        current = self.driver.find_element_by_id(current_id)
        total = self.driver.find_element_by_id(total_id)
        cnt = 0
        while total.text == current.text:
            self.refresh(spinner1, spinner2)
            sleep(0.5)
            current = self.driver.find_element_by_id(current_id)
            total = self.driver.find_element_by_id(total_id)
            cnt += 1
            if cnt == 150:
                self.driver.quit()
                return True

        if total.text != current.text:
            btn_id = 'mainframe_VFrameSet_WorkFrame_form_div_work_grd_gwam_body_gridrow_' + str(self.index) + \
                     '_cell_' + str(self.index) + '_0_controlbuttonTextBoxElement'
            btn = self.driver.find_element_by_id(btn_id)
            btn.click()
            return False
        else:
            return True
