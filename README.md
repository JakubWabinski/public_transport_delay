Modelowanie opóźnień transportu miejskiego

Projekt z pogranicza Data Science i Systemów informacji Przestrzennej (GIS). Wiele miast, w tym Warszawa, udostępnia dane dotyczące transportu miejskiego. Najistotniejszym elementem są logi pozycyjne (czas wysłania/odebrania sygnału GNSS oraz aktualne współrzędne). Na ich podstawie można modelować przemieszczanie się pojazdów komunikacji miejskiej (tramwajów, autobusów). 

Wzbogacając te logi o dodatkowe dane z portalu Dane po Warszawsku, m. in. dane przystankowe, o brygadach, pojazdach we flocie, a także Głównego Urzędu Statystycznego (gęstość zaludnienia, struktura społeczna), Geoportalu (formy użytkowania terenu, budynki), serwisów pogodowych, informacji o natężeniu ruchu (korkometr); jesteśmy w stanie zbudować model przewidujący opóźnienia na wybranych trasach w określonych warunkach. 

Urząd Miasta byłby zapewne zainteresowany współpracą. Wynika naszych analiz pozwolą im na dopasowanie rozkładów jazdy do faktycznych warunków na drogach. Poza tym, analizując strukturę demograficzną różnych części Warszawy, możliwe będzie wyciągnięcie wniosków na temat tego, gdzie należałoby zwiększyć, a gdzie zmniejszyć częstotliwość kursowania pojazdów lub wręcz zaprojektować nowe linie.

Oprócz zadań związanych czysto z modelowaniem, projekt będzie wymagał kilku przemyśleń na poziomie koncepcyjnym, np. jak wyekstrapolować z danych (logi z pozycją co 30 sekund lub mniej) moment, w którym pojazd pojawia się na przystanku? Poza tym trzeba będzie opracować efektywny sposób mapowania pozycji z logów na wektorowe wersje tras przejazdu poszczególnych linii (systemy pozycjonowania charakteryzują nawet kilkunastometrowymi błędami, zwłaszcza w okolicy wysokiej zabudowy).

Wyzwaniem w przypadku tego projektu będzie na pewno objętość danych. Logi samych tramwajów z jednego miesiąca to prawie 1 GB danych. Wydaje się, że początkowo należałoby się skupić na kilku wybranych trasach i pozyskać dane historyczne, np. z 3 lat (zakładam, że jest to możliwe, ale musiałbym dopytać ludzi z Warszawskiego Transportu Publicznego). Dłuższy zakres dat pozwoli z jednej strony na wyłapanie sezonowych trendów, ale z drugiej strony powoduje na przykład ryzyko wystąpienia zmian w rozkładach konkretnej linii.

______________________________________________________________

Próbka danych (tramwaje z jednego dnia) udostępnionych przez ZTM – dostępne w folderze raw_data

vhl_namespace	vhl_name	lsh_time	lsh_added	lat	lon	ol	ob<br/>
0	tw	3205	2022-04-15 00:00:04+02	2022-04-15 00:00:12.227338+02	52.24824	21.04631	26	11<br/>
1	tw	3205	2022-04-15 00:00:09+02	2022-04-15 00:00:12.32113+02	52.248295	21.046158	26	11<br/>
2	tw	3205	2022-04-15 00:00:14+02	2022-04-15 00:00:16.734894+02	52.2483	21.04614	26	11<br/>
3	tw	3205	2022-04-15 00:00:20+02	2022-04-15 00:00:21.980338+02	52.2483	21.04614	26	11<br/>
4	tw	3205	2022-04-15 00:00:25+02	2022-04-15 00:00:27.218877+02	52.2483	21.04614	26	11

Gdzie:<br/>
vhl_namespace >> typ pojazdu, tw = tramwaj<br/>
vhl_name >> numer boczny pojazdu <br/>
lsh_time >> data wysłania sygnału GNSS z pojazdu ??<br/>
lsh_added >> data odbioru sygnału GNSS w centrali ??<br/>
lat/long >> szerokość/długość geograficzna <br/>
ol >> numer linii<br/>
ob >> numer brygady**<br/>
______________________________________________________________

Obecna próbka danych – do pozyskania za pomocą skryptu korzystającego z API 

{"Lines": "35", "Lon": 21.021528, "VehicleNumber": "1219+1218", "Time": "2022-07-06 14:27:33", "Lat": 52.17795, "Brigade": "10"}, <br/>
{"Lines": "28", "Lon": 20.971552, "VehicleNumber": "1222", "Time": "2022-07-06 14:27:33", "Lat": 52.264355, "Brigade": "5"}, <br/>
{"Lines": "15", "Lon": 20.990152, "VehicleNumber": "1229+1230", "Time": "2022-07-06 14:27:30", "Lat": 52.26475, "Brigade": "6"}, <br/>
{"Lines": "35", "Lon": 20.957766, "VehicleNumber": "1247+1248", "Time": "2022-07-06 14:27:31", "Lat": 52.268127, "Brigade": "7"}, <br/>
{"Lines": "28", "Lon": 21.034035, "VehicleNumber": "1257+1258", "Time": "2022-07-06 14:27:30", "Lat": 52.255352, "Brigade": "2"}, <br/>
{"Lines": "27", "Lon": 20.971832, "VehicleNumber": "1267", "Time": "2022-07-06 14:27:29", "Lat": 52.27279, "Brigade": "5"}

______________________________________________________________

PYTANIA I ODPOWIEDZI:

Z czego wynikają rozbieżności pomiędzy kolejnymi wysłanymi sygnałami GPS wysłanymi przez pojazdy? Według dokumentacji rozdzielczość czasowa danych to 10 sekund. W rzeczywistości te odstępy są bardzo różne, a wielokrotnie zdarzają się odstępy kilkuminutowe. Te sytuacje można by było wytłumaczyć brakiem sygnału GPS w określonych momentach, gdyby te luki występowały tylko dla atrybutu GPS_received, ale w takiej sytuacji interwał w GPS_sent powinien być zawsze taki sam – 10 sekund.

Opiszę schemat gromadzenia danych. Dane z pojazdów są przesyłane do serwera agregującego dane (już zawierają timestamp GPS). Następnie nasz mechanizm odpytuje serwer agregujący co 10 sekund. Stąd czas odczytu będzie zróżnicowany a nie wielokrotnością 10 sekund.

2.	Wprawdzie trafił się tylko jeden przypadek, ale skąd się biorą braki przypisanej brygady do rekordu danych?

Problem danych źródłowych z pojazdu. Na szczęście niezbyt często występujący.

3.	Przepraszam, ale nie do końca rozumiem. Z jaką częstotliwością w takim razie dane są wysyłane z pojazdów na serwer? Czy jeżeli Państwa mechanizm odpytuje serwer co 10 sekund, to w atrybucie GPS_received odstępy nie powinny wynosić 10 sekund? Zmierzam do tego, że nieregularność w odstępach dotyczy zarówno GPS_sent, jak i GPS_received. No i skąd się biorą te kilkuminutowe luki (zdarzają się również w trakcie kursów, a więc to nie jest kwestia oczekiwania na przystanku końcowym/początkowym)?

W danych o ile pamiętam był jeden parametr dotyczący czasu i dotyczy on czasu rejestracji lokalizacji pojazdu.

______________________________________________________________

POZOSTAŁE USTALENIA…

System liczący relację pojazdu do rozkładu, czyli to na wyświetlaczach obok kierowcy (o czym ostatnio wspominałem), to jest wewnętrzny system pojazdu. Kierowca wklepuje na samym początku trasę, jaką będzie właśnie jechał (jeszcze na pętli). Pojazd liczy tylko przejechany dystans, a informacja o odległościach między przystankami jest zapisana jako trasa, czyli w ogóle nie ma tutaj pozycjonowania satelitarnego.
Rozwiązanie zagadki związanej z brakującym atrybutem identyfikatora pojazdu (numer boczny) dla danych wrześniowych – ten atrybut zaczął być udostępniany dopiero niedawno, czyli już po wrześniu 2020. Dane historyczne nie będą w takim razie tego atrybutu miały, a to uniemożliwia w zasadzie jednoznaczną identyfikację pojazdu (aktualnie ustalam, kiedy ta zmiana miała miejsce).
W ramach transportu miejskiego jest wielu przewoźników, główny to MZA, poza tym Tramwaje Warszawskie, Mobilis, Arriva…
Dane przez sieć komórkową z pojazdów trafiają na serwery przewoźników, później do ZTM, gdzie są agregowane, następnie do Urzędu Miasta i dopiero do API. Dużo rzeczy po drodze może pójść nie tak i stąd dziury w danych.
Każdy z tych przewoźników gromadzi inne dane, ale jak to później udostępnia zbiorczo ZTM, to jakby równają w dół, czyli udostępniają takie dane, które mają wszyscy. Poszczególni przewoźnicy mogą mieć bardziej szczegółowe dane – więcej atrybutów.
https://www.ztm.waw.pl/statystyki/ >> tam na przykład informacje o aktualnej liczbie pojazdów.
Za 1-2 lata (licząc od września 2020) chcieliby już mieć informację o przybyciu pojazdu na konkretny przystanek.

