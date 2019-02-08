from typing import List

from decksite.data import person as ps
from decksite.view import View
from shared.container import Container


# pylint: disable=no-self-use
class PersonAchievements(View):
    def __init__(self, person: ps.Person, achievements: List[Container]) -> None:
        super().__init__()
        self.person = person
        self.achievements = achievements
        self.show_seasons = True
        self.decks = []
        for a in achievements:
            if a.detail is not None:
                a.detail.hide_active_runs = True
                self.remove_active_runs_and_set_active_run_text(a.detail)
                self.decks += a.detail.decks
        if len([a for a in achievements if a.legend]) == 0:
            self.no_achievements = True

    def page_title(self):
        return f'Achievement details: {self.person.name}'
