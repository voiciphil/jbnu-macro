import argparse
from macro import Macro


# 유효성 검증을 하면서 파싱
def parse_input(parser):
    args = parser.parse_args()
    stu_no = args.n
    pw = args.p
    index = args.i
    grade = args.g
    major = args.m

    # 전공 선택했지만 학년이 없으면 에러
    if major == '' and not grade:
        return None

    major = True if major == '' else False

    return stu_no, pw, index, grade, major


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=str, help='학번', required=True)
    parser.add_argument('-p', type=str, help='비밀번호', required=True)
    parser.add_argument('-i', type=int, help='과목 인덱스', required=True)
    parser.add_argument('-m', type=str, help='전공 모드', nargs='?', const='')
    parser.add_argument('-g', type=int, help='학년')

    params = parse_input(parser)
    if not params:
        print("Params Error")
    else:
        stu_no, pw, index, grade, major = params

        flag = True
        while flag:
            macro = Macro(stu_no, pw, grade, index, major=major)
            try:
                flag = macro.run()
            except:
                macro.close_browser()
                flag = True
