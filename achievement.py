from pychievements import Achievement
from pychievements.icons import unicodeCheck

class BigEater(Achievement):
    name = "Big Eater"
    category = "game"
    goals = (
        {'level': 1, 'name': '첫 걸음!', 'description': '처음으로 먹이를 먹었다!', 'icon': unicodeCheck},
        {'level': 5, 'name': '성장 중!', 'description': '5개를 먹었다!', 'icon': unicodeCheck},
    )

    def evaluate(self, current_count, *args, **kwargs):
        self._current = current_count
        return self.achieved

class RightWalker(Achievement):
    name = "Right Walker"
    category = "game"
    goals = (
        {'level': 5, 'name': '우측 본능', 'description': '오른쪽 키를 5번 눌렀다!', 'icon': unicodeCheck},
    )

    def evaluate(self, right_count, *args, **kwargs):
        self._current = right_count
        return self.achieved

