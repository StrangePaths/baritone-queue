import main
import time
time.sleep(5)

mci = main.mc_interact()
ft = main.f_trail()
log = main.log_class()

log.edit('resume', 0)
log.edit('err', '')
log.edit('mode', 'deposit')
log.edit('depo_ticks', 0)


# you get what you get
def anti_afk(allow_place=False, allow_break=False):
    print('CALLED')
    if allow_place is False:
        mci.type('#allowplace false')
    if allow_break is False:
        mci.type('#allowbreak false')
    mci.type('#explore')

def excavation(): #can excavate large areas uses a schematic that makes baritone place torches on the ground so mobs dont kill it also can theoretically do the entire thing in one go if u use the refill part of it unlike clear
    #baritones clear ai for large deep areas kinda sucks ass unless they have an inverse layer by layer thing which they might cuz i cant remember if it was a suggestiong or an implementation regardless this is just an example
    repair = False
    #resets that amount of resume ticks
    log.edit('resume', 0)
    mode = log.read('mode')
    if mode == 'burrow':
        if str(type(log.read('err'))) == "<class 'list'>":
            repair = True
            x, y, z = log.read('err')[0], log.read('err')[1], log.read('err')[2]
        else:
            x, y, z = log.read('coords')[0], log.read('coords')[1], log.read('coords')[2]
            if z >= 845337:
                log.edit('mode', 'deposit')
                if x > '': #not leaking my coords
                    x = ''
                    z = ''
                    y -= ''
                else:
                    z = ''
                    x += ''
            else:
                z += 7
        mci.type('#build clear.schematic %d %d %d'%(x, y, z))
        if repair is False:
            log.edit('coords', [x, y, z])
        else:
            log.edit('err', '')


    elif mode == 'deposit':
        ticks = log.read('depo_ticks')
        if ticks == 0:
            mci.type('#sel clear')
            mci.type('#sel 1 --- -- ---')
            mci.type('#sel 2 --- -- ---')
            mci.type('#sel cleararea')
            log.edit('depo_ticks', 1)
        elif ticks == 1:
            print(1)
            time.sleep(5)
            mci.type('#sel cleararea')
            for i in range(8):
                time.sleep(.05)
                pyautogui.rightClick()
            log.edit('depo_ticks', 2)
        elif ticks == 2:
            print(2)
            for count, i in enumerate(range(36)):
                mci.inventory(slot= 36 - i, drop='transfer', type_='double_chest', exit=False)
                time.sleep(.1)
            pyautogui.press('esc')
            mci.type('#stop')
            mci.type('#goto --- -- ---')
            time.sleep(30)
            log.edit('mode', 'burrow')
            log.edit('depo_ticks', 0)
            excavation()

def resume():
    x, y, z = log.read('coords')[0], log.read('coords')[1], log.read('coords')[2]
    resume_ticks = log.read('resume')
    if resume_ticks > 5:
        log.edit('err', [x, y, z])
    mci.type('#resume')
    log.edit('resume', resume_ticks + 1)


ft.func_insert([
    ('[main/INFO]: [CHAT] Connecting to the server...\n', excavation),
    ('[main/INFO]: [CHAT] <%s> %s\n'%('ign','trigger'), excavation),
    ('[main/INFO]: [CHAT] [Baritone] Done building\n', excavation),
    ('[main/INFO]: [CHAT] [Baritone] Unable to do it. Pausing. resume to resume, cancel to cancel\n', resume)




])

excavation() #starts when u run it
ft.start()