from googletrans import Translator
import re

tradutor = Translator()

traducao = open('example.ltf', 'r')

traducao = traducao.readlines()

key_id = []
texto_en = []
texto_br_sep = []

regex = r"(\[.*?\])|<\w+(\s+(\[^\]*\|'[^']*'|[^>])+)?>|<\/\w+>"
regex_KEY = r"(KEY.*?\:)|<\w+(\s+(\[^\]*\|'[^']*'|[^>])+)?>|<\/\w+>"

i = 0
for key in traducao:
    if "KEY" in key:
        key_id.append(key.split(':')[0])
        texto_en.append(re.sub(regex_KEY, '', key, 1))
        #texto_en.append(texto.replace(key_id[i], ''))
        print(texto_en[i])
        en = re.split(regex, texto_en[i])
        en = list(filter(None, en)) 
        for index, palavra in enumerate(en):
            if palavra != None and re.search(regex, palavra, re.IGNORECASE) == None and palavra != '\n' and palavra != '\r' and palavra != '' and palavra != ' ':
                traduzida = tradutor.translate(palavra, src='en', dest='pt')
                en[index] = traduzida.text
        texto_br_sep.append(en)
        i += 1


key_len = len(key_id)

i = 0
texto_br_sep_len = len(texto_br_sep)

texto_br = []

while(i < texto_br_sep_len):
    texto_br.append(' '.join(texto_br_sep[i]))
    
    i += 1

texto_br = list(dict.fromkeys(texto_br))


print("\n\nTotal frases: " + str(len(texto_br)) + "\nTotal Keys: " + str(key_len))

final = open("pt.ltf", 'w+', encoding='utf8')

final.write("""# Language Text File
LANGNAME: Português Brasileiro
GENDERS: 0
BASESTRINGS: 0
\n\n
""")

i = 0

while(i < len(texto_br)):
    final.write(key_id[i] + ": " + texto_en[i])
    final.write("STR-1: " + texto_br[i] + "\n")
    i += 1


final.close()

