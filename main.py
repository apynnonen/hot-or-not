import bs4
import requests
import typing
import string
# Hot or Not


# Lexicons for opinion lexicon sentiment analysis
positive_lexicon = []
negative_lexicon = []

class ProfessorRating:
    # Possible attributes, edit as needed
    true_rating = 0 # from website scale
    homemade_rating = None
    sentiment_method = None
    label = "" # e.g. "Hot" or "not hot" or "lukewarm"
    name = "" # self-explanatory
    website_link = "ratemyprofessors.com" # direct link to this specific professor's page
    university = "University of Michigan" # which university this professor teaches for
    comments = [] # Comments scraped from ratemyprofessors

    def __init__(self, name, rating, link, university, comments):
        self.name = name
        self.true_rating = rating
        self.website_link = link
        self.university = university
        self.comments = comments

    def true_rating(self):
        return self.true_rating
    
    def rating(self):
        return self.rating

    def how_hot(self):
        return self.label
    
    def print_summary(self):
        print("Professor "+self.name+" is a professor at the "+self.university+" who has had comments written by "+str(len(self.comments))+" students.")
        if self.sentiment_method != None:
            print("Using the "+self.sentiment_method+" method, professor "+self.name+" has a rating of "+str(self.homemade_rating)+".")
            print("The true rating from ratemyprofessors is "+str(self.true_rating)+".")


def clean(comment: str) -> str:
    # Clean up a comment so that its ready for text processing TODO
    return comment.translate(str.maketrans('', '', string.punctuation))

def scrape(link: str) -> ProfessorRating:
    # Scrape the ratemyprofessors website with the given link to find information about a professor

    # Get the page
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.get(link, headers=headers)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')

    # Find true rating
    true_rating = float(soup.find("div", {"class": "RatingValue__Numerator-qw8sqy-2 liyUjw"}).next)*2

    #Find name and university
    name_div = soup.find("div", {"class": "NameTitle__Name-dowf0z-0 cfjPUG"})
    first_name = name_div.next.next
    last_name = name_div.find("span", {"class": "NameTitle__LastNameWrapper-dowf0z-2 glXOHH"}).next
    university = name_div.next_sibling.contents[1].next


    #Find comments
    comments = []
    comments_div = soup.find_all("div", {"class": "Comments__StyledComments-dzzyvm-0 gRjWel"})
    for comment in comments_div:
        comments.append(clean(comment.next))

    professor = ProfessorRating((first_name+" "+last_name), true_rating, link, university, comments)
    return professor


def opinion_lexicon(comment_list: typing.List[str]) -> float:
    # This method takes in the comments from a professor and uses the opinion lexicons to generate a rating.
    global positive_lexicon
    global negative_lexicon
    score = 0
    wc = 0
    for comment in comment_list:
        for word in comment.split(" "):
            if word in positive_lexicon:
                score = score + 1
            if word in negative_lexicon:
                score = score - 1
            wc += 1
    return round(score/wc * 200, 1)
#should we add w
def main():
    global positive_lexicon
    global negative_lexicon
    with open("negative-words.txt") as f:
        for line in f:
            negative_lexicon.append(line.strip())
    with open("positive-words.txt") as f:
        for line in f:
            positive_lexicon.append(line.strip())
    while True:
        link = input("Enter the link of a professor you want to learn about, or STOP to exit: ")
        if link.lower() == "stop" or link.lower() == 'exit':
            break
        try:
            professor = scrape(link)
            #professor = scrape("https://www.ratemyprofessors.com/professor?tid=140940")
        except:
            print("Invalid link")
        print("Evaluation methods:")
        print("1. Opinion Lexicons: This method solely uses the total" +
              "number of positive and negative words to try and determine "+
              "the overall sentiment of the comments to generate a rating score")
        print("2. [Under Construction]")
        choice = int(input("Which method would you like (enter the number): "))
        if choice == 1:
            professor.homemade_rating = opinion_lexicon(professor.comments)
            professor.sentiment_method = "Opinion Lexicon"
        else:
            print("Choice not valid")
        professor.print_summary()

if __name__ == "__main__":
    main()