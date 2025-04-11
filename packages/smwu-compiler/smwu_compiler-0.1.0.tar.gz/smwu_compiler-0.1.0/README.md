# smwu-compiler
컴파일러 과목 programming assignment 자가 채점 도구


## Quick Start Guide
1. 패키지 설치
  `pip install smwu-compiler`
  - MacOS의 경우 `pip3` 사용
2. `answer.txt` 작성: 과제의 출력 예시 붙여넣기
3. CLI 명령어 사용해 비교


## Description
두 **텍스트** 파일의 **내용 일치 여부**를 비교하는 CLI 도구입니다.
### 사용 예:
    - `./parser test.c | pacheck`      # 파이프 입력과 answer.txt 비교
    - `pacheck output.txt   `           # answer.txt와 output.txt 비교
    - `pacheck file1.txt file2.txt`     # 두 파일 직접 비교

### 출력 예시
- **일치하는 경우** 
`정답 파일과 입력 파일이 정확히 일치합니다.`
- **차이가 있는 경우**
```
2개의 줄에서 차이가 발생했습니다:

줄 3:
  answer.txt: Hello, world!
  입력 파일: Hello, Word!

줄 8:
  answer.txt: This is a test.
  입력 파일: This is test.
```

## Upcoming Next
- [ ] parse tree 시각화


------
### Author
[Yoon SeoJin](https://github.com/Y00NSJ/compiler-pa-checker)