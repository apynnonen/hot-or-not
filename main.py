# Hot or Not
class ProfessorRating:
    # Possible attributes, edit as needed
    rating = 0 # from website scale
    rating_label = "" # e.g. "Hot" or "not hot" or "lukewarm"
    name = 0 # self-explanatory
    website_link = "ratemyprofessor.com" # direct link to this specific professor's page
    university = "University of Michigan" # which university this professor teaches for
    class_name = "" # EECS482
    def __int__(self):
        pass

    def rating(self):
        return self.rating

    def how_hot(self):
        return self.rating_label