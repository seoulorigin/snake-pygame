from pychievements import Achievement
from pychievements.icons import unicodeCheck

class BigEater(Achievement):
    name = "Big Eater"
    category = "game"
    goals = (
        {'level': 1, 'name': 'First!', 'description': 'first eat', 'icon': unicodeCheck},
    )

    def evaluate(self, current_count, *args, **kwargs):
        self._current = current_count
        return self.achieved
