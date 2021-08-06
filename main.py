import argparse
from macro import Macro

parser = argparse.ArgumentParser()
parser.add_argument('-n', type=str, help='학번', required=True)
parser.add_argument('-p', type=str, help='비밀번호', required=True)
parser.add_argument('-i', type=int, help='과목 인덱스', required=True)
parser.add_argument('-m', type=int, help='0 -> 전공, 1 -> 장바구니', required=True)
parser.add_argument('-g', type=int, help='학년')

args = parser.parse_args()
stu_no = args.n
pw = args.p
index = args.i
grade = args.g
method = args.m

flag = True
while flag:
    macro = Macro(stu_no, pw, grade, index, method=method)
    try:
        flag = macro.run()
    except:
        macro.close_browser()
        flag = True
