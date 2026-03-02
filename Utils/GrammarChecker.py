import requests
from typing import Dict, List


class GrammarChecker:
    """Grammar checker using free LanguageTool API."""

    API_URL = "https://api.languagetool.org/v2/check"

    def __init__(self, language: str = "en-US"):
        self.language = language
        self.session = requests.Session()

    def check_grammar(self, text: str) -> Dict:
        """Check grammar and return detailed results."""
        try:
            data = {'text': text, 'language': self.language}
            response = self.session.post(self.API_URL, data=data, timeout=10)
            response.raise_for_status()
            result = response.json()

            matches = result.get('matches', [])
            error_count = len(matches)
            score = max(0, 100 - (error_count * 10))
            corrected_text = self._apply_corrections(text, matches)
            errors = self._parse_errors(matches)

            return {
                'is_correct': error_count == 0,
                'error_count': error_count,
                'errors': errors,
                'corrected_text': corrected_text,
                'score': score
            }
        except Exception as e:
            return {
                'is_correct': None,
                'error_count': 0,
                'errors': [],
                'corrected_text': text,
                'score': 0,
                'error': str(e)
            }

    def _parse_errors(self, matches: List[Dict]) -> List[Dict]:
        errors = []
        for match in matches:
            errors.append({
                'message': match.get('message', ''),
                'replacements': [r['value'] for r in match.get('replacements', [])[:3]],
                'type': match.get('rule', {}).get('issueType', 'unknown')
            })
        return errors

    def _apply_corrections(self, text: str, matches: List[Dict]) -> str:
        if not matches:
            return text
        sorted_matches = sorted(matches, key=lambda x: x['offset'], reverse=True)
        corrected = text
        for match in sorted_matches:
            offset = match['offset']
            length = match['length']
            replacements = match.get('replacements', [])
            if replacements:
                corrected = corrected[:offset] + replacements[0]['value'] + corrected[offset + length:]
        return corrected
