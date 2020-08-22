from googletrans import Translator
import re
import threading
import time
import sys

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
    tradutor = Translator()
    regex = r"(\[.*?\])|<\w+(\s+(\[^\]*\|'[^']*'|[^>])+)?>|<\/\w+>"
    en2 = []
    en = re.split(regex, texto)
    en = list(filter(None, en))
    for elemento in en:
        en2.append(elemento.strip())
    for index, palavra in enumerate(en2):

        if palavra != None and re.search(regex, palavra, re.IGNORECASE) == None and palavra != '' and palavra != ' ' and palavra != '  ' and palavra != '   ':
            try:
                traduzida = tradutor.translate(palavra, src='en', dest='pt')
                en2[index] = traduzida.text
                if(palavra == traduzida.text):
                    traduzida = tradutor.translate(palavra, src='en', dest='pt')
                    en2[index] = traduzida.text
            except:
                print('Erro na tradução da palavra "' + palavra + '"!', sys.exc_info()[0])
                print(type(palavra))
    final.write(key + ": " + texto)
    final.write("STR-1: " + str(' '.join(en2) + "\n"))

i = 0
for key in traducao:
    if "KEY" in key:
        print("Thread " + str(i) + " iniciado!")
        key_id.append(key.split(':')[0])
        texto_en.append(re.sub(regex_KEY, '', key, 1))
        t = threading.Thread(target=traduzir_key, args=(key_id[i], texto_en[i], final, texto_br_sep))
        t.start()
        time.sleep(0.01)
        i += 1

while(threading.active_count() > 1):
    print("Aguardando 5 segundos para a finalização de todos os Threads\nThreads ativos: " + str(threading.active_count()))
    time.sleep(5)

print("Todos os Threads finalizados!")
final.close()