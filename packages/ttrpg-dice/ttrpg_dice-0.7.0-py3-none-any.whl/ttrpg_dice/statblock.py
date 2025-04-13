"""Create statblocks easily."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from typing import TYPE_CHECKING

from tabulate2 import tabulate

from .dice import Dice

if TYPE_CHECKING:
    from contextlib import suppress

    with suppress(ImportError):
        from typing import ClassVar, Self


class StatBlock(Mapping):
    """A TTRPG StatBlock, acts as a mapping of stats."""

    _STATS: ClassVar[dict[str, Dice]]

    def __init__(self, *_args, **_kwargs) -> None:  # noqa: ANN002, ANN003
        """Raises TypeError - this method is replaced by `_init_` by the decorator."""
        if type(self) is StatBlock:
            msg = "Cannot directly instantiate a StatBlock, please use the @statblock decorator instead."
            raise TypeError(msg)
        
    def _pre_init_(self, /, **stats: int) -> dict[str, int | Dice]:
        """
        Subclasses can override this to perform actions at the start of __init__.
        
        Be sure to pop any used kwargs and return the remaining ones.
        """
        return stats
    
    def _init_(self, /, **stats: int | Dice) -> None:
        """Initialise a StatBlock with some, or all stats given."""
        stats = self._pre_init_(**stats)
        for stat in self._STATS:
            val = stats.pop(stat, vars(type(self)).get(stat, 0))
            setattr(self, stat, val)
        if stats:
            remaining_stats = ", ".join(f"`{stat}`" for stat in stats)
            msg = f"Invalid stat. {type(self).__name__} does not contain {remaining_stats}."
            raise AttributeError(msg)

    def __add__(self, other: Self) -> Self:
        """Adds each stat, raises AttributeError if stat missing in `other`."""
        newstats = {
            stat: min(self[stat] + other[stat], len(self._STATS[stat])) for stat in self._STATS
        }
        return type(self)(**newstats)
    
    def __sub__(self, other: Self) -> Self:
        """
        Subtracts each stat, raises AttributeError if stat missing in `other`.
        
        For example, if you want to take an NPC and remove a specific career.
        """
        newstats = {
            stat: max(self[stat] - other[stat], 0) for stat in self._STATS
        }
        return type(self)(**newstats)

    def __or__(self, other: Self) -> Self:
        """Merge stats, keeping the highest."""
        newstats = {stat: max(self[stat], other[stat]) for stat in self._STATS}
        return type(self)(**newstats)

    def __getitem__(self, stat: str) -> int | Dice:
        """Get a specific stat by subscripting."""
        if stat in self._STATS:
            return getattr(self, stat)
        msg = f"Unknown stat '{stat}'"
        raise KeyError(msg)
    
    def __len__(self) -> int:
        """Number of stats."""
        return len(self._STATS)
    
    def __iter__(self) -> Iterator:
        """Iterate over stats."""
        return iter(self._STATS)
    
    def __str__(self) -> str:
        """A description of the Statblock type e.g. 'Human Warhammer StatBlock'."""
        cls = type(self)
        bases = cls.mro()
        statblock_index = bases.index(StatBlock)
        return " ".join(base.__name__ for base in bases[:statblock_index+1])

    def __repr__(self) -> str:
        """Statblock type as per `str` plus the stats and their challenge rolls."""
        return (
            str(self)
            + "("
            + ", ".join(f"{statname}: {roll} = {self[statname]}" for statname, roll in self._STATS.items())
            + ")"
        )
    
    def as_table(self) -> str:
        """Render the StatBlock as a github markdown table."""
        return tabulate([[*self.values()]], headers=self.keys(), tablefmt="github")

    def _repr_markdown_(self) -> str:
        """For IPython notebooks - L3 header and stat table."""
        return f"### {self}\n{self.as_table()}"

def statblock(cls: type) -> StatBlock:
    """Create a StatBlock with the given fields."""
    stats = {statname: roll for statname, roll in vars(cls).items() if isinstance(roll, Dice)}
    _interimclass: type = type(
        cls.__name__,
        (StatBlock,),
        {attr: 0 if attr in stats else val for attr, val in vars(cls).items() if attr != "__dict__"},
    )
    _interimclass.__annotations__ = dict.fromkeys(stats, int | Dice)
    _interimclass._STATS = stats  # noqa: SLF001
    _interimclass.__init__ = StatBlock._init_
    return _interimclass
