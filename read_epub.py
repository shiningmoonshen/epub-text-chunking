import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import sys
import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

def main():
    #opens source file and returns pickled dictionary of text in chunks of length 50-200
    book = epub.read_epub(sys.argv[1])
    items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    #save all chapters in a list
    chapters = chap_as_list(items)
    #chunk texts, limiting length
    chunks = chunk(chapters)
    print(chunks['OEBPS/Oblivion_chap_1.html'][61])
    return chunks

def chap_as_list(items):
    #filter out and store all chapters in a list
    chapters = []
    for c in items:
        if 'chap' in c.get_name():
            chapters.append(c)
    return chapters

#use BeautifulSoup to read out only the text in each chapter, saved as a list of paragraphs
def chapter_to_str(chapter):
    soup = BeautifulSoup(chapter.get_body_content(), 'html.parser')
    text = [para.get_text() for para in soup.find_all('p')]
    for ti in range(len(text)):
        text.insert(ti, split_text_by_word_count(text[ti], 250))
    return text

def chunk(chapters):
    #save chunks into dictionary
    texts = {}
    for c in chapters:
        texts[c.get_name()] = chapter_to_str(c)
    return texts

def split_text_by_word_count(text, word_count):
    # Process the text using spaCy
    doc = nlp(text)

    segments = []
    curr_segment = []
    curr_word_count = 0

    for token in doc:
        # Count only non-punctuation tokens
        if not token.is_punct:
            curr_word_count += 1
            curr_segment.append(token.text)

            if curr_word_count >= word_count:
                segments.append(" ".join(curr_segment))
                curr_segment = []
                curr_word_count = 0

    # Append any remaining words to the last segment
    if curr_segment:
        segments.append(" ".join(curr_segment))

    #returns a list of segments, all under set word count
    return segments

main()
#print(len(texts['OEBPS/Oblivion_chap_1.html']))
#print(texts.keys())