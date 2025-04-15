from rapidfuzz import fuzz
from typing import Optional
from municipality_lookup.models import Municipality

class MunicipalitySearcher:
    def __init__(self, municipalities: list[Municipality]):
        self._municipalities = municipalities
        self._index = {m.name.lower(): m for m in municipalities}

    def find_exact(self, name: str) -> Optional[Municipality]:
        return self._index.get(name.strip().lower())

    def find_similar(self, name: str, min_score: float = 0.8) -> Municipality:
        name = name.strip().lower()
        best_match = None
        best_score = 0

        for m in self._municipalities:
            score = (fuzz.ratio(name, m.name.lower()) + fuzz.partial_ratio(name, m.name.lower())) / 2 / 100
            if score > best_score and score >= min_score:
                best_match = m
                best_score = score

        if best_match:
            return best_match
        else:
            return Municipality(name='', province='', land_registry='', national_code='', cadastral_code='')
