from googletrans import Translator
import re
import threading
import time

tradutor = Translator()

traducao = open('example.ltf', 'r')

final = open("pt.ltf", 'w+', encoding='utf8')

final.write("""# Language Text File
LANGNAME: Português Brasileiro
GENDERS: 0
BASESTRINGS: 0
\n\n
""")

traducao = traducao.readlines()

key_id = []
texto_en = []
texto_br_sep = []

regex = r"(\[.*?\])|<\w+(\s+(\[^\]*\|'[^']*'|[^>])+)?>|<\/\w+>"
regex_KEY = r"(KEY.*?\:)|<\w+(\s+(\[^\]*\|'[^']*'|[^>])+)?>|<\/\w+>"



def traduzir_key(key, texto, arquivo, db):
    regex = r"(\[.*?\])|<\w+(\s+(\[^\]*\|'[^']*'|[^>])+)?>|<\/\w+>"
    en = re.split(regex, texto)
    en = list(filter(None, en)) 
    db_interna = []
    for index, palavra in enumerate(en):
        if palavra != None and re.search(regex, palavra, re.IGNORECASE) == None and palavra != '\n' and palavra != '\r' and palavra != '' and palavra != ' ':
            traduzida = tradutor.translate(palavra, src='en', dest='pt')
            en[index] = traduzida.text
    db_interna.append(en)
    texto_br = []
    texto_br.append(' '.join(db_interna[0]))
    final.write(key + ": " + texto)
    final.write("STR-1: " + texto_br[0] + "\n")
    print(str(en) + " OK!")

i = 0

for key in traducao:
    if "KEY" in key:
        print("Thread " + str(i) + " iniciado!")
        key_id.append(key.split(':')[0])
        texto_en.append(re.sub(regex_KEY, '', key, 1))
        #texto_en.append(texto.replace(key_id[i], ''))
        t = threading.Thread(target=traduzir_key, args=(key_id[i], texto_en[i], final, texto_br_sep))
        t.start()
        i += 1
        time.sleep(0.01)

final.close()