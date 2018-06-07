from server import psql_worker

DB = psql_worker.PsqlWorker()
print(DB.get_word_details('кура'))
print(DB.get_lemko_translation("słońce"))

polish_arr = ['dobro','wiara','nadzieja','miłość','pokój','serce','pomoc' ,'przyjaźń','współpraca','słońce','śpiew','współczucie','empatia','sympatia','odwaga','piękno','świt','muzyka','marzenia','wschód','prawda','tradycja','szacunek','pełnia','poświęcenie','perła','skarb','droga','życie','radość','życzliwość','miłosierdzie','sprawiedliwość','otwartość','uczciwość','ciepło','czułość','gościnność','łaska','słodycz','sumienie','troskliwość','uprzejmość','wielkoduszność','człowieczeństwo','zgoda','delikatność','godność','bezinteresowność','subtelność','braterstwo','jedność','różnorodność','opieka','doskonałość','wierność','poezja','sztuka','kreatywność','niebo','harmonia','szlachetność','kolor','pokora','wielobarwność','światło','uśmiech','śmiech','słowik','pożytek','odpoczynek','natura','przyroda','wieczność','raj','zmartwychwstanie','jasność','słowo','dusza','chwała','mądrość','honor','wdzięczność','wytrwałość','cierpliwość','wyrozumiałość','chrześcijaństwo','prostota','prostolinijność','wolność','wrażliwość','twórczość','spontaniczność','korzenie','zaufanie','królestwo','szczęście','witaj','dzień dobry','dziękuję','melodia']

resp = dict()

for polish in polish_arr:
    lemko_translation = DB.get_lemko_translation(polish)
    # print(DB.get_lemko_translation(polish))
    if len(lemko_translation) > 0:
        resp[polish] = lemko_translation[0][0]
    else:
        resp[polish] = ''

sorted_resp = sorted(resp.items(), key=lambda x: x[0])
for el in sorted_resp:
    print(el[0] + " - " + el[1])