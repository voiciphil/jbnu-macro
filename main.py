from macro import Macro

stu_no = input('stu_no: ')
pw = input('pw: ')
grade = int(input('grade: '))
index = int(input('index: '))

flag = True
while flag:
    macro = Macro(stu_no, pw, grade, index)
    try:
        flag = macro.run()
    except:
        macro.driver.close()
        flag = True
