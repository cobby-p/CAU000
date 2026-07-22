# Setup/compile_ui.py
import ast
import io
import json
import os
import shutil
import subprocess
import sys
import tokenize
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
UI_TARGETS = (
    (
        PROJECT_DIR / "Resource" / "main_windows.ui",
        PROJECT_DIR / "Resource" / "main_windows_ui.py",
    ),
    (
        PROJECT_DIR / "Resource" / "main_macos.ui",
        PROJECT_DIR / "Resource" / "main_macos_ui.py",
    ),
)


def _get_uic_command():
    """현재 Python 환경의 pyside6-uic 실행 파일 경로 반환"""

    executable_name = "pyside6-uic.exe" if os.name == "nt" else "pyside6-uic"
    environment_uic = Path(sys.executable).with_name(executable_name)
    if environment_uic.is_file():
        return str(environment_uic)

    path_uic = shutil.which("pyside6-uic")
    if path_uic:
        return path_uic

    raise RuntimeError(
        "pyside6-uic를 찾을 수 없습니다. requirements.txt의 의존성을 먼저 설치하세요."
    )


def _needs_compile(ui_path, output_path):
    """생성 파일이 없거나 원본 UI가 더 최근에 변경되었는지 확인"""

    return (
        not output_path.is_file()
        or ui_path.stat().st_mtime_ns > output_path.stat().st_mtime_ns
    )


def _make_generated_strings_readable(output_path):
    """생성 코드의 유니코드 이스케이프 문자열을 읽기 쉬운 UTF-8로 변환"""

    source = output_path.read_text(encoding="utf-8")
    line_offsets = [0]
    for line in source.splitlines(keepends=True):
        line_offsets.append(line_offsets[-1] + len(line))

    replacements = []
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type != tokenize.STRING:
            continue
        if "\\u" not in token.string and "\\U" not in token.string:
            continue

        value = ast.literal_eval(token.string)
        if not isinstance(value, str):
            continue

        start = line_offsets[token.start[0] - 1] + token.start[1]
        end = line_offsets[token.end[0] - 1] + token.end[1]
        replacements.append((start, end, json.dumps(value, ensure_ascii=False)))

    for start, end, replacement in reversed(replacements):
        source = source[:start] + replacement + source[end:]

    current = output_path.read_text(encoding="utf-8")
    if source != current:
        output_path.write_text(source, encoding="utf-8", newline="")


def compile_ui():
    """변경된 플랫폼 UI만 생성하고 변환 실패 시 즉시 예외를 발생"""

    targets = [
        (ui_path, output_path)
        for ui_path, output_path in UI_TARGETS
        if _needs_compile(ui_path, output_path)
    ]
    if not targets:
        targets = []
    else:
        uic_command = _get_uic_command()
        for ui_path, output_path in targets:
            subprocess.run(
                [uic_command, str(ui_path), "-o", str(output_path)],
                check=True,
            )
            print(f"GUI 변환 완료: {ui_path.name} -> {output_path.name}")

    for _, output_path in UI_TARGETS:
        if output_path.is_file():
            _make_generated_strings_readable(output_path)


if __name__ == "__main__":
    compile_ui()
