# This python file is for our data collection and annotation
import script
def main():
    links = [
        ("https://www.ratemyprofessors.com/professor/1765657", "Andrew DeOrio", "University of Michigan"),
        ("https://www.ratemyprofessors.com/professor/1836686", "David Paoletti", "University of Michigan"),
        ("https://www.ratemyprofessors.com/professor/842649", "Atul Prakash", "University of Michigan"),
        ("https://www.ratemyprofessors.com/professor/1915339", "Rada Mihalcea", "University of Michigan"),
        ("https://www.ratemyprofessors.com/professor/2277209", "Westley Weimer", "University of Michigan"),
        ("https://www.ratemyprofessors.com/professor/140940", "Brian Noble", "University of Michigan"),
        ("https://www.ratemyprofessors.com/professor/2244255", "John Benedict", "University of Michigan"),
        ("https://www.ratemyprofessors.com/professor/2300313", "Michael LoPresto", "University of Michigan"),
        ("https://www.ratemyprofessors.com/professor/1991134", "Marcus Darden", "University of Michigan")
    ]
    options = [1,3,4] # Weighted opinion lexicon not real yet
    with open("raw_data.txt", "w") as f:
        with open("annoted_data.txt", "w") as f2:
            for link, name, university in links:
                print(f"Working on {name}")
                f.write(f"Raw comments for {name} from {university}, at RMP link {link}:\n")
                prof = script.getProfessor(link, name, university)
                for comment in prof.comments:
                    f.write(f"{comment}\n")
                f.write("\n")

                f2.write(f"Annotated scores for {name} from {university}, at RMP link {link}:\n")
                for option in options:
                    f2.write(script.getData(link, name, university, option) + "\n")
                f2.write("\n")


if __name__ == "__main__":
    main()