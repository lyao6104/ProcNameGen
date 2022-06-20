import json
import string
from functools import cached_property
from random import randint
from typing import List, Optional, Tuple

from numpy.random import choice

from .util import normalize_sum


class Name(object):
    def __init__(self, segments: List[str]) -> None:
        self.segments = segments

    def to_json(self):
        return json.dumps({"name": str(self), "segments": self.segments})

    def __str__(self) -> str:
        return "".join(self.segments).capitalize()


class SegmentType(object):
    def __init__(
        self, name: str, probability: float, segments: List[Tuple[str, float]]
    ) -> None:
        self.name = name
        self.probability = probability
        self.segments = segments

    def to_json(self):
        return json.dumps(
            {
                "name": self.name,
                "probability": self.probability,
                "segments": self.segments,
            }
        )

    @cached_property
    def values(self):
        return list(map(lambda s: s[0], self.segments))

    @cached_property
    def probabilities(self):
        return normalize_sum(list(map(lambda s: s[1], self.segments)))


class Language(object):
    def __init__(
        self,
        name: str,
        segment_types: List[SegmentType],
        min_segments: int,
        max_segments: int,
    ) -> None:
        self.name = name
        self.segment_types = segment_types
        self.min_segments = min_segments
        self.max_segments = max_segments

    def to_json(self):
        return json.dumps(
            {
                "name": self.name,
                "segmentTypes": list(map(lambda s: s.to_json(), self.segment_types)),
            }
        )

    def get_name(self):
        chosen_segments = []
        num_segments = randint(self.min_segments, self.max_segments)
        for _ in range(0, num_segments):
            segment_type = choice(
                self.segment_types,
                1,
                p=self.probabilities,
            )[0]
            segment = choice(
                segment_type.values,
                1,
                p=segment_type.probabilities,
            )[0]
            chosen_segments.append(segment)
        generated_name = Name(chosen_segments)
        return str(generated_name)

    @cached_property
    def probabilities(self):
        return normalize_sum(list(map(lambda st: st.probability, self.segment_types)))

    @classmethod
    def new_language(cls, name: Optional[str]):
        doubles = SegmentType(
            "doubles",
            1.0,
            [
                (a + b, 1.0)
                for a in string.ascii_lowercase
                for b in string.ascii_lowercase
            ],
        )
        triples = SegmentType(
            "triples",
            1.0,
            [
                (a + b + c, 1.0)
                for a in string.ascii_lowercase
                for b in string.ascii_lowercase
                for c in string.ascii_lowercase
            ],
        )

        return Language(name if name else "New Language", [doubles, triples], 2, 4)
