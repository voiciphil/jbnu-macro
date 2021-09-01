import argparse
from basket_macro import BasketMacro
from major_macro import MajorMacro


def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=str, help='학번', required=True)
    parser.add_argument('-p', type=str, help='비밀번호', required=True)
    parser.add_argument('-i', type=int, help='과목 인덱스', required=True)
    parser.add_argument('-m', type=str, help='전공 모드', nargs='?', const='')
    parser.add_argument('-g', type=int, help='학년')
    return parser

def is_not_valid_args(args):
    if not args.m and not args.g:
        return False
    if not args.m or not args.g:
        return True
    return False

def create_macro(args):
    stu_no = args.n
    pw = args.p
    index = args.i
    grade = args.g
    major = True if args.m == '' else False

    if major:
        return MajorMacro(stu_no, pw, index, grade)
    return BasketMacro(stu_no, pw, index)

if __name__ == '__main__':
    parser = get_argument_parser()
    args = parser.parse_args()

    if is_not_valid_args(args):
        parser.print_help()
    else:
        flag = True
        while flag:
            macro = create_macro(args)
            try:
                flag = macro.run()
            except:
                macro.close_browser()
                flag = True
