Modelowanie opóŸnieñ transportu miejskiego

Projekt z pogranicza Data Science i Systemów informacji Przestrzennej (GIS). Wiele miast, w tym Warszawa, udostêpnia dane dotycz¹ce transportu miejskiego. Najistotniejszym elementem s¹ logi pozycyjne (czas wys³ania/odebrania sygna³u GNSS oraz aktualne wspó³rzêdne). Na ich podstawie mo¿na modelowaæ przemieszczanie siê pojazdów komunikacji miejskiej (tramwajów, autobusów). 

Wzbogacaj¹c te logi o dodatkowe dane z portalu Dane po Warszawsku, m. in. dane przystankowe, o brygadach, pojazdach we flocie, a tak¿e G³ównego Urzêdu Statystycznego (gêstoœæ zaludnienia, struktura spo³eczna), Geoportalu (formy u¿ytkowania terenu, budynki), serwisów pogodowych, informacji o natê¿eniu ruchu (korkometr); jesteœmy w stanie zbudowaæ model przewiduj¹cy opóŸnienia na wybranych trasach w okreœlonych warunkach. 

Urz¹d Miasta by³by zapewne zainteresowany wspó³prac¹. Wynika naszych analiz pozwol¹ im na dopasowanie rozk³adów jazdy do faktycznych warunków na drogach. Poza tym, analizuj¹c strukturê demograficzn¹ ró¿nych czêœci Warszawy, mo¿liwe bêdzie wyci¹gniêcie wniosków na temat tego, gdzie nale¿a³oby zwiêkszyæ, a gdzie zmniejszyæ czêstotliwoœæ kursowania pojazdów lub wrêcz zaprojektowaæ nowe linie.

Oprócz zadañ zwi¹zanych czysto z modelowaniem, projekt bêdzie wymaga³ kilku przemyœleñ na poziomie koncepcyjnym, np. jak wyekstrapolowaæ z danych (logi z pozycj¹ co 30 sekund lub mniej) moment, w którym pojazd pojawia siê na przystanku? Poza tym trzeba bêdzie opracowaæ efektywny sposób mapowania pozycji z logów na wektorowe wersje tras przejazdu poszczególnych linii (systemy pozycjonowania charakteryzuj¹ nawet kilkunastometrowymi b³êdami, zw³aszcza w okolicy wysokiej zabudowy).

Wyzwaniem w przypadku tego projektu bêdzie na pewno objêtoœæ danych. Logi samych tramwajów z jednego miesi¹ca to prawie 1 GB danych. Wydaje siê, ¿e pocz¹tkowo nale¿a³oby siê skupiæ na kilku wybranych trasach i pozyskaæ dane historyczne, np. z 3 lat (zak³adam, ¿e jest to mo¿liwe, ale musia³bym dopytaæ ludzi z Warszawskiego Transportu Publicznego). D³u¿szy zakres dat pozwoli z jednej strony na wy³apanie sezonowych trendów, ale z drugiej strony powoduje na przyk³ad ryzyko wyst¹pienia zmian w rozk³adach konkretnej linii.

______________________________________________________________

Próbka danych (tramwaje z jednego dnia) – dostêpne w folderze trams_September2020 
>> brak numeru bocznego pojazdu:

Column1	line_number	brigade	latitude	longitude	GPS_sent	GPS_received
4	4	3	21.025087	52.296046999999994	01.09.2020 21:30:51	01.09.2020 21:31:01
6	4	3	21.025719	52.295193	01.09.2020 21:31:01	01.09.2020 21:31:14
8	4	6	21.024124	52.19627	01.09.2020 22:31:17	01.09.2020 22:31:24
9	4	13	21.021442	52.177704	01.09.2020 19:30:46	01.09.2020 19:31:00
10	4	1	21.022382999999998	52.264034	01.09.2020 21:31:03	01.09.2020 21:31:14

______________________________________________________________

Obecna próbka danych – do pozyskania za pomoc¹ skryptu korzystaj¹cego z API 
>> s¹ ju¿ numery boczne pojazdu:

"Brigade": "014"}	 {"Lines": "4"	 "Lon": 21.024202	 "VehicleNumber": "3187"	 "Time": "2022-02-27 18:07:30"	 "Lat": 52.19709
 "Brigade": "014"}	 {"Lines": "4"	 "Lon": 21.023993	 "VehicleNumber": "3187"	 "Time": "2022-02-27 18:08:37"	 "Lat": 52.199135
 "Brigade": "014"}	 {"Lines": "4"	 "Lon": 21.023993	 "VehicleNumber": "3187"	 "Time": "2022-02-27 18:08:58"	 "Lat": 52.199135
 "Brigade": "014"}	 {"Lines": "4"	 "Lon": 21.023638	 "VehicleNumber": "3187"	 "Time": "2022-02-27 18:09:30"	 "Lat": 52.20138
 "Brigade": "014"}	 {"Lines": "4"	 "Lon": 21.023401	 "VehicleNumber": "3187"	 "Time": "2022-02-27 18:10:07"	 "Lat": 52.202915
 "Brigade": "014"}	 {"Lines": "4"	 "Lon": 21.022938	 "VehicleNumber": "3187"	 "Time": "2022-02-27 18:10:38"	 "Lat": 52.20531
 "Brigade": "014"}	 {"Lines": "4"	 "Lon": 21.022818	 "VehicleNumber": "3187"	 "Time": "2022-02-27 18:10:59"	 "Lat": 52.20586
 "Brigade": "014"}	 {"Lines": "4"	 "Lon": 21.021458	 "VehicleNumber": "3187"	 "Time": "2022-02-27 18:11:30"	 "Lat": 52.20925

______________________________________________________________

PYTANIA I ODPOWIEDZI:

Z czego wynikaj¹ rozbie¿noœci pomiêdzy kolejnymi wys³anymi sygna³ami GPS wys³anymi przez pojazdy? Wed³ug dokumentacji rozdzielczoœæ czasowa danych to 10 sekund. W rzeczywistoœci te odstêpy s¹ bardzo ró¿ne, a wielokrotnie zdarzaj¹ siê odstêpy kilkuminutowe. Te sytuacje mo¿na by by³o wyt³umaczyæ brakiem sygna³u GPS w okreœlonych momentach, gdyby te luki wystêpowa³y tylko dla atrybutu GPS_received, ale w takiej sytuacji interwa³ w GPS_sent powinien byæ zawsze taki sam – 10 sekund.

Opiszê schemat gromadzenia danych. Dane z pojazdów s¹ przesy³ane do serwera agreguj¹cego dane (ju¿ zawieraj¹ timestamp GPS). Nastêpnie nasz mechanizm odpytuje serwer agreguj¹cy co 10 sekund. St¹d czas odczytu bêdzie zró¿nicowany a nie wielokrotnoœci¹ 10 sekund.

2.	Wprawdzie trafi³ siê tylko jeden przypadek, ale sk¹d siê bior¹ braki przypisanej brygady do rekordu danych?

Problem danych Ÿród³owych z pojazdu. Na szczêœcie niezbyt czêsto wystêpuj¹cy.

3.	Przepraszam, ale nie do koñca rozumiem. Z jak¹ czêstotliwoœci¹ w takim razie dane s¹ wysy³ane z pojazdów na serwer? Czy je¿eli Pañstwa mechanizm odpytuje serwer co 10 sekund, to w atrybucie GPS_received odstêpy nie powinny wynosiæ 10 sekund? Zmierzam do tego, ¿e nieregularnoœæ w odstêpach dotyczy zarówno GPS_sent, jak i GPS_received. No i sk¹d siê bior¹ te kilkuminutowe luki (zdarzaj¹ siê równie¿ w trakcie kursów, a wiêc to nie jest kwestia oczekiwania na przystanku koñcowym/pocz¹tkowym)?

W danych o ile pamiêtam by³ jeden parametr dotycz¹cy czasu i dotyczy on czasu rejestracji lokalizacji pojazdu.

______________________________________________________________

POZOSTA£E USTALENIA…

System licz¹cy relacjê pojazdu do rozk³adu, czyli to na wyœwietlaczach obok kierowcy (o czym ostatnio wspomina³em), to jest wewnêtrzny system pojazdu. Kierowca wklepuje na samym pocz¹tku trasê, jak¹ bêdzie w³aœnie jecha³ (jeszcze na pêtli). Pojazd liczy tylko przejechany dystans, a informacja o odleg³oœciach miêdzy przystankami jest zapisana jako trasa, czyli w ogóle nie ma tutaj pozycjonowania satelitarnego.
Rozwi¹zanie zagadki zwi¹zanej z brakuj¹cym atrybutem identyfikatora pojazdu (numer boczny) dla danych wrzeœniowych – ten atrybut zacz¹³ byæ udostêpniany dopiero niedawno, czyli ju¿ po wrzeœniu 2020. Dane historyczne nie bêd¹ w takim razie tego atrybutu mia³y, a to uniemo¿liwia w zasadzie jednoznaczn¹ identyfikacjê pojazdu (aktualnie ustalam, kiedy ta zmiana mia³a miejsce).
W ramach transportu miejskiego jest wielu przewoŸników, g³ówny to MZA, poza tym Tramwaje Warszawskie, Mobilis, Arriva…
Dane przez sieæ komórkow¹ z pojazdów trafiaj¹ na serwery przewoŸników, póŸniej do ZTM, gdzie s¹ agregowane, nastêpnie do Urzêdu Miasta i dopiero do API. Du¿o rzeczy po drodze mo¿e pójœæ nie tak i st¹d dziury w danych.
Ka¿dy z tych przewoŸników gromadzi inne dane, ale jak to póŸniej udostêpnia zbiorczo ZTM, to jakby równaj¹ w dó³, czyli udostêpniaj¹ takie dane, które maj¹ wszyscy. Poszczególni przewoŸnicy mog¹ mieæ bardziej szczegó³owe dane – wiêcej atrybutów.
https://www.ztm.waw.pl/statystyki/ >> tam na przyk³ad informacje o aktualnej liczbie pojazdów.
Za 1-2 lata (licz¹c od wrzeœnia 2020) chcieliby ju¿ mieæ informacjê o przybyciu pojazdu na konkretny przystanek.

