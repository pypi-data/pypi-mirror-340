import argparse
import sys
import os

def compare_lines(answer_lines, input_lines, answer_name='answer.txt', input_name='입력'):
    max_lines = max(len(answer_lines), len(input_lines))
    differences = []

    for i in range(max_lines):
        line1 = answer_lines[i].rstrip('\n') if i < len(answer_lines) else f"[{answer_name}에 없음]"
        line2 = input_lines[i].rstrip('\n') if i < len(input_lines) else f"[{input_name}에 없음]"

        if line1 != line2:
            differences.append((i + 1, line1, line2))

    if not differences:
        print(f"{answer_name}과 {input_name}의 내용이 정확히 일치합니다.")
    else:
        print(f"{len(differences)}개의 줄에서 차이가 발생했습니다:\n")
        for line_num, line1, line2 in differences:
            print(f"줄 {line_num}:\n  {answer_name}: {line1}\n  {input_name}: {line2}\n")


def main():
    parser = argparse.ArgumentParser(
        description='''두 텍스트 파일의 내용 일치 여부를 비교합니다.
    사용 예:
        ./parser test.c | pacheck       # 파이프 입력과 answer.txt 비교
        pacheck output.txt              # answer.txt와 output.txt 비교
        pacheck file1.txt file2.txt     # 두 파일 직접 비교
        '''
    )
    parser.add_argument('files', nargs='*', help='비교할 파일 경로 (0개~2개)')

    args = parser.parse_args()

    # 파이프 입력 (stdin)
    if not sys.stdin.isatty():
        input_lines = sys.stdin.readlines()
        if not os.path.exists('answer.txt'):
            print("[ERROR] answer.txt 파일이 존재하지 않습니다.")
            return
        with open('answer.txt', 'r', encoding='utf-8') as f:
            answer_lines = f.readlines()
        compare_lines(answer_lines, input_lines, 'answer.txt', '표준 입력')
        return

    # 인자 1개 → answer.txt와 비교
    if len(args.files) == 1:
        if not os.path.exists('answer.txt'):
            print("[ERROR] answer.txt 파일이 존재하지 않습니다.")
            return
        with open('answer.txt', 'r', encoding='utf-8') as f1, open(args.files[0], 'r', encoding='utf-8') as f2:
            compare_lines(f1.readlines(), f2.readlines(), 'answer.txt', args.files[0])

    # 인자 2개 → 두 파일 비교
    elif len(args.files) == 2:
        with open(args.files[0], 'r', encoding='utf-8') as f1, open(args.files[1], 'r', encoding='utf-8') as f2:
            compare_lines(f1.readlines(), f2.readlines(), args.files[0], args.files[1])

    else:
        print("[ERROR] 인자는 1개-2개 입력하거나, 파이프로 입력을 넘겨야 합니다.")
        print("사용 예:")
        print("  pacheck output.txt              # answer.txt와 output.txt 비교")
        print("  pacheck file1.txt file2.txt     # 두 파일 직접 비교")
        print("  ./parser test.c | pacheck       # 파이프 입력과 answer.txt 비교")

if __name__ == '__main__':
    main()
