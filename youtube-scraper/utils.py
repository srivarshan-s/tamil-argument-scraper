import pycld2 as cld2


def is_tamil(text):

    if type(text) == str:
            _, _, _, lang = cld2.detect(text,  returnVectors=True)
            
            if len(lang) == 1 and lang[0][2] == "TAMIL":
                return True
    
    return False