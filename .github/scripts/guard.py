#!/usr/bin/env python3
"""Deterministic safety gate for pull requests. No AI: nothing written in a PR can talk it out of a rule.

Usage: guard.py FILES_JSON DIFF_PATCH > report.md   (exit 1 = blocked)

It never executes PR code. It only reads the file list and the diff, and blocks:
  - files outside the allowlist (workflows, tests, package.json, scripts, legal files...)
  - new text with network calls, dynamic code, new script/iframe tags, unknown URLs,
    obfuscation, invisible Unicode, or instructions aimed at an AI reviewer
  - any edit to the security header (CSP) or the pinned three.js script
"""
import json, re, sys

ALLOWED = [
    re.compile(r'^index\.html$'),
    re.compile(r'^media/[\w.-]+\.(png|jpe?g|gif|webp)$'),
    re.compile(r'^(?!\.github/)[\w./-]+\.md$'),
]
PROTECTED = {'LICENSE', 'CLA.md', 'TRADEMARKS.md', 'SECURITY.md', 'CODE_OF_CONDUCT.md',
             'CONTRIBUTING.md', 'THIRD-PARTY-NOTICES.md', 'README.md'}
URL_OK = re.compile(r'https?://(github\.com/tobeficv/founders-way|tobeficv\.github\.io/founders-way'
                    r'|cdnjs\.cloudflare\.com/ajax/libs/three\.js/r128/|fonts\.(googleapis|gstatic)\.com'
                    r'|www\.w3\.org/)')

RULES = [  # (name, regex) checked on the new text of every added or edited line
    ('network call', r'\bfetch\s*\(|XMLHttpRequest|WebSocket|EventSource|sendBeacon|RTCPeerConnection|importScripts'
                     r'|\bimport\s*\(|new\s+(Shared)?Worker|serviceWorker|\.src\s*=|\.href\s*=|new\s+Image\s*\('),
    ('dynamic code', r'\beval\s*\(|\bFunction\s*\(|set(Timeout|Interval)\s*\(\s*[\'"`]|document\.write'
                     r'|createContextualFragment|outerHTML\s*='),
    ('new script, frame or embed', r'<\s*(script|iframe|object|embed|frame|link|meta|base|form)\b|srcdoc|javascript:'),
    ('navigation or popup', r'location\s*\.\s*(href|replace|assign)|location\s*=|window\.open|top\.location'
                            r'|window\.parent|\bparent\.(location|document)|postMessage'),
    ('hidden call by name', r'\b(window|globalThis|self|document|navigator)\s*\[|\[\s*[\'"`]\w+[\'"`]\s*\]\s*\('
                            r'|createElement\s*\(\s*[^\'"`\s]'
                            r'|createElement\s*\(\s*[\'"`](script|iframe|img|link|object|embed|a|form)\b'
                            r'|Reflect\.|constructor\s*\('),
    ('cookies or credentials', r'document\.cookie|credentials|password|indexedDB'),
    ('obfuscation', r'\batob\s*\(|\bbtoa\s*\(|fromCharCode|(\\x[0-9a-fA-F]{2}){4}|(\\u[0-9a-fA-F]{4}){4}'
                    r'|[A-Za-z0-9+/]{160,}={0,2}|unescape\s*\('),
    ('instructions aimed at an AI reviewer', r'(?i)ignore (all |any |the )?(previous|prior|above)|system prompt'
                     r'|you are (an? |the )?(ai|assistant|reviewer|claude)|\b(claude|anthropic|chatgpt|openai|llm)\b'
                     r'|auto-?(approve|merge)|approve this|do not (read|review|flag)'),
]
RULES = [(n, re.compile(p)) for n, p in RULES]
# Zero-width joiner is fine right after an emoji; every other invisible or bidi character is not.
INVISIBLE = re.compile('(?<![\\U0001F000-\\U0001FAFF\\u2600-\\u27BF])\\u200d'
                       '|[\\u200b\\u200c\\u200e\\u200f\\u202a-\\u202e\\u2060-\\u2064\\u2066-\\u2069'
                       '\\ufeff\\u00ad\\u180e\\U000E0000-\\U000E007F]')
LOCKED = re.compile(r'Content-Security-Policy|integrity=|three\.min\.js|@@I18N-(START|END)')
URL = re.compile(r'https?://[^\s"\'<>)`]+')


def main():
    files = json.load(open(sys.argv[1], encoding='utf-8'))
    diff = open(sys.argv[2], encoding='utf-8', errors='replace').read()
    problems = []
    for f in files:
        p = f['path']
        if p in PROTECTED or not any(r.match(p) for r in ALLOWED):
            problems.append(f'`{p}`: this file can only be changed by the maintainer')

    # Pair each hunk's removed and added lines so only the NEW part of an edited line is judged.
    # (index.html keeps big dictionaries on one line; the text already there is trusted.)
    state = {'path': None, 'line': 0}
    minus, plus = [], []

    def judge(ln, text, lo, hi):
        if hi <= lo:
            return
        where = f"`{state['path']}` line {ln}"
        hit = lambda m: m.start() < hi and m.end() > lo
        if any(hit(m) for m in INVISIBLE.finditer(text)):
            problems.append(f'{where}: invisible or direction-changing Unicode characters')
        if any(hit(m) for m in LOCKED.finditer(text)):
            problems.append(f'{where}: edits a locked security line')
        for name, rx in RULES:
            if any(hit(m) for m in rx.finditer(text)):
                problems.append(f'{where}: {name}')
        if any(hit(m) and not URL_OK.match(m.group()) for m in URL.finditer(text)):
            problems.append(f'{where}: link to a site outside the allowlist')

    def flush():
        for i, (ln, text) in enumerate(plus):
            old = minus[i] if i < len(minus) else ''
            n = min(len(old), len(text))
            a = 0
            while a < n and old[a] == text[a]:
                a += 1
            b = 0
            while b < n - a and old[-1 - b] == text[-1 - b]:
                b += 1
            judge(ln, text, a, len(text) - b)
        kept = {t for _, t in plus}
        if any(LOCKED.search(t) and t not in kept for t in minus):
            problems.append(f"`{state['path']}`: removes or edits a locked security line")
        minus.clear()
        plus.clear()

    for raw in diff.split('\n'):
        if raw.startswith(('+++ ', '--- ', 'diff --git')):
            flush()
            if raw.startswith('+++ '):
                state['path'] = raw[6:] if raw.startswith('+++ b/') else raw[4:]
            continue
        m = re.match(r'@@ -\d+(?:,\d+)? \+(\d+)', raw)
        if m:
            flush()
            state['line'] = int(m.group(1))
        elif raw.startswith('-'):
            if plus:
                flush()
            minus.append(raw[1:])
        elif raw.startswith('+'):
            plus.append((state['line'], raw[1:]))
            state['line'] += 1
        else:
            flush()
            state['line'] += 1
    flush()

    seen = list(dict.fromkeys(problems))
    if seen:
        print('**Safety check: blocked.** These changes need the maintainer, so this PR cannot be merged as is:\n')
        print('\n'.join(f'- {p}' for p in seen[:40]))
        if len(seen) > 40:
            print(f'- and {len(seen) - 40} more')
        print('\nIf this is a false positive, explain it in a comment and the maintainer will look at it. '
              'See CONTRIBUTING.md for what pull requests can change.')
        sys.exit(1)
    print('Safety check passed.')


if __name__ == '__main__':
    main()
