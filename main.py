import argparse
from macro import Macro

parser = argparse.ArgumentParser()
parser.add_argument('-n', type=str, help='학번')
parser.add_argument('-p', type=str, help='비밀번호')
parser.add_argument('-g', type=int, help='학년')
parser.add_argument('-i', type=int, help='과목 인덱스')

args = parser.parse_args()
stu_no = args.n
pw = args.p
grade = args.g
index = args.i

flag = True
while flag:
    macro = Macro(stu_no, pw, grade, index)
    try:
        flag = macro.run()
    except:
        macro.close_browser()
        flag = True
