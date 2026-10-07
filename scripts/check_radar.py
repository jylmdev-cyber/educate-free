"""Public source change signals. Never updates course availability or prices."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style', 'noscript', 'svg'}:
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag in {'script', 'style', 'noscript', 'svg'} and self.hidden:
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def signal(item, previous, fetcher=None):
    now = datetime.now(timezone.utc).isoformat()
    output = dict(id=item['id'], institution=item['institution'], url=item['url'], checked_at=now)
    parsed = urlsplit(item['url'])
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        return dict(output, state='access_failure', error='URL must be public HTTPS', fingerprint=None)
    try:
        if fetcher:
            raw, content_type = fetcher(item['url'])
        else:
            request = Request(item['url'], headers={'User-Agent': 'EducaLibre-public-radar/1.0', 'Accept': 'text/html'})
            with urlopen(request, timeout=12) as response:
                if urlsplit(response.url).scheme != 'https':
                    raise ValueError('Non-HTTPS redirect')
                raw = response.read(2_000_001)
                content_type = response.headers.get('Content-Type', '')
        if len(raw) > 2_000_000 or 'html' not in content_type.lower():
            raise ValueError('Unsupported or oversized response')
        parser = VisibleText()
        parser.feed(raw.decode('utf-8', errors='replace'))
        text = re.sub(r'\s+', ' ', ' '.join(parser.parts)).strip()
        if len(text) < 100 or any(x in text.lower() for x in ['verify you are human', 'enable javascript and cookies', 'checking your browser']):
            raise ValueError('Insufficient visible text or access challenge')
        fingerprint = hashlib.sha256(text.encode('utf-8')).hexdigest()
        last = previous.get('fingerprint')
        state = 'baseline' if not last else 'unchanged' if last == fingerprint else 'changed'
        snippets = [text[max(0, m.start() - 70):m.end() + 140] for m in re.finditer(r'convocatoria|inscripci[oó]n|matr[ií]cula|gratuit|capacitaci[oó]n', text, re.I)][:3]
        return dict(output, state=state, fingerprint=fingerprint, snippets=snippets, error=None)
    except Exception as error:
        # Keep last successful fingerprint so an outage cannot erase the baseline.
        return dict(output, state='access_failure', fingerprint=previous.get('fingerprint'), snippets=[], error=f'{type(error).__name__}: {str(error)[:180]}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'public/radar-checks.json')
    args = parser.parse_args()
    catalog = json.loads((ROOT / 'investigacion/catalogo.json').read_text(encoding='utf-8'))
    previous = json.loads(args.output.read_text(encoding='utf-8')) if args.output.exists() else {'checks': []}
    old = {i['id']: i for i in previous['checks']}
    items = [dict(i, id=f'watch-{n + 1}') for n, i in enumerate(catalog['watchlist'])]
    with ThreadPoolExecutor(max_workers=4) as pool:
        checks = list(pool.map(lambda item: signal(item, old.get(item['id'], {})), items))
    result = dict(version=1, checked_at=datetime.now(timezone.utc).isoformat(), checks=checks)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'output': str(args.output), 'checked': len(checks), 'states': {state: sum(c['state'] == state for c in checks) for state in ['baseline', 'changed', 'unchanged', 'access_failure']}}))


if __name__ == '__main__':
    main()
