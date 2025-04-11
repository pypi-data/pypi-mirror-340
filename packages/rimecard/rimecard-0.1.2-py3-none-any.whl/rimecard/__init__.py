#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import chardet
from pypinyin import lazy_pinyin


def detect_file_encoding(file_path: Path) -> tuple[str | None, float]:
    encoding = None
    confidence = 0.0
    try:
        with file_path.open('rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            confidence = result['confidence']
            print(f'Detect encoding: {encoding} (confidence: {confidence})')
    except Exception:
        print('Detect encoding failed.')
    return encoding, confidence


def vcf2dict(args: argparse.Namespace) -> None:
    input: Path | None = getattr(args, 'input', None)
    output: Path | None = getattr(args, 'output', None)
    output_encoding = getattr(args, 'encoding', 'utf-8')
    words_limit = getattr(args, 'limit', 0)
    if input is None:
        print('Input file not specified.')
        sys.exit(1)
    if words_limit > 0:
        print(f'Words limit: {words_limit}')

    encoding, confidence = detect_file_encoding(input)
    if confidence < 0.8:
        print('Encoding confidence is low, use utf-8 as default.')
        encoding = 'utf-8'

    output_lines = ''
    with input.open('r', encoding=encoding) as ifp:
        output_lines += f'# coding: {output_encoding}\n---\n'

        for line in ifp:
            if line.startswith('FN:'):
                content = line[3:].strip()
                words = content.split(' ')
                name = ''.join(words)
                pinyin = ' '.join(lazy_pinyin(name))
                if len(name) > words_limit:
                    continue
                output_lines += f'{name}\t{pinyin}\t1\n'

    if output is None:
        print()
        for line in output_lines:
            print(line, end='')
    else:
        output_file = output.resolve()
        if output_file.is_dir():
            print('Can not write to directory.')
            sys.exit(1)
        if not output_file.parent.exists():
            output_file.parent.mkdir(parents=True)
        with output_file.open('w', encoding='utf-8') as wfp:
            wfp.writelines(output_lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-i', '--input', type=Path, required=True, help='file to read')
    parser.add_argument('-o', '--output', type=Path, help='file to write')
    parser.add_argument(
        '-e', '--encoding', type=str, default='utf-8', help='output file encoding'
    )
    parser.add_argument(
        '-l', '--limit', type=int, default=3, help='limit the number of words'
    )
    parser.set_defaults(func=vcf2dict)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
