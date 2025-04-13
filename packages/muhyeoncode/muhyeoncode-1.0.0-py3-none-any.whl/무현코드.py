import sys
import ast

def 해석해라인(line):
    line = line.strip()
    try:
        if line.startswith("부엉이바위 "):
            content = line.split("부엉이바위 ", 1)[1].strip()
            if content.startswith('"') and content.endswith('"') and "{" in content and "}" in content:
                try:
                    inner = content[1:-1]
                    evaluated = eval("f" + repr(inner), globals())
                    print(evaluated)
                except NameError as e:
                    print(f"💥 [무현쉘오류] 선언되지 않은 변수 사용됨: {e}")
                except Exception as e:
                    print(f"💥 [무현쉘오류] {type(e).__name__}: {e}")
            else:
                try:
                    exec(f'print({content})', globals())
                except Exception as e:
                    print(f"💥 [무현쉘오류] {type(e).__name__}: {e}")
        elif line.startswith("이기야 "):
            content = line.split("이기야 ")[1]
            exec(f'print("🔥 " + {content})', globals())
        elif line.startswith("운지 "):
            try:
                parts = line[3:].strip().split(" ", 1)
                if len(parts) != 2:
                    print("💥 [무현쉘오류] '운지 변수 값' 형식으로 입력해주세요.")
                    return
                var, val = parts
                var = var.strip()
                val = val.strip()

                # 따옴표 오류 검사
                if (val.startswith('"') and not val.endswith('"')) or \
                   (val.startswith("'") and not val.endswith("'")):
                    print("💥 [무현쉘오류] 문자열 따옴표가 닫히지 않았습니다. 양쪽을 맞춰주세요.")
                    return

                if val.startswith('"') and val.endswith('"'):
                    assignment = f"{var} = {repr(val[1:-1])}"
                elif val.startswith("'") and val.endswith("'"):
                    assignment = f"{var} = {repr(val[1:-1])}"
                else:
                    assignment = f"{var} = {val}"

                exec(assignment, globals())
                print(f"✅ 변수 '{var}' 선언됨 → {repr(globals().get(var))}")
            except Exception as e:
                print(f"💥 [무현쉘오류] {type(e).__name__}: {e}")
        elif line.startswith("무현정수 "):
            expr = line.split("무현정수 ")[1].strip()
            if "=" in expr:
                var, val = expr.split("=", 1)
                exec(f'{var.strip()} = int({val.strip()})', globals())
        elif line.startswith("무현산술 "):
            expression = line.split("무현산술 ")[1].strip()
            if "=" in expression:
                exec(expression, globals())
            else:
                exec(expression, globals())
        elif line.startswith("무현출력 "):
            expr = line.split("무현출력 ", 1)[1]
            if expr.startswith('"') and expr.endswith('"') and "{" in expr and "}" in expr:
                try:
                    print(eval("f" + repr(expr[1:-1]), globals()))
                except Exception:
                    print(expr)
            else:
                exec(f'print({expr})', globals())
        elif line.strip() == "중력이 아니면":
            print("# else 진입")
            print("else:")
        elif line.strip() == "노빠꾸":
            print("# 무한 루프 진입")
            print("while True:")
        elif line.startswith("듣보잡 "):
            var = line.split("듣보잡 ", 1)[1].strip()
            exec(f"{var} = input('👂 {var}: ')", globals())
        elif line.startswith("무현인증 "):
            var = line.split("무현인증 ", 1)[1].strip()
            try:
                print(repr(eval(var, globals())))
            except Exception as e:
                print(f"💥 [무현쉘오류] {type(e).__name__}: {e}")
        elif line.startswith("노무 "):
            func_decl = line.split("노무 ")[1].strip()
            if "(" in func_decl and not func_decl.endswith(")"):
                func_decl += ")"
            if "(" not in func_decl:
                func_decl += "()"
            print(f"def {func_decl}:")
        elif line.strip() == "노숙자":
            print("return")
        elif line.startswith("무현돌려 "):
            value = line.split("무현돌려 ", 1)[1].strip()
            print(f"return {value}")
        elif line.startswith("소환해 "):
            call_expr = line.split("소환해 ", 1)[1].strip()
            print(f"{call_expr}")
        elif line.startswith("무현클래스 "):
            classname = line.split("무현클래스 ", 1)[1].strip()
            print(f"class {classname}:")
        elif line.startswith("무현속성 "):
            expr = line.split("무현속성 ", 1)[1].strip()
            print(expr)
        elif line.startswith("무현비동기 "):
            fname = line.split("무현비동기 ", 1)[1].strip()
            print(f"async def {fname}:")
        elif line.startswith("무현기다림 "):
            expr = line.split("무현기다림 ", 1)[1].strip()
            print(f"await {expr}")
        elif line.startswith("무현컨텍스트 "):
            expr = line.split("무현컨텍스트 ", 1)[1].strip()
            print(f"with {expr}:")
        elif line.startswith("무현패턴매칭 "):
            expr = line.split("무현패턴매칭 ", 1)[1].strip()
            print(f"match {expr}:")
        elif line.startswith("무현케이스 "):
            expr = line.split("무현케이스 ", 1)[1].strip()
            print(f"case {expr}:")
        elif line.strip() == "무현탈출":
            print("break")
        elif line.strip() == "무현넘김":
            print("continue")
        elif line.startswith("무현비산출 "):
            expr = line.split("무현비산출 ", 1)[1].strip()
            print(f"yield {expr}")
        elif line.startswith("무현글로벌 "):
            var = line.split("무현글로벌 ", 1)[1].strip()
            print(f"global {var}")
        elif line.startswith("무현논로컬 "):
            var = line.split("무현논로컬 ", 1)[1].strip()
            print(f"nonlocal {var}")
        else:
            exec(f'# [해석불가] {line}', globals())
    except Exception as e:
        print(f"💥 [무현쉘오류] {type(e).__name__}: {e}")

def 해석해(filename):
    import sys
    debug = False
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    code_lines = []
    indent = 0

    for line in lines:
        line = line.strip()
        if line.startswith("부엉이바위 "):
            content = line.split("부엉이바위 ")[1]
            code_lines.append("    " * indent + f'print(eval("f" + repr({content})))')
        elif line.startswith("이기야 "):
            content = line.split("이기야 ")[1]
            code_lines.append("    " * indent + f'print("🔥 " + {content})')
        elif line.startswith("운지 "):
            parts = line[3:].strip().split(" ", 1)
            if len(parts) == 2:
                var, val = parts
                code_lines.append("    " * indent + f'{var.strip()} = {val.strip()}')
        elif line.startswith("중력 "):
            condition = line.split("중력 ")[1]
            code_lines.append("    " * indent + f'if {condition.strip()}:')
            indent += 1
        elif line.startswith("아메리카노 ") and "번" in line:
            times = line.split("아메리카노 ")[1].split("번")[0].strip()
            code_lines.append("    " * indent + f'for _ in range({times}):')
            indent += 1
        elif line.startswith("노무 "):
            func_decl = line.split("노무 ")[1].strip()
            if "(" in func_decl and not func_decl.endswith(")"):
                func_decl += ")"
            if "(" not in func_decl:
                func_decl += "()"
            code_lines.append("    " * indent + f'def {func_decl}:')
            indent += 1
        elif line.strip() == "노숙자":
            code_lines.append("    " * indent + "return")
        elif line.strip() == "운지":
            indent = max(0, indent - 1)
        elif line.startswith("망각해 "):
            var = line.split("망각해 ")[1].strip()
            code_lines.append("    " * indent + f'del {var}')
        elif line.strip() == "노코멘트":
            code_lines.append("    " * indent + "pass")
        elif line.startswith("소환해 "):
            call_expr = line.split("소환해 ")[1].strip()
            code_lines.append("    " * indent + f'{call_expr}')
        elif line.startswith("고무통 "):
            fname = line.split("고무통 ")[1].strip().strip('"')
            해석해(fname)
        elif line.strip() == "노무현 사 시리즈":
            code_lines.append("    " * indent + 'print("노무현은 살아있다")')
        elif line.startswith("무현산술 "):
            expression = line.split("무현산술 ")[1].strip()
            code_lines.append("    " * indent + expression)
        elif line.startswith("듣보잡 "):
            var = line.split("듣보잡 ")[1].strip()
            code_lines.append("    " * indent + f'{var} = input()')
        elif line.startswith("무현인증 "):
            var = line.split("무현인증 ")[1].strip()
            code_lines.append("    " * indent + f'print(repr({var}))')
        elif line.strip() == "노무현 컴파일 끝":
            code_lines.append("    " * indent + 'exit()')
        elif line.startswith("노빠꾸 "):
            condition = line.split("노빠꾸 ")[1]
            code_lines.append("    " * indent + f'while {condition.strip()}:')
            indent += 1
        elif line.startswith("무현리스트 "):
            expression = line.split("무현리스트 ")[1].strip()
            code_lines.append("    " * indent + expression)
        elif line.startswith("무현딕트 "):
            expression = line.split("무현딕트 ")[1].strip()
            code_lines.append("    " * indent + expression)
        elif line.startswith("무현출력 "):
            expr = line.split("무현출력 ", 1)[1]
            if expr.startswith('"') and expr.endswith('"') and "{" in expr and "}" in expr:
                code_lines.append("    " * indent + f'print(f{expr})')
            else:
                code_lines.append("    " * indent + f'print({expr})')
        elif line.strip() == "무현예외":
            code_lines.append("    " * indent + "try:")
            indent += 1
        elif line.strip() == "무현실패:":
            indent = max(0, indent - 1)
            code_lines.append("    " * indent + "except:")
            indent += 1
        elif line.startswith("무현클래스 "):
            classname = line.split("무현클래스 ")[1].strip()
            code_lines.append("    " * indent + f'class {classname}:')
            indent += 1
        elif line.startswith("무현속성 "):
            expr = line.split("무현속성 ")[1].strip()
            code_lines.append("    " * indent + expr)
        elif line.startswith("무현비동기 "):
            fname = line.split("무현비동기 ")[1].strip()
            code_lines.append("    " * indent + f'async def {fname}:')
            indent += 1
        elif line.startswith("무현기다림 "):
            expr = line.split("무현기다림 ")[1].strip()
            code_lines.append("    " * indent + f'await {expr}')
        elif line.startswith("무현컨텍스트 "):
            expr = line.split("무현컨텍스트 ")[1].strip()
            code_lines.append("    " * indent + f'with {expr}:')
            indent += 1
        elif line.startswith("무현패턴매칭 "):
            expr = line.split("무현패턴매칭 ")[1].strip()
            code_lines.append("    " * indent + f'match {expr}:')
            indent += 1
        elif line.startswith("무현케이스 "):
            expr = line.split("무현케이스 ")[1].strip()
            code_lines.append("    " * indent + f'case {expr}:')
            indent += 1
        elif line.strip() == "무현탈출":
            code_lines.append("    " * indent + 'break')
        elif line.strip() == "무현넘김":
            code_lines.append("    " * indent + 'continue')
        elif line.startswith("무현비산출 "):
            expr = line.split("무현비산출 ")[1].strip()
            code_lines.append("    " * indent + f'yield {expr}')
        elif line.startswith("무현글로벌 "):
            var = line.split("무현글로벌 ")[1].strip()
            code_lines.append("    " * indent + f'global {var}')
        elif line.startswith("무현논로컬 "):
            var = line.split("무현논로컬 ")[1].strip()
            code_lines.append("    " * indent + f'nonlocal {var}')
        elif line.strip() == "무현주입":
            code_lines.append("    " * indent + 'if __name__ == "__main__":')
            indent += 1
        elif line.startswith("무현정수 "):
            expr = line.split("무현정수 ")[1].strip()
            if "=" in expr:
                var, val = expr.split("=", 1)
                code_lines.append("    " * indent + f'{var.strip()} = int({val.strip()})')
        elif line.startswith("무현실수 "):
            expr = line.split("무현실수 ")[1].strip()
            if "=" in expr:
                var, val = expr.split("=", 1)
                code_lines.append("    " * indent + f'{var.strip()} = float({val.strip()})')
        elif line.startswith("무현문자열 "):
            expr = line.split("무현문자열 ")[1].strip()
            if "=" in expr:
                var, val = expr.split("=", 1)
                code_lines.append("    " * indent + f'{var.strip()} = str({val.strip()})')
        elif line.startswith("무현불리언 "):
            expr = line.split("무현불리언 ")[1].strip()
            if "=" in expr:
                var, val = expr.split("=", 1)
                code_lines.append("    " * indent + f'{var.strip()} = bool({val.strip()})')
        elif line.startswith("무현타입 "):
            var = line.split("무현타입 ")[1].strip()
            code_lines.append("    " * indent + f'print(type({var}))')
        elif line.startswith("무현주석 #"):
            code_lines.append("    " * indent + line.replace("무현주석", "").strip())
        elif line.startswith("무현데이터클래스 "):
            classname = line.split("무현데이터클래스 ")[1].strip()
            code_lines.append("    " * indent + '@dataclass')
            code_lines.append("    " * indent + f'class {classname}:')
            indent += 1
        elif line.strip() == "무현탈출":
            code_lines.append("    " * indent + 'break')
        elif line.strip() == "무현넘김":
            code_lines.append("    " * indent + 'continue')
        else:
            code_lines.append("    " * indent + f'# [해석불가] {line}')

    code = "\n".join(code_lines)
    if debug:
        print("🔍 [DEBUG] 변환된 코드:\n" + code + "\n" + "🔚" * 20)
    try:
        exec(code, globals())
    except Exception as e:
        print(f"💥 [무현런타임오류] {type(e).__name__}: {e}")

def main():
    if len(sys.argv) > 1:
        target = sys.argv[1]
        if target == "--help":
            무현도움말()
        elif target == "--repl" or target == "무현쉘모드":
            print("💻 무현쉘모드 진입! 한 줄씩 무현코드를 입력하세요. (종료: exit 또는 Ctrl+D)")
            try:
                while True:
                    line = input("🐉 >>> ").strip()
                    if line.lower() in ["exit", "quit"]:
                        print("👋 무현쉘모드 종료!")
                        break
                    해석해라인(line)
            except (EOFError, KeyboardInterrupt):
                print("\n👋 무현쉘모드 종료!")
        else:
            해석해(target)
    else:
        해석해("muhyun.mh")

if __name__ == "__main__":
    main()

print("🐉 MUHYEON CODE v1.0 - 부엉이바위 컴파일러 시작됨")

def 무현도움말():
    print("🧾 사용 가능한 무현 명령어 예시:")
    print("- 운지 변수는 값")
    print("- 부엉이바위 \"내용\"")
    print("- 중력 조건")
    print("- 무현정수 / 무현출력 / 노무 / 노숙자 등 전체 문법은 README.md 참고")
