import json,re
h=open('/mnt/user-data/outputs/app4/index.html').read()
order=['punch','tunnel','snow','suitcase','change','lake','uniform','liars','stub','lantern']
cn={c:31+i for i,c in enumerate(order)}
# moods per case/char from MOODS block
mb=h[h.index('const MOODS'):]; M={}
for c in order:
    line=re.search(r'\n\s*'+c+r':\{(.*)\n',mb).group(1)
    M[c]={ch:set(re.findall(r'"(\w+)"',body))-{'neutral','nervous'} for ch,body in re.findall(r'(\w+):\{([^}]*)\}',line)}
reuse={'kaur':'punch','szabo':'punch','tess':'snow'}
for who,home in reuse.items():
    u=set()
    for c in order:
        if who in M[c]: u|=M[c][who]
    M[home][who]=u
STYLE="An adult"  # unused
D={
'punch':{'bg':"A wide 16:9 view inside a vintage mountain train dining car: small tables with white cloths and little lamps, red leather seats, big windows on both sides showing green mountains and pine forest, a wooden serving counter with a coffee machine on the left, a door to the next car at the back, warm morning light.",
 'kaur':"an adult woman chief train conductor named Ms. Kaur, Indian, brown skin, long black hair in a neat braid, a navy conductor uniform with gold buttons, a red conductor cap, a silver ticket punch on a chain",
 'szabo':"an adult man train chef named Mr. Szabo, Hungarian, light skin, a short grey beard, a white chef coat and small chef hat, a tea towel over his shoulder",
 'timetable':"printed train timetable board in a wooden frame with station names and times",
 'novak':"an adult man named Mr. Novak, Czech, light skin, short brown hair, a tweed jacket, a long red scarf, a leather bag covered in old train badges",
 'castillo':"an older woman named Mrs. Castillo, Mexican, tan skin, curly grey hair, glasses, a green cardigan, holding knitting needles and blue wool",
 'benji':"a 14 year old boy named Benji, Nigerian, dark brown skin, short hair, a grey hoodie, big headphones around his neck, a phone"},
'tunnel':{'bg':"A wide 16:9 view of a vintage mountain train sleeper car corridor: a long narrow corridor with wood panels, sliding doors with room numbers on the right, a row of windows on the left showing snowy mountains, a small wall shelf, warm lamps on the ceiling, a carpet runner.",
 'dahl':"an older woman photographer named Mrs. Dahl, Norwegian, pale skin, short white hair, a khaki travel vest with many pockets, a camera strap around her neck with no camera",
 'ferreira':"an adult man businessman named Mr. Ferreira, Portuguese, olive skin, slicked black hair, a thin moustache, a grey suit, a gold watch",
 'park':"an adult woman named Ms. Park, Korean, light skin, a black bob haircut, a beige trench coat, a small suitcase, a train ticket in her hand",
 'amadi':"an adult man painter named Mr. Amadi, Nigerian, dark brown skin, a short beard, a paint-splashed blue shirt, holding a paintbrush and small canvas"},
'snow':{'bg':"A wide 16:9 view of a small snowy mountain station platform: deep snow on the roofs, a wooden station building, a little kiosk with snow globes and newspapers on the left, a blue vintage train with open doors on the right, pine trees, falling snow, early morning light.",
 'aalto':"an older woman kiosk owner named Mrs. Aalto, Finnish, pale skin, rosy cheeks, white hair in a bun under a knitted hat, a thick red coat, fingerless gloves",
 'tess':"a young adult woman baggage helper named Tess, Irish, pale skin, freckles, red hair in a short ponytail, green work overalls, a cap, a clipboard",
 'lindgren':"an adult man named Mr. Lindgren, Swedish, pale skin, light brown hair, a beard, a thick grey wool sweater, dark boots with snow on them",
 'quist':"an adult woman named Ms. Quist, Dutch, pale skin, blonde hair in a bun, a long blue coat, a folded newspaper under her arm",
 'mila':"an 8 year old girl named Mila, Polish, light skin, two blonde pigtails, a pink winter jacket, a woolly hat with a pom-pom"},
'suitcase':{'bg':"A wide 16:9 view inside a vintage train baggage car: wooden walls, metal shelves with suitcases and boxes on two levels, two identical black suitcases in front, luggage tags hanging from handles, a small desk with a clipboard, a sliding door, soft light from a small window.",
 'haugen':"an older man violin maker named Mr. Haugen, Norwegian, pale skin, white hair and a long white beard, round glasses, a brown waistcoat, a measuring tape around his neck",
 'baglist':"clipboard with a baggage list and luggage tag numbers on a small wooden desk",
 'abara':"an adult man named Mr. Abara, Ghanaian, dark brown skin, short hair, a smart black coat, a black suitcase with a luggage tag",
 'rask':"an adult woman violin teacher named Ms. Rask, Estonian, pale skin, long straight brown hair, a dark green dress, holding a pile of music books"},
'change':{
 'cashbox':"small metal cash box with notes inside on a wooden train counter",
 'slips':"small pile of paper lunch slips with a pen on a wooden counter",
 'holm':"an adult woman named Ms. Holm, Danish, pale skin, sharp blonde bob haircut, a purple coat, a handbag, arms crossed",
 'eriksen':"a young adult waiter named Mr. Eriksen, Swedish, pale skin, neat blond hair, a white shirt with a black waistcoat and bow tie, holding a tray of plates"},
'lake':{'bg':"A wide 16:9 view inside a vintage train observation car: huge curved windows all around, a big blue mountain lake outside on the left side, comfy armchairs facing the windows, small side tables, a stand with a golden lantern at the back, bright afternoon light.",
 'tanaka':"an older woman named Mrs. Tanaka, Japanese, light skin, neat grey hair, a lavender cardigan, an open handbag on her arm",
 'rocha':"an adult man named Mr. Rocha, Brazilian, tan skin, curly black hair, a yellow shirt, a big camera phone held up",
 'wren':"an adult woman birdwatcher named Ms. Wren, English, pale skin, short red hair, a green outdoor jacket, binoculars around her neck",
 'boyle':"an older man named Mr. Boyle, Scottish, pale skin, bald with white sideburns, a tartan scarf, a sleepy face, a folded newspaper"},
'uniform':{
 'mensah':"an older man named Mr. Mensah, Ghanaian, dark brown skin, white hair, a smart brown suit, reading glasses on his nose",
 'closetlog':"small logbook hanging on a hook next to a staff closet door",
 'halloran':"an adult man named Mr. Halloran, Irish, pale skin, a grey beard, a grey sweater, brown shoes",
 'brandt':"an adult man train conductor named Mr. Brandt, German, light skin, clean-shaven, short brown hair, a navy conductor uniform and cap, black polished shoes",
 'ivers':"an adult woman named Ms. Ivers, Canadian, light brown skin, long dark hair, a long navy wool coat, a handbag"},
'liars':{
 'sato':"an adult woman named Ms. Sato, Japanese, light skin, black hair in a long braid, round glasses, a cosy grey cardigan, holding a book",
 'lena':"an 11 year old girl named Lena, German, light skin, straight brown hair, blue pyjamas with stars, slippers",
 'ole':"a 9 year old boy named Ole, German, light skin, messy blond hair, green pyjamas, a little chocolate on his chin",
 'vance':"an adult man toy collector named Mr. Vance, American, light skin, slicked grey hair, a thin face, striped blue-and-white pyjamas, a silk dressing gown"},
'stub':{
 'bianchi':"an adult woman chocolate maker named Ms. Bianchi, Italian, olive skin, dark curly hair under a white cap, a brown chocolatier apron",
 'galloway':"an adult man named Mr. Galloway, English, light brown skin, short black hair, a white shirt with rolled cuffs, a brown waistcoat",
 'nyberg':"an adult man hotel porter named Mr. Nyberg, Finnish, pale skin, tall, short blond hair, a burgundy hotel porter uniform and round cap"},
'lantern':{
 'lindahl':"an older woman named Mrs. Lindahl, Swedish, pale skin, silver hair, a yellow raincoat, an old instant camera",
 'albrecht':"an adult woman train writer named Ms. Albrecht, Austrian, light skin, brown hair in a high bun, a long brown coat, a red notebook in her hand",
 'pereira':"an adult man named Mr. Pereira, Portuguese, olive skin, a neat black beard, a dark blue sweater, holding a chess piece",
 'rune':"a 10 year old boy named Rune, Norwegian, pale skin, light blond hair, a red puffer jacket, snow on his boots, a notebook with tunnel light tally marks"}}
icons={'punch':[{'name':'punch','desc':'a silver train conductor ticket punch'},{'name':'timetable','desc':'a printed train timetable card'},{'name':'train','desc':'a small blue vintage train with five cars'}],
 'snow':[{'name':'snowglobe','desc':'a snow globe with a little mountain station inside'},{'name':'snow','desc':'a white snowflake'}],
 'suitcase':[{'name':'suitcase','desc':'a black suitcase with a luggage tag'}],
 'uniform':[{'name':'pen','desc':'a gold fountain pen'}],
 'lantern':[{'name':'lantern','desc':'a golden lantern with a glowing light'}]}
OBJ=('printed','clipboard','small','printed')
for c in order:
    d=D[c]; sp={'case':f'case{cn[c]}'}
    if 'bg' in d: sp['bg']=d['bg']
    chars=[]
    for k,v in d.items():
        if k=='bg': continue
        if k not in M[c]: chars.append({'id':k,'object':True,'desc':v})
        else: chars.append({'id':k,'desc':v,'moods':sorted(M[c].get(k,set()))})
    sp['chars']=chars; sp['icons']=icons.get(c,[])
    json.dump(sp,open(f'/mnt/user-data/outputs/gen/case{cn[c]}.json','w'),indent=1)
    print(c,cn[c],[(x['id'],x.get('moods','obj')) for x in chars],[i['name'] for i in sp['icons']])
