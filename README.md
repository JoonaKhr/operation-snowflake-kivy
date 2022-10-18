# Operation Snowflake with Kivy ![A1](https://github.com/JoonaKhr/operation-snowflake-kivy/blob/master/resources/imgs/A1.png)
Projektin tavoite olisi saada luotua peli, jossa painellaan ruudulle ilmestyviä lumihiutaleita, joita on kahdessa eri koossa merkiten paljonko niistä saa pisteistä.

Pelin olisi tarkoitus toimia niin tietokoneella kuin mobiilillakin kivyn ansiosta ja tulokset pitäisi lähteä nettiin mongoDB:hen ja tulla myös sieltä pelissä olevaan
pistetaulukkoon.

Asiakasvaatimuksina olisi, että peliä pelatessa saa pisteitä,  jotka tallennetaan tietokantaan ja ne voi nähdä pelin sisällä herättäen kilpaisullisuutta
Pelaaja tahtoo nähdä itsensä parempana kuin kaverinsa joten vertaa omia pisteitään kavereiden pisteisiin

Pythonilla rakennettava logiikka ja kivyllä rakennettava käyttöliittymä, mongoDB tietokantana

Testaan sitä manuaalisesti toimintoja tehdessä, en tiedä voiko sitä miten hyvin automatisoida. MongoDB yhteyttä kai voinee testata automaattisesti

Ensimmäiset pari viikkoa menee kivyn UI rakentamisen opettelemiseen, jonka jälkeen alan työstämään logiikkaa tämän ympärille.

Työskentelen suurimmaksi osaksi kahden kaverini kanssa puhelussa discordin kautta jakaen ruutuani, jotta he voivat katsoa mitä teen.

## Päiväkirja
20.9.-27.9. Pelin ulkoasun tekemisen aloittaminen, painikkeita ja pisteteksti. Start Game painike, joka aloittaa ajastimen ja ajastimen loputtua ajastin sulkee itsensä.
Tein myös Screen Managerin, jossa on pelinäkymä, asetukset ja pistetilastot, mutta en ehtinyt saada niihin siirtymistä toimimaan tämän viikon aikana. Seuraavan viikon tavoite on saada Screen Manager toimimaan ja siistiä vähän ongelmia, huomasin Start Game painiketta painaessa useamman kerran sen käynnistävän ajastimia, jotka tekevät pelistä huomattavasti vaikeamman.

28.9.-5.10. Start Game on nyt toggle eikä ajastimia voi laittaa päällekkäin, jotta pelisessioita ei voi aloittaa montaa päällekkäin. Sain Screen Managerin toimimaan, jotta asetuksiin ja pistetilastoihin pääsee vaikka niissä ei toistaiseksi muuta olekaan kuin vain nappi takaisin pelinäkymään. Myös ensimmäinen kuva tuli piirrettyä ruudulle, mutta en ole vielä keksinyt miten saisin niitä tulemaan satunnaisiin kohtiin ruudulla, joka onkin minun seuraavan viikon tavoite, jos ehdin sen saada toimimaan ajoissa niin siirryn tekemään niistä painettavia, jotta niistä saisi pisteitä ja näin peli olisi teknisesti pelattavassa vaiheessa. Pitää myös tehdä asetus ja pistetaulukko näkymän napit toimimattomiksi pelinkulun aikana.

6.10.-11.10 Lumihiutaleiden satunnainen kutsuminen pelialueelle toimii onnistuneesti, niitä tulee nyt joka sekunti mitä peli on päällä. Laitoin myös peliin omaa grafiikkaa nappeihin ja myöhemmin päivitän lumihiutaleet uusiksi, kun saan tehtyä tai löydettyä jostain grafiikkaa minkä varmasti omistan. Asetukset ja tilastot napit menevät nyt myös pois päältä, kun käynnistät pelin ettet paina itseäsi vahingossa pois pelistä kierroksen aikana. Peli nyt myös säilyttää vain maksimissaan viittä hiutaletta ruudulla. 12.10.-18.10. välin aion käyttää pelilogiikan rakentamiseen, jotta lumihiutaletta painaessa saat pisteen ja se häviää ruudulta. Painaessasi yhden pois se kutsuu uuden tilalle, jotta pelaajat voivat oikeasti kilpailla nopeudesta, jos saan nämä tehtyä niin jatkosuunnitelmana olisi siistiä koodia ja/tai lisätä äänet nappeihin jne. 

12.10.-18.10. Lumihiutaleen painaminen nyt antaa pisteen, poistaa painetun yksikön, kutsuu uuden tilalle ja toistaa äänen. Muutkin ohjelman painikkeet pitää nyt äänen. Yritin saada pelinsisäistä ääniliukuria toimimaan, mutta se oli vähän monimutkaisempaa kuin kuvittelin, joten en saanut sitä toimimaan ja aion hyllyttää tämän idean toistaiseksi ja rakentaa tärkeämmät ominaisuudet ensin. Ensi viikon aion keskittää pistetilastojen tekemiseen eli pelin tulisi, joko erän jälkeen kysyä nimi tai teen asetusnäkymään tai asetusnäppäimen tilalle tekstikentän mihin voi kirjoittaa ja erän jälkeen kysytään haluatko lähettää tulokset nettiin. Jos ehdin saada nämä valmiiksi niin yritän saada pistetilastonäkymän näyttämään nämä viisi parasta tulosta kaikkien nimien kesken ja valinnaisesti tietyn nimen perusteella viisi parasta.
