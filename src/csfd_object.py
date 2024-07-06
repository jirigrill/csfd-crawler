from dataclasses import dataclass, field
from typing import List

@dataclass
class CSFDObject:
    type: str
    url: str
    name: str
    year: int
    genre: List[str] = field(default_factory=list)
    country: List[str] = field(default_factory=list)
    rating: int = 0

    def __eq__(self, other):
        if not isinstance(other, CSFDObject):
            return False
        return (
            self.type == other.type
            and self.url == other.url
            and self.name == other.name
            and self.year == other.year
            and self.genre == other.genre
            and self.country == other.country
            and self.rating == other.rating
        )

    def __hash__(self):
        # Convert mutable list to tuple to make it hashable
        genre_tuple = tuple(self.genre)
        genre_country = tuple(self.country)
        return hash(
            (
                self.type,
                self.url,
                self.name,
                self.year,
                genre_tuple,
                genre_country,
                self.rating,
            )
        )