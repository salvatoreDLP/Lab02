def carica_da_file(file_path):
    album = []

    try:
        file = open(file_path, "r", encoding="utf-8")
        righe = file.readlines()
        file.close()
    except FileNotFoundError:
        return None

    for riga in righe[1:]:
        riga = riga.strip()

        if riga == "":
            continue

        dati = riga.split(",")

        codice = dati[0].strip()
        titolo = dati[1].strip()
        autore = dati[2].strip()
        mese = int(dati[3].strip())
        anno = int(dati[4].strip())

        foto = [codice, titolo, autore, mese, anno]

        gruppo_anno = None

        for gruppo in album:
            if gruppo[0] == anno:
                gruppo_anno = gruppo
                break

        if gruppo_anno is None:
            gruppo_anno = [anno, []]
            album.append(gruppo_anno)

        gruppo_anno[1].append(foto)

    return album


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    if mese < 1 or mese > 12:
        return None

    # controllo se il codice esiste gia
    for gruppo in album:
        for foto in gruppo[1]:
            if foto[0] == codice:
                return None

    try:
        file = open(file_path, "r", encoding="utf-8")
        file.close()
    except FileNotFoundError:
        return None

    nuova_foto = [codice, titolo, autore, mese, anno]

    try:
        file = open(file_path, "a", encoding="utf-8")
        file.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
        file.close()
    except FileNotFoundError:
        return None

    gruppo_anno = None

    for gruppo in album:
        if gruppo[0] == anno:
            gruppo_anno = gruppo
            break

    if gruppo_anno is None:
        gruppo_anno = [anno, []]
        album.append(gruppo_anno)

    gruppo_anno[1].append(nuova_foto)

    return nuova_foto


def cerca_foto(album, codice):
    for gruppo in album:
        for foto in gruppo[1]:
            if foto[0] == codice:
                return f"{foto[0]}, {foto[1]}, {foto[2]}, {foto[3]}, {foto[4]}"

    return None


def elenco_foto_anno_per_titolo(album, anno):
    for gruppo in album:
        if gruppo[0] == anno:
            titoli = []

            for foto in gruppo[1]:
                titoli.append(foto[1])

            titoli.sort()
            return titoli

    return None


def main():
    album = []
    file_path = ""

    while True:
        print()
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ")

        if scelta == "1":
            file_path = input("Nome del file: ")
            nuovo_album = carica_da_file(file_path)

            if nuovo_album is None:
                print("File non trovato")
            else:
                album = nuovo_album
                print("Album caricato")

        elif scelta == "2":
            if len(album) == 0:
                print("Carica prima un album")
                continue

            codice = input("Codice: ")
            titolo = input("Titolo: ")
            autore = input("Autore: ")

            try:
                mese = int(input("Mese: "))
                anno = int(input("Anno: "))
            except ValueError:
                print("Mese o anno non valido")
                continue

            foto = aggiungi_foto(
                album, codice, titolo, autore, mese, anno, file_path
            )

            if foto is None:
                print("Foto non aggiunta")
            else:
                print("Foto aggiunta")

        elif scelta == "3":
            codice = input("Codice da cercare: ")
            risultato = cerca_foto(album, codice)

            if risultato is None:
                print("Foto non trovata")
            else:
                print(risultato)

        elif scelta == "4":
            try:
                anno = int(input("Anno: "))
            except ValueError:
                print("Anno non valido")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)

            if titoli is None:
                print("Anno non presente")
            else:
                for titolo in titoli:
                    print(titolo)

        elif scelta == "5":
            break

        else:
            print("Scelta non valida")


if __name__ == "__main__":
    main()
