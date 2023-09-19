from flask import abort
from sql.models.natures import Natures
from extensions import db


class StatsCalculator:
    def calculate_stats(
        self,
        # pokemon: str | int = None,
        hp: tuple = None,
        attack: tuple = None,
        defense: tuple = None,
        special_attack: tuple = None,
        special_defense: tuple = None,
        speed: tuple = None,
        nature: str = None,
        level=100,
    ):
        """calculates the stats of a pokemon given its nature, level, IVs, and EVs

        Args:
            pokemon (str | int, optional): pokemon name or id. Defaults to None.
            hp (tuple, optional): tuple in form of (base stat, iv, ev). Defaults to None.
            attack (tuple, optional): tuple in form of (base stat, iv, ev). Defaults to None.
            defense (tuple, optional): tuple in form of (base stat, iv, ev). Defaults to None.
            special_attack (tuple, optional): tuple in form of (base stat, iv, ev). Defaults to None.
            special_defense (tuple, optional): tuple in form of (base stat, iv, ev). Defaults to None.
            speed (tuple, optional): tuple in form of (base stat, iv, ev). Defaults to None.
            nature (str, optional): name of pokemon's nature. Defaults to None.
            level (int, optional): pokemon level. Defaults to 100.
        """
        # if pokemon:
        #     pass
        ret = {
            "hp": hp,
            "attack": attack,
            "defense": defense,
            "special-attack": special_attack,
            "special-defense": special_defense,
            "speed": speed,
        }

        calculated = {}

        for stat_name, stat_values in ret.items():
            if stat_name == "hp":
                base_stat, iv, ev = stat_values
                calculated["hp"] = self._calculate_hp(base_stat, iv, ev, level)
            else:
                nature_effect_1, nature_effect_2 = self._get_nature_modifiers_from_db(
                    nature
                )

                if stat_name == nature_effect_1[0]:
                    nature_mod = nature_effect_1[1]
                elif stat_name == nature_effect_2[0]:
                    nature_mod = nature_effect_2[1]
                else:
                    nature_mod = 1

                base_stat, iv, ev = stat_values
                calculated[stat_name] = self._calculate_stat(
                    base_stat, iv, ev, level, nature_mod
                )

        return calculated

    def _calculate_hp(self, base, iv, ev, level):
        """HP calculation is different than those of other stats"""
        part_1 = 2 * base
        part_1 += iv
        part_1 += ev / 4
        part_1 *= level
        part_1 /= 100
        part_2 = level + 10
        return int(part_1) + int(part_2)

    def _calculate_stat(self, base, iv, ev, level, nature_mod=1, is_speed=False):
        """Calculate non-HP stats"""
        result = 2 * base
        result += iv
        result += ev / 4
        result = int(result)
        result *= level
        result /= 100
        result = int(result)  # get floor
        result += 5
        if not is_speed:
            result = result * nature_mod  # formula uses floor again
        return int(result)

    def _get_nature_modifiers(self, nature):
        """Placeholder for adamant nature as of now"""
        return ("attack", 1.1), ("special-attack", 0.9)

    def _get_nature_modifiers_from_db(self, nature):
        query = db.session.query(Natures.increased_stat, Natures.decreased_stat).filter(
            Natures.name == nature.lower()
        )
        result = query.all()
        if not result:
            abort(500, "Could not find nature {nature}")
        result = result[0]
        buffed_stat, nerfed_stat = result
        if not buffed_stat and not nerfed_stat:
            # placeholder, use to not modify any stats
            return ("attack", 1), ("attack", 1)
        return (buffed_stat, 1.1), (nerfed_stat, 0.9)
