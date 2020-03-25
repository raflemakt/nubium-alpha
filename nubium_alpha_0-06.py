#!/usr/bin/env python
import curses
from curses import textpad
import time

"""TODO:
liste av med OEIS i faktorgraf, med forskjellige lister = l
bruk primtalslista i faktorgraf "m"
fikse transparent i svært_tal()
FIKSE NY FAKTORFUNKSJON
legge til beskrivelse og legend til venstre for null i f.graf
Last ned divisorplot.com før den forsvinner
primtalsmodus for f.graf
modus i f.graf for å fjerne tosifra tal (vis kun siste siffer)
"""

menu = ["Faktorgraf", "Vis Primtalsliste", "Gongetabell", "Info", "Quit"]
høgkompositt = [1,2,4,6,12,24,36,48,60,120,180,240,360,720,840,
 1260,1680,2520,5040,7560,10080,15120,20160,25200,221760,277200,332640,498960,554400,665280,720720,
 1081080,1441440,2162160]

def erathostenes(limit):
    n = limit + 1
    sieve = []
    primtal = []
    starttime = time.time()
    for i in range(2, n):
        if i not in sieve:
            primtal.append(i)
            for j in range(i*i, n, i):
                sieve.append(j)
    endtime = time.time()
    elap = round((endtime - starttime), 2)
    return primtal, limit, elap

def sieveprime(n):
    """overlegen"""
    sieve = [True] * n
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i]:
            sieve[i*i::2*i]=[False]*((n-i*i-1)//(2*i)+1)
    return [2] + [i for i in range(3,n,2) if sieve[i]]

def tau_primes(limit):  #denne er seks gonger så effektiv! Kun 6i+1 eller 6i+5 kan vere P
    primtal = [2,3,5]
    starttime = time.time()
    for i in range(1, limit//6):
        if tau(6*i + 1) == 2:
            primtal.append(6*i+1)
        if tau(6*i + 5) == 2:
            primtal.append(6*i+5)
    endtime = time.time()
    elap = round((endtime - starttime), 2)
    return primtal, limit, elap

def tau(n):
    sqroot,t = int(n**0.5),0
    for factor in range(1,sqroot+1):
        if n % factor == 0:
            t += 2 # both factor and N/factor
    if sqroot*sqroot == n: t = t - 1 # if sqroot is a factor then we counted it twice, so subtract 1
    return t

def OEIS_liste_temp(stdscr, y, x):
    #bruk WASD for å manøvrere lista/infoen.
    #kanskje ha legend her
    h, w = stdscr.getmaxyx()
    liste_h = h - y - 2
    stdscr.border(0)
    listeboks = stdscr.subwin(20,20,5,5)
    listeboks.bkgd(" ", curses.color_pair(1))
    listeboks.box()
    listeboks.refresh()
    #textpad.rectangle(stdscr, 5, 4, liste_h + y, 22)

def OEIS_liste(stdscr, y, x):
    #bruk WASD for å manøvrere lista/infoen.
    #kanskje ha legend her
    h, w = stdscr.getmaxyx()
    liste_h = h - y - 2
    textpad.rectangle(stdscr, 5+y, 4+x, liste_h + y, 32)
    liste_tittel = "OEIS A002182: Høgkompositt-tal"
    stdscr.addstr(5+y, 5+x, liste_tittel)
    stdscr.addstr(h-2, 0, "Denne funksjonaliteten er under utvikling")
    for i in range(0, liste_h - 2):
        try:
            stdscr.addstr(6+y+i, 5+x, str(høgkompositt[i]))
        except:
            pass

def faktorgraf(stdscr, COUNTER, show_marker):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    n = 0
    user_offset = COUNTER - w//2
    longstep = 12
    show_liste = False
    prime_mode = False

    while True:
        h, w = stdscr.getmaxyx()
        stdscr.erase()

        #enkel mark
        stdscr.addstr(1, w//2, "V", curses.A_BOLD)

        #scale (raud skrift)
        for n in range(0-user_offset, w-len(str(n)), longstep):
            num = str(n+user_offset)
            if n >= 0:
                stdscr.addstr(0, n, num, curses.color_pair(3))

        #grafen (kvit)
        for i in range(0, h-2): # høgda
            num = str(i+1) #det som printast
            row = i + 1
            if prime_mode:
                i = int(primtal[i])
                num = str(i)
    
            #find offsets
            offs = 0
            for off in range(0, w-2):
                if int(user_offset + off) % (i+1 - 1*prime_mode) == 0:
                    offs = off
                    break
            for j in range(0, w-2-offs, i+1): #bredda
                if j >= 0:
                    stdscr.addstr(row+1, j+offs, num)
                    if show_marker and int(j+offs) == w//2:
                        stdscr.addstr(row+1, w//2, num, curses.color_pair(1))
        
        #primtal P, kvadrattal K, tau-markør tau(n)=
        if show_marker:
            stdscr.addstr(1, w//2, "tau(n) = "+str(tau(w//2 + user_offset)), curses.color_pair(4))
            if user_offset == 0-w//2:
                stdscr.addstr(1, w//2, "tau(n) er udefinert", curses.color_pair(4))
            bunn_l = "n = " + str(w//2 + user_offset)
            stdscr.addstr(0, w//2 - 4, bunn_l, curses.color_pair(1))
            #for num in range(0 - user_offset, w-2):
            for num in range(0, w-2):
                current = num + user_offset                    
                if current >= 0:
                    if (current + 1) % 6 == 0 or (current + 5) % 6 == 0 or current in [2,3]:
                        if tau(current) == 2:
                        #if current in primtal: er skikkelig treig, men kvifor
                            if num == w//2:
                                stdscr.addstr(2, num, "P", curses.color_pair(15))
                            else:
                                stdscr.addstr(2, num, "P", curses.color_pair(5))
                    if (tau(current) + 1) % 2 == 0 and num >= 0:
                    #if current in kvadrattal:
                        if num == w//2:
                            stdscr.addstr(2, num, "K", curses.color_pair(16))
                        else:
                            stdscr.addstr(2, num, "K", curses.color_pair(6))

        #print listeboks
        if show_liste:
            OEIS_liste(stdscr, 0, 0)

        bunn_r = "m = markør, \u21d4 = bla, SHIFT + \u21d4 = bla raskt"
        stdscr.addstr(h-1, w-len(bunn_r)-1, bunn_r, curses.color_pair(1))

        key = stdscr.getch()
        if key == curses.KEY_LEFT:
            if user_offset > 0 - w//2:
                user_offset -= 1
        elif key == curses.KEY_RIGHT:
                user_offset += 1
        #shift
        if key == curses.KEY_SLEFT:
            if user_offset <  0 - w//2 + longstep:
                user_offset = 0 - w//2
            else:
                user_offset -= longstep

        elif key == curses.KEY_SRIGHT:
                user_offset += longstep

        elif key == ord('m'):
            show_marker ^= True #XOR-operator
        elif key == ord('p'):
            prime_mode ^= True
        elif key == ord('l'):
            show_liste ^= True
        elif key == curses.KEY_ENTER or key in [10, 13] or key == ord("q"):
            return user_offset + w//2

def gongetabell(stdscr):
    h, w = stdscr.getmaxyx()
    stdscr.erase()
    for n in range(1, h-2):
        for m in range(1, w//3 - 1):
            tekst = str(n * m)
            if m % 2 == 0:
                stdscr.addstr(n, 3*m, tekst)
            else:
                stdscr.addstr(n, 3*m, tekst, curses.color_pair(3))
    stdscr.getch()

def svært_tal(stdscr, tal_input, offsy, offsx):
    lengde = [9, 4, 8, 8, 8, 8, 9, 8, 8, 8]
    tal_str = str(tal_input)

    tal_grafikkliste = [
    " ██████╗  ██╗██████╗ ██████╗ ██╗  ██╗███████╗ ██████╗ ███████╗ █████╗  █████╗ ",
    "██╔═████╗███║╚════██╗╚════██╗██║  ██║██╔════╝██╔════╝ ╚════██║██╔══██╗██╔══██╗",
    "██║██╔██║╚██║ █████╔╝ █████╔╝███████║███████╗███████╗     ██╔╝╚█████╔╝╚██████║",
    "████╔╝██║ ██║██╔═══╝  ╚═══██╗╚════██║╚════██║██╔═══██╗   ██╔╝ ██╔══██╗ ╚═══██║",
    "╚██████╔╝ ██║███████╗██████╔╝     ██║███████║╚██████╔╝   ██║  ╚█████╔╝ █████╔╝",
    " ╚═════╝  ╚═╝╚══════╝╚═════╝      ╚═╝╚══════╝ ╚═════╝    ╚═╝   ╚════╝  ╚════╝ "]

    tal_offsx = 0
    while len(tal_str) != 0:
        if len(tal_str) > 1:
            current_tal = int(tal_str[:-len(tal_str)+1]) #]
        else:
            current_tal = int(tal_str)
        remain = 0
        before = 0
        if current_tal > 0:
            for i in range(0, current_tal):
                before = before + lengde[i]
        for num in range(current_tal+1, len(lengde)):
            remain = remain + lengde[num]
        for i in range(0, 6):
            kort = tal_grafikkliste[i]
            if current_tal < 9:
                kort = kort[:-remain]
            kortere = kort[before:]
            stdscr.addstr(offsy+i, offsx + tal_offsx, kortere, curses.color_pair(6))
        tal_offsx = tal_offsx + lengde[current_tal]
        tal_str = tal_str[1:]


def faktor_numerical(n):
    faktorar = []
    for i in range(2, n):
        while n % i == 0:
            faktorar.append(i)
            n = n // i
    return faktorar

def faktor(n):
    if n >= len(primtal) * 2:
        return "Kan ikkje faktorisere tal over "+str(len(primtal)*2-1)
    if n == 0:
        return "Alle positive heiltal"
    faktorar = []
    limit = int((n/2) + 1)
    for i in range(0, limit):
        while n % primtal[i] == 0:
            faktorar.append(primtal[i])
            n = n / (primtal[i])
    return faktorar

def print_menu(stdscr, selected_row_idx):
    stdscr.erase()
    h, w = stdscr.getmaxyx()
    textpad.rectangle(stdscr, 2, 3, h-2, w-3)

    nubium_logo = [
    ",--.  ,--.        ,--.   ,--.                  ",
    "|  ,'.|  |,--.,--.|  |-. `--',--.,--.,--,--,--.",
    "|  |' '  ||  ||  || .-. ',--.|  ||  ||        |",
    "|  | `   |'  ''  '| `-' ||  |'  ''  '|  |  |  |",
    "`--'  `--' `----'  `---' `--' `----'A L P H A-'    v0.05"]

    offsx = w//2 - len(nubium_logo[0])//2
    offsy = 0
    for i in range(0, len(nubium_logo)):
        stdscr.addstr(offsy + i, offsx, nubium_logo[i])
    stdscr.addstr(offsy+4, w//2 + 13, "A L P H A")

    bunntekst_l = " ◀ SHIFT ▶, f = faktorgraf"
    stdscr.addstr(h-1, 4, bunntekst_l)
    bunntekst_r = "\u25b2 ENTER \u25bc,  q = quit"
    stdscr.addstr(h-1, w - len(bunntekst_r)-3, bunntekst_r)

    for i in range(6, h - len(menu) - 3):
        for j in range(5, w-4, i-4):
            #stdscr.addstr(i, j, "Nub", curses.color_pair(6))
            #stdscr.addstr(i, j, "\u262D", curses.color_pair(3))
            stdscr.addstr(i, j, "\u2618", curses.color_pair(4))
    textpad.rectangle(stdscr, 5, 4, h - len(menu) - 3, w-4) #firkant inni

    for idx, row in enumerate(menu):
        x = w - len(row) - 3
        y = h - len(menu) + idx - 2
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    #stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(15, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(16, curses.COLOR_BLACK, curses.COLOR_GREEN)

    current_row_idx = 0
    tal_str = "0"
    faktorar = []
    print_menu(stdscr, current_row_idx)

    while True:
        h, w = stdscr.getmaxyx()
        stdscr.erase()

        COUNTER = int(tal_str)
        faktorar = faktor_numerical(int(COUNTER))
        print_menu(stdscr, current_row_idx)
        svært_tal(stdscr, COUNTER, h-8, 5)

        tau_COUNTER = tau(COUNTER)
        x_offs = 15
        stdscr.addstr(h-11, x_offs, "Faktorar i "+str(COUNTER)+":")
        stdscr.addstr(h-10, x_offs, str(faktorar))
        #if tau_COUNTER == 2:
        if COUNTER <= primtal[-1]:
            if COUNTER in primtal:
                stdscr.addstr(h-12, x_offs, "Primtal", curses.color_pair(5))
        elif tau_COUNTER == 2:
                stdscr.addstr(h-12, x_offs, "Primtal", curses.color_pair(5))

        #fiks denne
        """
        n = 1
        for i in range(1, COUNTER, 2*n + 1):
            n = i
            if i == COUNTER:
                stdscr.addstr(h-12, x_offs, "Kvadrattal", curses.color_pair(6))
        """
        
        if (tau_COUNTER + 1) % 2 == 0:
            stdscr.addstr(h-12, x_offs, "Kvadrattal", curses.color_pair(6))
        if COUNTER in høgkompositt:
            stdscr.addstr(h-9, x_offs, "Høgkompositt", curses.color_pair(4))

        key = stdscr.getch()
        char = chr(key)

        if key == curses.KEY_RIGHT:
            COUNTER += 1
            tal_str = str(int(tal_str) + 1)
        elif key == curses.KEY_SRIGHT:
            COUNTER += 10
            tal_str = str(int(tal_str) + 10)
        elif key == curses.KEY_LEFT:
            if COUNTER >= 1:
                COUNTER -= 1
                tal_str = str(int(tal_str) - 1)
        elif key == curses.KEY_SLEFT:
            if COUNTER <= 10:
                COUNTER = 0
                tal_str = str(0)
            else:
                COUNTER -= 10
                tal_str = str(int(tal_str) - 10)
        elif key == 127:
            if len(tal_str) > 1:
                tal_str = tal_str[:-1]
            else:
                tal_str = "0"
        elif key == ord('f'):
            show_marker = True
            if COUNTER > 1000000:      #opp frå 4k
                show_marker = False
            tal_str = str(faktorgraf(stdscr, COUNTER, show_marker))
        elif char.isdigit():
            tal_str = tal_str + char


        elif key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
            current_row_idx += 1
        elif key == ord('q'):
            break
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row_idx == 1:
                stdscr.clear()
                try:
                    stdscr.addstr(0, w//2 - len(streng)//2, streng, curses.color_pair(3))
                    stdscr.addstr(1, 0, primtalstr)
                except:
                    pass
                stdscr.refresh()
                stdscr.getch()
            elif current_row_idx == 0:
                show_marker = True
                if COUNTER > 1000000:      #Fjern denne etter optimalisering
                    show_marker = False
                tal_str = str(faktorgraf(stdscr, COUNTER, show_marker))
            elif current_row_idx == 2:
                gongetabell(stdscr)
            elif current_row_idx == 3:
                # "info"
                pass
            elif current_row_idx == len(menu) - 1:
                break


primtal_limit = 1000000
starttime = time.time()
primtal = sieveprime(primtal_limit)
primtal_len = len(primtal)
endtime = time.time()
elap = starttime - endtime
streng = ("Fann " + str(len(primtal)) + " primtal under " + str(primtal_limit) +
    ", brukte " + str(elap) + " sekunder.")
primtalstr = str(primtal).strip('[]')

curses.wrapper(main)
