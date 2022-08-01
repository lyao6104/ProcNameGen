import json
import string
from functools import cached_property
from random import random
from typing import Dict, List, Optional, Tuple

from numpy.random import choice

from .util import lerp, normalize_sum


class Name(object):
    def __init__(self, segments: List[str]) -> None:
        self.segments = segments

    def to_json(self):
        return json.dumps({"name": str(self), "segments": self.segments})

    def __str__(self) -> str:
        return "".join(self.segments).capitalize()


class SegmentType(object):
    def __init__(
        self,
        name: str,
        probability: float,
        segments: Dict[str, List[Tuple[str, float]]],
    ) -> None:
        self.name = name
        self.probability = probability
        self.segments = segments

        self.normalize_segment_probabilities()

    def to_json(self):
        return json.dumps(
            {
                "name": self.name,
                "probability": self.probability,
                "segments": self.segments,
            }
        )

    def to_dict(self):
        return {
            "name": self.name,
            "probability": self.probability,
            "segments": self.segments,
        }

    def get_segment(self, current_segment: str) -> str:
        self.normalize_segment_probabilities()
        return choice(
            list(map(lambda segment: segment[0], self.segments[current_segment])),
            1,
            p=list(map(lambda segment: segment[1], self.segments[current_segment])),
        )[0]

    def normalize_segment_probabilities(self):
        for current_segment in self.segments.keys():
            segment_probabilities = normalize_sum(
                list(map(lambda s: s[1], self.segments[current_segment]))
            )
            for i in range(0, len(segment_probabilities)):
                segment_text, _ = self.segments[current_segment][i]
                self.segments[current_segment][i] = (
                    segment_text,
                    segment_probabilities[i],
                )

    @cached_property
    def values(self):
        return list(map(lambda s: s[0], self.segments))


class Language(object):
    def __init__(
        self,
        name: str,
        segment_types: List[SegmentType],
        openers: Dict[str, float],
        min_segments: int,
        max_segments: int,
        avg_segments: Optional[float] = None,
    ) -> None:
        self.name = name
        self.segment_types = segment_types
        self.openers = openers
        self.min_segments = min_segments
        self.max_segments = max_segments
        self.average_segments = avg_segments or (min_segments + max_segments) / 2

        self.normalize_segment_type_probabilities()
        self.normalize_opener_probabilities()

    def to_json(self, pretty: bool = False):
        return json.dumps(
            {
                "name": self.name,
                "segmentTypes": list(map(lambda s: s.to_dict(), self.segment_types)),
                "openers": self.openers,
                "minSegments": self.min_segments,
                "maxSegments": self.max_segments,
                "averageSegments": self.average_segments,
            },
            indent=(2 if pretty else None),
            sort_keys=pretty,
        )

    def get_name(self) -> Name:
        chosen_segments = [
            # The opener
            choice(
                list(self.openers.keys()),
                1,
                list(self.openers.values()),
            )[0]
        ]
        gen_segments = True
        while gen_segments:
        # num_segments = randint(self.min_segments, self.max_segments)
        # for _ in range(1, num_segments):
            # Choose the next segment and add it to the list
            segment_type = choice(
                self.segment_types,
                1,
                p=self.probabilities,
            )[0]
            segment = segment_type.get_segment(
                chosen_segments[len(chosen_segments) - 1][-1]
            )
            chosen_segments.append(segment)

            # Determine whether to keep going. Chance of stopping is 0% before min_segments,
            # increasing linearly to 35% at average_segments, then to 100% at max_segments.
            cur_length = len(chosen_segments)
            stop_chance = 0
            if cur_length >= self.max_segments:
                stop_chance = 1
            elif cur_length >= self.average_segments:
                t = (cur_length - self.average_segments) / (self.max_segments - self.average_segments)
                stop_chance = lerp(0.35, 1, t)
            elif cur_length >= self.min_segments:
                t = (cur_length - self.min_segments) / (self.average_segments - self.min_segments)
                stop_chance = lerp(0, 0.35, t)
            stop_roll = random()
            # print(f"Stop chance is {stop_chance} and stop roll is {stop_roll}.")
            gen_segments = stop_roll > stop_chance
        generated_name = Name(chosen_segments)
        return generated_name

    def mark_name(self, name: Name, good: bool) -> None:
        p_modifier = 1.01 if good else 0.99

        # Modify average length to be 5% closer to the length of this name if good,
        # do the opposite if bad.
        distance = len(name.segments) - self.average_segments
        if good:
            # Using addition and subtraction should be fine since distance is not absolute.
            self.average_segments += distance * 0.05
        else:
            self.average_segments -= distance * 0.05

        # Modify opener probability
        self.openers[name.segments[0]] *= p_modifier

        # Modify segment probabilities
        cur_next_segment_mapping = {}
        for i in range(0, len(name.segments) - 1):
            cur_next_segment_mapping[name.segments[i]] = name.segments[i + 1]
        # Look through segment types to find instances of each segment in the mapping
        for i in range(0, len(self.segment_types)):
            for cur_segment in cur_next_segment_mapping.keys():
                # If current segment is found, find the segment that comes after and adjust probabilities
                if cur_segment in self.segment_types[i].segments:
                    for j in range(0, len(self.segment_types[i].segments[cur_segment])):
                        next_segment, p = self.segment_types[i].segments[cur_segment][j]
                        if next_segment == cur_next_segment_mapping[cur_segment]:
                            self.segment_types[i].segments[cur_segment][j] = (
                                next_segment,
                                p * p_modifier,
                            )

        # Normalize probabilities when finished
        self.normalize_opener_probabilities()
        self.normalize_segment_type_probabilities()

    @cached_property
    def probabilities(self):
        return normalize_sum(list(map(lambda st: st.probability, self.segment_types)))

    def normalize_segment_type_probabilities(self):
        probabilities = self.probabilities
        for i in range(0, len(self.segment_types)):
            self.segment_types[i].probability = probabilities[i]

    def normalize_opener_probabilities(self):
        total_p = sum(list(self.openers.values()))
        for opener in self.openers.keys():
            self.openers[opener] /= total_p

    @classmethod
    def language_template(cls, name: Optional[str] = None):
        openers = {a: 1.0 for a in string.ascii_lowercase}
        cur_segments = [a for a in string.ascii_lowercase] + [
            a + b for a in string.ascii_lowercase for b in string.ascii_lowercase
        ]
        singles = SegmentType(
            "singles",
            1.0,
            {
                # Discourage the same letter from appearing twice in a row.
                s: [(b, 0.5 if s[-1] == b else 1.0) for b in string.ascii_lowercase]
                for s in cur_segments
            },
        )
        doubles = SegmentType(
            "doubles",
            1.0,
            {
                # Make sure two letters don't appear in a row
                s: [
                    (c + d, 1.0)
                    for c in string.ascii_lowercase
                    for d in string.ascii_lowercase
                    if s[-1] != c and c != d
                ]
                for s in cur_segments
            },
        )

        return Language(
            name if name else "New Language", [singles, doubles], openers, 2, 4
        )
