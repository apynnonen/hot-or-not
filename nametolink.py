import requests
import bs4


def name_to_link(name, university):
    # # get name
    # name = input(
    #     "Please insert the first and last name of the professor you are looking for or STOP if you wish to exit:\n")
    # if name.lower() == "stop" or name.lower() == 'exit':
    #     return 1

    # # get University
    # university = input(
    #     "Please insert the university of the professor you are looking for:\n")

    # name = "brian noble"
    # university = "university of michigan "

    # format google search
    search = name.replace(" ", "+") + "+" + university.replace(" ", "+")
    URL = 'https://www.google.com/search?q=rate+my+professors+' + search

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    page = requests.get(URL, headers=headers).text
    soup = bs4.BeautifulSoup(page, 'html.parser')
    # find first result <a> tag
    link = soup.find("div", {"class": "egMi0 kCrYT"})
    link = link.find("a")

    # find professor tid
    temp = str(link).find("tid%") + 6
    temp2 = str(link).find("&amp", temp-6)
    if temp == 5:
        temp = str(link).find("/professor/") + 11
        temp2 = str(link).find("&amp", temp-11)
        if temp == 10:
            print("Invalid credentials!")
            print("Try again")
            return 1
    tid = str(link)[temp:temp2]
    link = "https://www.ratemyprofessors.com/professor?tid=" + str(tid)
    return link, name.title(), university.title()


# name_to_link()
