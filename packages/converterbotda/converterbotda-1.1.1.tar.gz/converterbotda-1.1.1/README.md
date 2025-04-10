# BOTDA-converter

## Installazione

Per installare il pacchetto, da terminale nella cartella che contiene il file wheel:

```cmd
pip install \converterbotda-1.0.0-py3-none-any.whl
```

modificando opportunamente la versione nel nome del file.

Opzionalmente, da terminale:

```cmd
botda-converter --install-completion
```

## Command line interface

I comandi disponibili da command prompt sono:

* `botda-converter`
* `botda-converter batch`
* `botda-converter profile`
* `botda-converter raw`
* `botda-converter split`

Di seguito le descrizioni dei singoli comandi.

### `botda-converter`

**Utilizzo**:

```console
$ BOTDA-converter [OPTIONS]
```

**Opzioni**:

* `--filename TEXT`
* `--folder TEXT`
* `--range <INT INT>...`: in campioni, per esempio `--range 20 800` [default: 0, fine fibra]
* `--statistics / --no-statistics`: [default: statistics]
* `--correlations / --no-correlations`: [default: correlations]
* `--help`: Show this message and exit.

**Descrizione**:

Se presenti, vengono convertiti i files nelle sottocartelle `rawarray` e `rawmatrix`. Se la `folder` non è specificata allora viene considerata la cartella corrente da cui è eseguito il comando.
Il parametro `filename` viene utilizzato come radice comune. Per esempio, con `--filename ku23_1` i files risultanti saranno `ku23_1_profile.h5` e `ku23_1_raw.h5`. Se desiderato, deve contenere anche il path relativo altrimenti i files verranno creati nella cartella di lavoro corrente, *non* nella cartella che contiene le sottocartelle `rawarray` e `rawmatrix`.
Se `statistics` allora vengono calcolate la stima BFS media e sua deviazione standard e curva massimi di guadagno Brillouin media e sua deviazione standard.
Se `correlations` allora vengono calcolate anche statistiche relative alla stabilità nel tempoc del profilo BFS e curva dei massimi; in questo caso è altamente consigliato indicare anche l'opzione `--range` indicando l'inizio e la fine *in campioni* della tratta significativa di fibra, in modo da escludere in particolare l'inizio e la fine della fibra la cui variabilità casuale priverebbe di senso le correlazioni calcolate.

### `botda-converter batch`

**Utilizzo**:

```console
$ botda-converter batch [OPTIONS] BATCH_INFO_FILENAME
```

**Argomenti**:

* `BATCH_INFO_FILENAME`: [required]

**Opzioni**:

* `--help`: Show this message and exit.

**Descrizione**:

Conversione batch di più cartelle. Le cartelle sono definite in `BATCH_INFO_FILENAME` che deve essere un file json così strutturato:

```json
"entries":
    [
        {
            "folder":"ku23_1/fibra01/110mA",
            "range":[25,1110]
        },
        {
            "folder":"ku23_1/fibra1/120mA",
            "range":[25,1110]
        },
        {
            "folder":"ku23_1/fibra2/110mA",
            "range":[25,845]
        },
    ]
}
```

dove il campo `range` è facoltativo ed utilizzato per calcolare le statistiche (BFS medio e deviazione standard). I numeri sono interi e rappresentano gli indici del vettore BFS. I path indicati in `folder` devono contenere la cartella `rawarray` e/o `rawmatrix`. All'interno dei path verranno generati i files `profile.h5` e `raw.h5`.

### `botda-converter profile`

**Utilizzo**:

```console
$ botda-converter profile [OPTIONS] FILENAME
```

**Argomenti**:

* `FILENAME`: [required] Target filename (ex: `rawarray.h5`), compreso il path relativo.

**Opzioni**:

* `--folder TEXT`
* `--range <INT INT>...`
* `--statistics / --no-statistics`: [default: statistics]
* `--correlations / --no-correlations`: [default: correlations]
* `--help`: Show this message and exit.

**Descrizione**:

Comando per convertire i files `rawarray` contenenti i profili BFS. Il nome del file deve essere fornito ed essere `*.h5`. Se la `folder` non è specificata allora viene considerata la cartella corrente da cui è eseguito il comando o la sottocartella `rawarray`, se presente.
Se `statistics` allora vengono calcolate la stima BFS media e sua deviazione standard e curva massimi di guadagno Brillouin media e sua deviazione standard.
Se `correlations` allora vengono calcolate anche statistiche relative alla stabilità nel tempoc del profilo BFS e curva dei massimi; in questo caso è altamente consigliato indicare anche l'opzione `--range` indicando l'inizio e la fine *in campioni* della tratta significativa di fibra, in modo da escludere in particolare l'inizio e la fine della fibra la cui variabilità casuale priverebbe di senso le correlazioni calcolate.

### `botda-converter raw`

**Utilizzo**:

```console
$ botda-converter raw [OPTIONS] FILENAME
```

**Argomenti**:

* `FILENAME`: [required]

**Opzioni**:

* `--folder TEXT`
* `--help`: Show this message and exit.

**Descrizione**:

Comando per convertire i files `rawmatrix` contenenti i dati raw BGS. Il nome del file deve essere fornito ed essere `*.h5`. Se la `folder` non è specificata allora viene considerata la cartella corrente da cui è eseguito il comando o la sottocartella `rawmatrix`, se presente.

### `botda-converter split`

**Utilizzo**:

```console
$ botda-converter split [OPTIONS] FILENAME
```

**Argomenti**:

* `FILENAME`: [required]

**Opzioni**:

* `--size`: Dimensione massima (approssimativa) dei files generati, in megabytes. [default: 100 MB]

**Descrizione**:

Divide un singolo file h5 (`raw` o `profile`) in files più piccoli, nella stessa cartella contenente il file originale. Nel caso di `profile`, se le statistiche sono presenti, queste sono semplicemente ricopiate in tutti i files; *non* vengono ricalcolate media e deviazione standard sulle sole misure contenute nel file più piccolo.

## TODO

- [ ] build in repo: https://github.com/python-poetry/poetry/issues/366
