import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('radar', Path(__file__).resolve().parents[1] / 'scripts/check_radar.py')
radar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(radar)


class RadarTest(unittest.TestCase):
    item = dict(id='watch-1', institution='Test institution', url='https://example.org/cursos')

    def fetch(self, suffix=''):
        return lambda _: (('<html><script>ignore-me</script><p>Convocatoria gratuita ' + 'aprendizaje ' * 20 + suffix + '</p></html>').encode(), 'text/html')

    def test_first_success_and_change(self):
        baseline = radar.signal(self.item, {}, self.fetch())
        self.assertEqual(baseline['state'], 'baseline')
        self.assertEqual(radar.signal(self.item, baseline, self.fetch())['state'], 'unchanged')
        self.assertEqual(radar.signal(self.item, baseline, self.fetch('nuevo plazo'))['state'], 'changed')

    def test_outage_preserves_fingerprint(self):
        def failed(_):
            raise TimeoutError('fixture timeout')
        result = radar.signal(self.item, {'fingerprint': 'previous'}, failed)
        self.assertEqual(result['state'], 'access_failure')
        self.assertEqual(result['fingerprint'], 'previous')

    def test_challenge_is_not_availability(self):
        result = radar.signal(self.item, {}, lambda _: (b'verify you are human', 'text/html'))
        self.assertEqual(result['state'], 'access_failure')
        self.assertNotIn('registration', result)

    def test_reject_unsafe_url(self):
        self.assertEqual(radar.signal(dict(self.item, url='http://example.org'), {}, self.fetch())['state'], 'access_failure')


if __name__ == '__main__':
    unittest.main()
