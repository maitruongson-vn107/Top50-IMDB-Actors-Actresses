from nltk.tokenize import sent_tokenize
import calendar


def birthdayConvert(dob: str):
    dob_list = dob.split("-")
    year = dob_list[0]
    month = calendar.month_name[int(dob_list[1])]
    day = dob_list[2]
    return day + " " + month + " " + year


def bioProcess(bio: str):
    bio = sent_tokenize(bio)[:2]
    bio = "\n".join(bio)
    bio = bio.replace(",", ", ")
    bio = bio.replace(".", ". ")
    bio += "\n..."
    return bio