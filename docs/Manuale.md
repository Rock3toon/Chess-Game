# **MANUALE UTENTE**


## **INDICE**
1. [Introduzione](#1-introduzione)
2. [Regolamento degli Scacchi](#2-regolamento-degli-scacchi) <br/>
    2.1 [Movimenti dei pezzi](#-21-movimenti-dei-pezzi) <br/>
    2.2 [Regole Speciali](#-22-regole-speciali) <br/>
    2.3 [Scopo del gioco](#-23-scopo-del-gioco) <br/>
    2.4 [Esiti della partita](#-24-esiti-della-partita) <br/>
3. [Procedura preliminare](#3-procedura-preliminare) <br>
    3.1 [Creazione Token per il Docker login](#31-creazione-token-per-il-docker-login) <br/>
    3.2 [Docker Login con GitHub Access Token](#32-docker-login-con-github-access-token) <br/>
4. [Avvio applicazione](#4-avvio-applicazione) 
5. [Guida ai comandi](#5-guida-ai-comandi) <br/>
    5.1 [Help](#51-help) <br/>
    5.2 [Gioca](#52-gioca) <br/>
    5.3 [Scachiera](#53-scacchiera) <br/>
    5.4 [Mosse](#54-mosse) <br/>
    5.5 [Abbandona](#55-abbandona) <br/>
    5.6 [Patta](#56-patta) <br/>
    5.7 [Esci](#57-esci) <br/>



## ***1) Introduzione***
♟️Benvenuti nell’universo degli **Scacchi**!
In questo documento troverete una guida completa per immergervi nell'arte degli scacchi: dalle regole fondamentali fino ai principi strategici più raffinati. Gli scacchi sono molto più di un semplice gioco da tavolo, sono una battaglia mentale dove intuizione, logica e previsione si intrecciano a ogni mossa.
Che tu sia un principiante curioso o un giocatore esperto in cerca di perfezionare il tuo stile, questa guida ti accompagnerà passo dopo passo in questa esperienza.


## ***2) Regolamento degli scacchi***
Il gioco degli **Scacchi** si svolge tra due giocatori che muovono pezzi di diverso colore (bianco e nero) su una scacchiera quadrata di 64 caselle alternate nei colori chiaro e scuro.
### ♔ <ins>*La scacchiera e i pezzi*</ins>
La scacchiera viene disposta in modo che la casella d'angolo a destra di ciascun giocatore sia bianca
Ogni giocatore ha a disposizione 16 pezzi: *1 Re, 1 Donna (Regina), 2 Torri, 2 Alfieri, 2 Cavalli e 8 Pedoni*.
La posizione iniziale vede i pezzi disposti nelle due traverse più vicine al giocatore.
<div align="center">  
  <img src="img/Disposizione_Iniziale.png">
</div><br/>

### 🔀 2.1) Movimenti dei pezzi
***Re***: Può muoversi di una posizione dalla casa in cui si trova in qualsiasi direzione. Purchè non sia sotto scacco o la posizione di arrivo sia sotto attacco.<br>
<div align="left">  
  <img src="img/Movimento_Re.png">
</div><br/>

***Donna***: Può muoversi di un qualsiasi numero di posizioni e in tutte le direzioni.<br>
<div align="left">  
  <img src="img/Movimento_Donna.png">
</div><br/>

***Torre***: Può muoversi di un qualsiasi numero di posizioni e solamente in direzione orizzontale o verticale.<br>
<div align="left">  
  <img src="img/Movimento_Torre.png">
</div><br/>

***Alfiere***: In base alla sua casa di partenza (Bianco o Nero) può muoversi in diagonale di un qualsiasi numero di posizioni rimanendo ovviamente sul suo colore di partenza.<br>
<div align="left">  
  <img src="img/Movimento_Alfiere.png">
</div><br/>

***Cavallo***: Può muoversi a "L" ovvero può spostarsi di due posizioni in orizzontale o verticale e successivamente di una posizione perpendicolare (movimento ortogonale).<br>

<div align="left">  
  <img src="img/Movimento_Cavallo.png">
</div><br/>

***Pedone***: Può muoversi avanzando verticalmente di una sola casella, due solamente se è la prima mossa di quel pedone. Il pedone ha la facoltà di catturare solo in diagonale.<br>

<div align="left">
  <img src="img/Movimento_Pedone.png">
</div><br/>

**<ins>Movimento del Pedone dalla casa di partenza.</ins>**
<div align="left">
  <img src="img/Movimento_Pedone_Partenza.png">
</div><br/>

**<ins>Cattura del Pedone.</ins>**
<div align="left">  
  <img src="img/Cattura_Pedone.png">
</div><br/>

Il pedone **non può** muoversi all'indietro.
<div align="left">  
  <img src="img/Errore_Movimento_Pedone.png">
</div><br/>

### 📖 2.2) Regole speciali
***Arrocco***: L'arrocco coinvolge il Re e una delle sue due Torri e può essere di due tipi Lungo (0-0-0) o Corto (0-0). L'arrocco si può eseguire solo a determinate condizioni: <br>
Re e Torre **non si sono mai mossi**, le case su cui si muoverà il Re non devono essere occupate e non devono essere sotto attacco e il Re nella sua casa di partenza non deve essere sotto scacco. L'arrocco è una particolare mossa che permette di mettere al sicuro il proprio Re, solo in questo caso il re ha la facoltà di spostarsi di due case e saltare la propria Torre.<br>
<ins>**Arrocco Lungo (0-0-0)**</ins>
<div align="left">  
  <img src="img/Arrocco1.png">
</div><br/>

<div align="left">  
  <img src="img/Arrocco2.png">
</div><br/>

<ins>**Arrocco corto (0-0)**</ins>
<div align="left">  
  <img src="img/Arrocco3.png">
</div><br/>

<div align="left">  
  <img src="img/Arrocco4.png">
</div><br/>

***En passant***: Avviene solo se un pedone avversario avanza di due caselle dalla sua posizione iniziale (cioè dalla seconda alla quarta traversa) e si posiziona accanto a un tuo pedone (nella colonna adiacente). Il pedone può quindi catturarlo come se si fosse mosso di una sola posizione.<br>
<div align="left">  
  <img src="img/En-passant1.png">
</div><br/>

<div align="left">  
  <img src="img/En-passant2.png">
</div><br/>

***Promozione***: quando un pedone raggiunge l'ottava traversa (per il Bianco) o la prima traversa (per il Nero), deve essere promosso (sostituito) a un altro pezzo. La promozione è obbligatoria e avviene immediatamente. I pezzi disponibili alla promozione sono:<br>
Donna (**D**), Torre (**T**), Alfiere (**A**), Cavallo (**C**).
<div align="left">  
  <img src="img/Promozione1.png">
</div><br/>

<div align="left">  
  <img src="img/Promozione2.png">
</div><br/>

### 🎯 2.3) Scopo del gioco
L'obiettivo degli **Scacchi** è chiaro: mettere in scacco matto il re avversario, ovvero attaccarlo in una posizione da cui non può più fuggire o essere protetto legalmente. Due giocatori si alternano mossa dopo mossa, per cercare di controllare il centro della scacchiera, sviluppare i propri pezzi e mettere in difficoltà l'avversario.

### 🏆 2.4) Esiti della partita
La partita termina quando uno dei due re viene messo in **scacco matto**.
Tuttavia, il gioco può anche finire in patta, stallo, abbandono o per mancanza di pezzi..<br>
***Patta:*** Un giocatore può offrire *patta* all’avversario **<ins>all'inizio del proprio turno<ins>**. Se il giocatore avversario accetta, la partita termina in parità.<br>
***Stallo:*** Il giocatore di turno non è sotto scacco ma non ha a disposizione mosse legali da poter effettuare, la partita termina automaticamente in parità.<br>
***Abbandono:*** Un giocatore durante <ins>il proprio turno</ins> decide volontariamente di rinunciare alla partita ritirandosi, riconoscendo la propria sconfitta. Al giocatore avversario viene riconosciuta la vittoria della partita.<br>
***Mancanza di Pezzi:*** La partita può terminare automaticamente in parità (patta) se nessuno dei due giocatori dispone più del materiale sufficiente per dare scacco matto. I casi in cui avviene questa condizione sono: <br>
**Re vs Re**, **Re + Cavallo vs Re**, **Re + Alfiere vs Re**, **Re + Alfiere vs Re + Alfiere** (solo se entrambi gli alfieri si trovano su case dello stesso colore)

Per arrivare alla vittoria servono visione strategica, pianificazione accurata e la capacità di anticipare le intenzioni dell'avversario. Ogni mossa conta, e un singolo errore può cambiare le sorti dell'intera partita.

## ***3) Procedura preliminare***
Prima di poter avviare il gioco bisogna essere sicuri di trovarsi in un ambiente che permette la
sua esecuzione, per questo lasciamo una guida completa di tutti i passaggi preparatori:

- Come prima cosa bisogna installare l'applicazione [Docker Desktop](https://www.docker.com/products/docker-desktop/) e verificarne la corretta installazione
- Autenticarsi su Docker con github access token tramite CLI come segue:

### 3.1) Creazione Token per il Docker login


Verificare di utilizzare uno dei terminali supportati, riportati nel file Report alla voce Requisiti Non Funzionali

Per ottenere un token per l'accesso alle risorse di GitHub, segui i passaggi descritti di seguito:

1. **Registrazione**: Se non hai già un account, [registrati su GitHub](https://github.com/join) per ottenere un account.

2. **Accesso**: Accedi al tuo account GitHub utilizzando le tue [credenziali di accesso](https://github.com/login).


3. **Generazione del token**: Una volta effettuato l'accesso, vai alle impostazioni del tuo account. Puoi accedervi cliccando sulla tua immagine del profilo e selezionando `Settings`.
   Nella sezione `Developer settings`, seleziona `Personal access tokens` dal menu a sinistra.


4. **Generazione**: Fai clic sul pulsante `Generate new token`


5. **Autorizzazioni**: Seleziona le autorizzazioni necessarie per il token.


6. **Copia il token**: Una volta generato, copia il token. GitHub mostrerà il token solo una volta, quindi assicurati di copiarlo e conservarlo in un luogo sicuro.

A questo punto si è pronti per accedere a Docker tramite Github PAT

### 3.2) Docker Login con GitHub Access Token

1. **Copia del token su un file `.txt`**:

   Copia il token generato in precedenza in un file di testo, ad esempio, `token.txt`


2. **Ottenere il percorso del file**:

   Dopo aver creato il file, copia il percorso completo


3. **Login a GitHub Container Registry (GHCR) tramite Docker**:

   Apri il terminale come amministratore ed esegui il seguente comando, sostituendo `PATH_DEL_TOKEN` con il percorso copiato e `USERNAME` con il tuo nome utente GitHub:

```bash
cat "PATH_DEL_TOKEN/token.txt" | docker login ghcr.io -u "USERNAME" --password-stdin
```
4. **Scaricare l'immagine tramite Docker Pull**:

   Una volta effettuato l'accesso con successo, puoi scaricare l'immagine Docker desiderata con il seguente comando:

```shell
docker pull ghcr.io/softeng2425-inf-uniba/scacchi-naur:latest
```
5. **Esecuzione del container Docker**:
   Una volta eseguito l'accesso e scaricata l'immagine con successo, puoi eseguire l'immagine Docker desiderata con
   il seguente comando:
```shell
docker run --rm -it ghcr.io/softeng2425-inf-uniba/scacchi-naur:latest
```
Questo comando avvierà il gioco **Scacchi**
## ***4) Avvio applicazione***
All'avvio dell'applicazione viene mostrato in grande il titolo "**SCACCHI**" insieme a dei messaggi di benvenuto. 

<div align="center">  
  <img src="img/Intro.png">
</div><br/>

Viene successivamente invitato l'utente a premere un qualsiasi tasto per continuare.
Se l'applicazione viene avviata insieme ai flag `-h` o `--help` viene mostrato prima della schermata di benevenuto l'elenco dei comandi:
riassuntivo se il flag inserito è `-h`, esteso se il flag inserito è `--help`.

## ***5) Guida ai comandi***
Per avviare il gioco degli **Scacchi**, seguite le istruzioni riportate di seguito in base al tipo di esecuzione desiderata.
### 5.1) Help
Il comando `/help` mostra la guida di base del gioco degli **Scacchi**, visualizzando come muovere i pezzi, il formato delle mosse e i comandi disponibili nel gioco 
### 5.2) Gioca
Tramite comando `/gioca` la partita viene avviata e viene mostrata a schermo la scacchiera nella sua configurazione iniziale.
### 5.3) Scacchiera
Tramite comando `/scacchiera` viene mostrata a schermo la scacchiera con le posizioni dei pezzi attuali.
### 5.4) Mosse
Tramite comando `/mosse` viene mostrato lo storico di tutte le mosse effetuate.
### 5.5) Abbandona
Tramite comando `/abbandona` viene chiesto all'utente la conferma di abbandono e in caso affermativo la partita viene terminata.
Se si utilizza il comando `/abbandona` a partita non avviata verrà mostrato messaggio di errore.
### 5.6) Patta
Tramite comando `/patta` viene chiesto all'utente la conferma di richiesta della patta e in caso affermativo viene richiesto all'altro giocatore di accettare o rifiutare la patta. In caso affermativo la partita termina in **patta** in caso negativo la partita prosegue.
Se si utilizza il comando `/patta` a partita non avviata verrà mostrato messaggio di errore.
### 5.7) Esci
Tramite comando `/esci` viene chiesto all'utente la conferma di chiusura dell'applicazione e in caso affermativo l'applicazione viene terminata restituendo il potere al sistema operativo.
