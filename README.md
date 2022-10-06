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
