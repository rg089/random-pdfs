from fpdf import FPDF
import random
import os
import shutil

def yes_no_input(qn):
    '''
    Parameters: qn -> The question asked in string form.
    Returns: True if answer is yes, else False.
    '''
    ans = ""
    while not (ans=="y" or ans=="yes" or ans=="n" or ans=="no"):
        ans = input(qn).lower()
    if ans=="yes" or ans=="y":
        return True
    return False

def positive_int_input(qn):
    '''
    Take integer input > 0.
    Paramters: qn -> The question asked in string form.
    Returns: The integer input.
    '''
    ans = -1
    while ans<1:
        try:
            ans = int(input(qn))
        except:
            print ("Please enter an integer.")
    return ans

def get_online_data():
    '''
    Returns the wordlist from an online source.
    '''
    import requests
    source = "https://www.mit.edu/~ecprice/wordlist.10000" # For even more words, use https://www.mit.edu/~ecprice/wordlist.100000
    response = requests.get(source)
    wordlist = response.content.decode('utf-8').splitlines()
    return wordlist


def get_local_data():
    '''
    Returns the wordlist from local text file.
    '''
    with open("words.txt", "r") as f:
        wordlist = f.read().splitlines()
    return wordlist

def get_title_words(wordlist, possible_names, num):
    '''
    Helper function for get proper nouns.
    '''
    counter = 0
    title_words = []
    for i in range(num):
        if counter==2:
                title_words.append(random.choice(wordlist))
                counter = 0
        else:
            title_words.append(random.choice(possible_names))
            counter+=1
    title = " ".join(title_words)
    return title

def generate_name(wordlist):
    '''
    Randomly generates and returns a fake name.
    '''
    name = ""
    possible_names = [word for word in wordlist if word[0].isupper() and not word.isupper()]
    if len(possible_names)==0:
        name = " ".join(map(lambda x: x.capitalize(), random.choices(wordlist, k=2)))
    else:
        name = " ".join(random.choices(possible_names, k=2))
    return name

def generate_proper_nouns(wordlist, num):
    '''
    Randomly generates proper nouns from the wordlist.
    '''
    proper_nouns = [word for word in wordlist if word[0].isupper()]
    possible_names = [word for word in proper_nouns if not word.isupper()]
    possible_places = [word for word in proper_nouns if word.isupper()]

    title = ""
    title_words = []
    counter = 0
    place_in_title = bool(random.randint(0,1))  
    if place_in_title: 
        title = get_title_words(wordlist, possible_names, num-2)
        title += " at {}".format(random.choice(possible_places))
    else:
        title = get_title_words(wordlist, possible_names, num)
    return title


def generate_title(wordlist, online_wordlist):
    '''
    Generates a random title.
    '''
    length = random.randint(4,7)
    title = ""
    if not online_wordlist:
        title = generate_proper_nouns(wordlist, length)
    else:
        words = map(lambda x: x.capitalize(), random.choices(wordlist, k=length))
        title = " ".join(words)
    return title


def generate_text(wordlist):
    '''
    Generates and returns random text from the wordlist for 1 page.
    Parameters: wordlist -> A list of words in the English Language.
    '''
    num_of_sentences = random.randint(26, 33)
    words_per_sentence = random.randint(7, 10)
    total_words = num_of_sentences*words_per_sentence
    text_words = random.choices(wordlist, k=total_words)
    text = ""; capitalize = True
    for i in range(total_words):
        if capitalize:
            text += text_words[i].capitalize()
            capitalize = False
        else:
            text+= text_words[i]
        if i==total_words-1:
            text+="."
            break
        if (i+1)%words_per_sentence == 0:
            text += "."
            capitalize = True
        text += " "
    return text


def create_pdf(wordlist, title, num_pages):
    '''
    Generates a PDF. Doesn't return anything.
    Parameters: wordlist -> A list of words in the English Language.
                title -> The title of the PDF.
                num_pages -> The number of pages in the PDF.
    '''
    pdf = FPDF()
    pdf.set_font('Arial', size=15)
    pdf.set_auto_page_break(False)
    has_byline = bool(random.randint(0,1))
    for i in range(num_pages):
        pdf.add_page()
        if i==0:
            pdf.set_font('Arial', 'B', 18)
            pdf.cell(0, 20, title, ln=1, align='C')
            if has_byline:
                pdf.set_font('Arial', 'B', 16)
                pdf.cell(0, 20, "By - {}".format(generate_name(wordlist)), ln=1, align='C')
            pdf.set_font('Arial', size=15)
        text = generate_text(wordlist)
        pdf.multi_cell(w = 0, h=8, txt=text)
    pdf.output('Output/{}.pdf'.format(title))


if __name__=="__main__":
    if os.path.exists("Output"):
        shutil.rmtree("Output")
    os.makedirs("Output")

    wordlist =[]

    online_wordlist = yes_no_input("Do you want to use the online wordlist [y/n]: ")
    num_of_pdfs = positive_int_input("Please enter the number of pdfs you want to generate: ")
    print ()
    
    if online_wordlist:
        wordlist = get_online_data()
    else:
        wordlist = get_local_data()

    multiple_pdfs = False
    if num_of_pdfs>1:
        multiple_pdfs = True

    constant_length = False
    if multiple_pdfs:
        constant_length = yes_no_input("Do you want the length of each pdf to be the same [y/n]: ")

    pdf_length = 0
    if not multiple_pdfs:
        pdf_length = positive_int_input("Please enter the length of the pdf: ")
    elif constant_length:
        pdf_length = positive_int_input("Please enter the default length of your pdfs: ")

    for i in range(num_of_pdfs):
        length = pdf_length
        if length == 0:
            length = positive_int_input("Please enter the length of PDF {}: ".format(i+1))
        title = generate_title(wordlist, online_wordlist)
        create_pdf(wordlist, title, length)

    print ('\nGeneration Complete!\n')

