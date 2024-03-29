import items
import enemies
import world
import actions


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError()

    def modify_player(self, player):
        raise NotImplementedError()

    def adjacent_moves(self):
        moves = []
        if world.tile_exists(self.x+1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x-1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y+1):
            moves.append(actions.MoveSouth())
        if world.tile_exists(self.x, self.y-1):
            moves.append(actions.MoveNorth())
        return moves

    def available_actions(self):
        """ Returns all of the available actions in this room """
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())
        return moves


class StartingRoom(MapTile):
    def intro_text(self):
        return """
        You find yourself if a cave with a flickering torch on the wall.
        You can make out four paths, each equally as dark and foreboding.
        """

    def modify_player(self, player):
        # room has no action on player
        pass


class LootRoom(MapTile):
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)

    def add_loot(self, player):
        player.inventory.append(self.item)
        self.item = None
    
    def modify_player(self, player):
        if self.item is not None:
            self.add_loot(player)



class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print(
                f"Enemy does {self.enemy.damage}. You have {the_player.hp} HP remaining.")

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()


class EmptyCavePath(MapTile):
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """

    def modify_player(self, player):
        # Room has no action on player
        pass


class GiantSpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantSpider())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant spider jumps down from its web in front of you!
            """
        else:
            return """
            The corpse of a dead spider rots on the ground.
            """


class FindDaggerRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Dagger())

    def intro_text(self):
        if self.item is None:
            return EmptyCavePath.intro_text(self)

        return """
        Your notice something shiny in the corner.
        It's a dagger! You pick it up.
        """


class OgreRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Ogre())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            An ogre is looking at you very aggressively.
            """
        else:
            return """
            The corpse of an ogre rots on the ground.
            """


class FindGoldRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Gold(amt=100))

    def intro_text(self):
        return """
        You notice some gold on the ground. 
        You pick it up.
        """


class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!

        Victory is yours!
        """

    def modify_player(self, player):
        player.victory = True
