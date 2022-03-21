Modelowanie op�nie� transportu miejskiego

Projekt z pogranicza Data Science i System�w informacji Przestrzennej (GIS). Wiele miast, w tym Warszawa, udost�pnia dane dotycz�ce transportu miejskiego. Najistotniejszym elementem s� logi pozycyjne (czas wys�ania/odebrania sygna�u GNSS oraz aktualne wsp�rz�dne). Na ich podstawie mo�na modelowa� przemieszczanie si� pojazd�w komunikacji miejskiej (tramwaj�w, autobus�w). 

Wzbogacaj�c te logi o dodatkowe dane z portalu Dane po Warszawsku, m. in. dane przystankowe, o brygadach, pojazdach we flocie, a tak�e G��wnego Urz�du Statystycznego (g�sto�� zaludnienia, struktura spo�eczna), Geoportalu (formy u�ytkowania terenu, budynki), serwis�w pogodowych, informacji o nat�eniu ruchu (korkometr); jeste�my w stanie zbudowa� model przewiduj�cy op�nienia na wybranych trasach w okre�lonych warunkach. 

Urz�d Miasta by�by zapewne zainteresowany wsp�prac�. Wynika naszych analiz pozwol� im na dopasowanie rozk�ad�w jazdy do faktycznych warunk�w na drogach. Poza tym, analizuj�c struktur� demograficzn� r�nych cz�ci Warszawy, mo�liwe b�dzie wyci�gni�cie wniosk�w na temat tego, gdzie nale�a�oby zwi�kszy�, a gdzie zmniejszy� cz�stotliwo�� kursowania pojazd�w lub wr�cz zaprojektowa� nowe linie.

Opr�cz zada� zwi�zanych czysto z modelowaniem, projekt b�dzie wymaga� kilku przemy�le� na poziomie koncepcyjnym, np. jak wyekstrapolowa� z danych (logi z pozycj� co 30 sekund lub mniej) moment, w kt�rym pojazd pojawia si� na przystanku? Poza tym trzeba b�dzie opracowa� efektywny spos�b mapowania pozycji z log�w na wektorowe wersje tras przejazdu poszczeg�lnych linii (systemy pozycjonowania charakteryzuj� nawet kilkunastometrowymi b��dami, zw�aszcza w okolicy wysokiej zabudowy).

Wyzwaniem w przypadku tego projektu b�dzie na pewno obj�to�� danych. Logi samych tramwaj�w z jednego miesi�ca to prawie 1 GB danych. Wydaje si�, �e pocz�tkowo nale�a�oby si� skupi� na kilku wybranych trasach i pozyska� dane historyczne, np. z 3 lat (zak�adam, �e jest to mo�liwe, ale musia�bym dopyta� ludzi z Warszawskiego Transportu Publicznego). D�u�szy zakres dat pozwoli z jednej strony na wy�apanie sezonowych trend�w, ale z drugiej strony powoduje na przyk�ad ryzyko wyst�pienia zmian w rozk�adach konkretnej linii.

______________________________________________________________

Pr�bka danych (tramwaje z jednego dnia) � dost�pne w folderze trams_September2020 
>> brak numeru bocznego pojazdu:

Column1	line_number	brigade	latitude	longitude	GPS_sent	GPS_received
4	4	3	21.025087	52.296046999999994	01.09.2020 21:30:51	01.09.2020 21:31:01
6	4	3	21.025719	52.295193	01.09.2020 21:31:01	01.09.2020 21:31:14
8	4	6	21.024124	52.19627	01.09.2020 22:31:17	01.09.2020 22:31:24
9	4	13	21.021442	52.177704	01.09.2020 19:30:46	01.09.2020 19:31:00
10	4	1	21.022382999999998	52.264034	01.09.2020 21:31:03	01.09.2020 21:31:14

______________________________________________________________

Obecna pr�bka danych � do pozyskania za pomoc� skryptu korzystaj�cego z API 
>> s� ju� numery boczne pojazdu:

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

Z czego wynikaj� rozbie�no�ci pomi�dzy kolejnymi wys�anymi sygna�ami GPS wys�anymi przez pojazdy? Wed�ug dokumentacji rozdzielczo�� czasowa danych to 10 sekund. W rzeczywisto�ci te odst�py s� bardzo r�ne, a wielokrotnie zdarzaj� si� odst�py kilkuminutowe. Te sytuacje mo�na by by�o wyt�umaczy� brakiem sygna�u GPS w okre�lonych momentach, gdyby te luki wyst�powa�y tylko dla atrybutu GPS_received, ale w takiej sytuacji interwa� w GPS_sent powinien by� zawsze taki sam � 10 sekund.

Opisz� schemat gromadzenia danych. Dane z pojazd�w s� przesy�ane do serwera agreguj�cego dane (ju� zawieraj� timestamp GPS). Nast�pnie nasz mechanizm odpytuje serwer agreguj�cy co 10 sekund. St�d czas odczytu b�dzie zr�nicowany a nie wielokrotno�ci� 10 sekund.

2.	Wprawdzie trafi� si� tylko jeden przypadek, ale sk�d si� bior� braki przypisanej brygady do rekordu danych?

Problem danych �r�d�owych z pojazdu. Na szcz�cie niezbyt cz�sto wyst�puj�cy.

3.	Przepraszam, ale nie do ko�ca rozumiem. Z jak� cz�stotliwo�ci� w takim razie dane s� wysy�ane z pojazd�w na serwer? Czy je�eli Pa�stwa mechanizm odpytuje serwer co 10 sekund, to w atrybucie GPS_received odst�py nie powinny wynosi� 10 sekund? Zmierzam do tego, �e nieregularno�� w odst�pach dotyczy zar�wno GPS_sent, jak i GPS_received. No i sk�d si� bior� te kilkuminutowe luki (zdarzaj� si� r�wnie� w trakcie kurs�w, a wi�c to nie jest kwestia oczekiwania na przystanku ko�cowym/pocz�tkowym)?

W danych o ile pami�tam by� jeden parametr dotycz�cy czasu i dotyczy on czasu rejestracji lokalizacji pojazdu.

______________________________________________________________

POZOSTA�E USTALENIA�

System licz�cy relacj� pojazdu do rozk�adu, czyli to na wy�wietlaczach obok kierowcy (o czym ostatnio wspomina�em), to jest wewn�trzny system pojazdu. Kierowca wklepuje na samym pocz�tku tras�, jak� b�dzie w�a�nie jecha� (jeszcze na p�tli). Pojazd liczy tylko przejechany dystans, a informacja o odleg�o�ciach mi�dzy przystankami jest zapisana jako trasa, czyli w og�le nie ma tutaj pozycjonowania satelitarnego.
Rozwi�zanie zagadki zwi�zanej z brakuj�cym atrybutem identyfikatora pojazdu (numer boczny) dla danych wrze�niowych � ten atrybut zacz�� by� udost�pniany dopiero niedawno, czyli ju� po wrze�niu 2020. Dane historyczne nie b�d� w takim razie tego atrybutu mia�y, a to uniemo�liwia w zasadzie jednoznaczn� identyfikacj� pojazdu (aktualnie ustalam, kiedy ta zmiana mia�a miejsce).
W ramach transportu miejskiego jest wielu przewo�nik�w, g��wny to MZA, poza tym Tramwaje Warszawskie, Mobilis, Arriva�
Dane przez sie� kom�rkow� z pojazd�w trafiaj� na serwery przewo�nik�w, p�niej do ZTM, gdzie s� agregowane, nast�pnie do Urz�du Miasta i dopiero do API. Du�o rzeczy po drodze mo�e p�j�� nie tak i st�d dziury w danych.
Ka�dy z tych przewo�nik�w gromadzi inne dane, ale jak to p�niej udost�pnia zbiorczo ZTM, to jakby r�wnaj� w d�, czyli udost�pniaj� takie dane, kt�re maj� wszyscy. Poszczeg�lni przewo�nicy mog� mie� bardziej szczeg�owe dane � wi�cej atrybut�w.
https://www.ztm.waw.pl/statystyki/ >> tam na przyk�ad informacje o aktualnej liczbie pojazd�w.
Za 1-2 lata (licz�c od wrze�nia 2020) chcieliby ju� mie� informacj� o przybyciu pojazdu na konkretny przystanek.

