import argparse
from basket_macro import BasketMacro
from major_macro import MajorMacro


def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=str, help='학번', required=True)
    parser.add_argument('-p', type=str, help='비밀번호', required=True)
    parser.add_argument('-i', type=int, help='과목 인덱스', required=True)
    return parser

def create_macro(args):
    stu_no = args.n
    pw = args.p
    index = args.i
    grade = args.g
    return BasketMacro(stu_no, pw, index)

if __name__ == '__main__':
    parser = get_argument_parser()
    args = parser.parse_args()
    flag = True
    while flag:
        macro = create_macro(args)
        try:
            flag = macro.run()
        except:
            macro.close_browser()
            flag = True
