from __future__ import annotations

from render_order import RenderOrder
import copy
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from ai import BaseAI
    from fighter import Fighter
    from game_map import GameMap

T = TypeVar('T', bound='Entity')


class Entity:
    # generic entity to represent stuff: players, enemies, items, etc.

    parent: GameMap

    def __init__(
        self,
        parent: Optional[GameMap] = None,
        x:int=0,
        y:int=0,
        char:str='?',
        color:Tuple[int,int,int]=(255,255,255),
        name:str='<Unnamed>',
        blocks_movement: bool=False,
        render_order: RenderOrder = RenderOrder.CORPSE,
        ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.block_movement = blocks_movement
        self.render_order = render_order
        if parent:
            # if parent isn't provided now then it will be set later
            self.parent = parent
            parent.entities.add(self)

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap
    
    def spawn(self: T, gamemap: GameMap, x:int, y:int) -> T:
        # Spawn a copy of this instance at given location
        clone = copy.deepcopy(self)
        clone.x=x
        clone.y=y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x:int, y:int, gamemap:Optional[GameMap]=None) -> None:
        # Place this entity at a new location. Handles moving across GameMaps
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, 'parent'): # Possibly uninitialized.
                if self.parent is self.gamemap:
                    self.gamemap.entities.remove(self)
            self.parent = gamemap
            gamemap.entities.add(self)
    # method to move
    def move(self, dx:int, dy:int) -> None:
        self.x += dx
        self.y += dy


class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        ai_cls: Type[BaseAI],
        fighter: Fighter
    ):

        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR
        )

        self.ai: Optional[BaseAI] = ai_cls(self)

        self.fighter = fighter
        self.fighter.parent = self

    @property
    def is_alive(self) -> bool:
        # Returns true as long as actor can perform actions
        return bool(self.ai)
