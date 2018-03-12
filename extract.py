from bs4 import BeautifulSoup as bs
from greekutils.beta2unicode import convert
import logging
import begin

def s_convert(w):
    """Fix final sigma conversion."""
    try:
        if w[-1] in ['s', 'S']:
            return convert(w.upper())[:-1] + '\u03c2'
        return convert(w.upper())
    except:
        logging.error('could not convert %s' % w)


@begin.start
def main(src_xml, out='output.txt', sep='::'):
    """Extract vocabulary from xml file and build table.

    The Perseus vocabulary tool allows one to build an xml file of
    vocabulary from works in the database. This script will pull that
    vocabulary from =src_xml=, convert Greek text to unicode, and
    store it in a file name by the =out= parameter. The parameter
    =sep=, can be set to '\t' (for example) to produce tab separated
    rows. (Such files can be easily imported into Anki.)

    """
    
    soup = bs(open(src_xml).read(), 'lxml')  
    data = [(p[0].text, s_convert(p[1].text), p[2].text)
             for p in zip(soup('weightedfrequency'),
                          soup('headword'),
                          soup('shortdefinition'))]
    res = ''
    words = []
    for item in data:
        try:
            if item[1].replace('\n', '') in words:
                continue
            else:
                res += '{}{}{}{}{}\n'.format(item[0],
                                             sep,
                                             item[1].replace('\n', ''),
                                             sep,
                                             item[2].replace('\n', ''))
                words.append(item[1].replace('\n', ''))
        except:
            continue
    with open(out, 'w') as f:
        f.write(res)
    return res
