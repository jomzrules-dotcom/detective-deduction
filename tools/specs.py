import json,re
moods=open('/home/claude/f3_moods.js').read()
# parse moods per case/char
M={}
for line in moods.strip().splitlines():
    cid=line.strip().split(':',1)[0]
    M[cid]={}
    for ch,body in re.findall(r'(\w+):\{([^}]*)\}',line.split(':{',1)[1]):
        ms=set(re.findall(r'"(\w+)"',body))-{'neutral','nervous'}
        M[cid][ch]=ms
order=['cheese','surprise','harmonica','trainset','topper','pumpkin','ferry','page','tag','openkey']
reuse={'bello':'cheese','nakamura':'cheese','kowal':'surprise'}
# union moods for recurring
for who,home in reuse.items():
    u=set()
    for c in order:
        if who in M[c]: u|=M[c][who]
    M[home][who]=u
D={
'cheese':{'bg':"A wide 16:9 view inside a busy covered city market hall: a high glass-and-iron roof, rows of colourful food stalls with awnings, a dairy stall with cheese wheels and a white cool box on the left, a honey stall with jars, a big round hall clock on the back wall, a back door with a delivery sign on the right, warm afternoon light.",
 'bello':"an adult police officer named Officer Bello, a friendly woman, dark brown skin, short black natural hair under a police cap, a navy police uniform with a reflective vest, a notebook in her hand",
 'nakamura':"an older woman market manager named Mrs. Nakamura, Japanese, light skin, short grey hair, glasses on a chain, a green market apron over a cardigan, holding a clipboard with the stall list",
 'arjun':"a young adult man named Arjun, Indian, brown skin, short black hair, a white dairy apron and cap, rolled-up sleeves",
 'rohan':"a 9 year old boy named Rohan, Indian, brown skin, messy black hair, a yellow t-shirt with cheese crumbs on it, shorts",
 'ines':"an adult woman named Ines, Spanish, olive skin, long wavy brown hair, a striped honey-stall apron, a jar of honey in her hand",
 'dlist':"clipboard with a delivery list hanging on a hook by a back door"},
'surprise':{'bg':"A wide 16:9 view of a city apartment building lobby: a concierge desk with a visitor book and a bell on the left, rows of metal mailboxes, a lift with brass doors in the back, a door marked PARCELS and a door marked LAUNDRY on the right, potted plants, a tiled floor, evening light from a glass front door.",
 'kowal':"an older man concierge named Mr. Kowal, Polish, light skin, neat white moustache, bald on top with grey sides, a dark green concierge jacket with brass buttons, a big ring of keys on his belt",
 'seo':"an adult man named Mr. Seo, Korean, light skin, short black hair, a grey hoodie and jeans, bike gloves, holding a bike wrench",
 'mateo':"an 11 year old boy named Mateo, Latino, tan skin, short curly black hair, a red hoodie with white dryer lint on one sleeve, jeans",
 'brennan':"an older woman named Mrs. Brennan, Irish, pale skin, curly white hair, a lilac cardigan, pearl earrings, holding a small handbag",
 'bruno':"an adult courier named Bruno, Brazilian, tan skin, short black hair and stubble, an orange courier uniform with a cap, a parcel scanner in his hand",
 'llog':"key card reader panel with a small screen next to a laundry room door"},
'harmonica':{'bg':"A wide 16:9 view of a clean underground subway platform: a long platform with a yellow safety line, a train tunnel on the right, tiled walls with a city map, a small tea kiosk, a wooden bench, a row of ticket gates on the left, an open guitar case on the floor near a pillar, bright station lights.",
 'gallo':"an adult street musician named Mr. Gallo, Italian, olive skin, a brown beard, a flat cap, a patched corduroy jacket, a scarf, holding a cup of tea",
 'lucia':"a 10 year old girl named Lucia, Latina, tan skin, two dark brown braids, a purple coat, a backpack covered in gold star stickers",
 'dmitri':"a 10 year old boy named Dmitri, Russian, light skin, straight blond hair, a blue puffer jacket, a subway pass on a lanyard",
 'grimsby':"an older grumpy man named Mr. Grimsby, light skin, bushy grey eyebrows, a brown flat cap, a long beige raincoat, a folded newspaper",
 'wen':"an adult woman named Wen, Chinese, light skin, black hair in a low ponytail, a red kiosk apron over a white shirt, holding a teapot",
 'gates':"small screen on top of a subway ticket gate showing a list of taps"},
'trainset':{'bg':"A wide 16:9 view of a bright department store toy floor: shelves of toys and puzzles, a big model train set on a display table, a hold shelf with boxes behind a counter on the left, a gift-wrap desk with ribbon rolls, a cashier till near the front doors on the right, colourful hanging signs.",
 'yasmin':"an adult woman cashier named Yasmin, Middle Eastern, olive skin, a navy headscarf, a red store vest with a name badge",
 'duarte':"an adult man store guard named Mr. Duarte, Portuguese, tan skin, a shaved head, a black guard uniform with a radio on the shoulder",
 'fujita':"an older man named Mr. Fujita, Japanese, light skin, neat grey hair, glasses, a beige coat over a sweater vest, a receipt in his hand",
 'desmond':"a young adult stock boy named Desmond, Black, dark brown skin, short twists, a red store vest, holding half a sandwich",
 'rhee':"an adult woman named Ms. Rhee, Korean, light skin, a black bob haircut, a white trench coat, holding a puzzle box",
 'tunde':"a young adult man named Tunde, Nigerian, dark brown skin, short hair, a red store vest, a roll of shiny wrapping paper",
 'holdlog':"open logbook on a counter with a pen on a string, a hold shelf behind it"},
'topper':{
 'mbatha':"an adult woman named Ms. Mbatha, South African, dark brown skin, long braids in a bun, a yellow dress, holding a phone showing a photo",
 'anders':"an adult man named Anders, Swedish, pale skin, blond hair, a stubble beard, a green scarf, a travel jacket, a phone in his hand",
 'haddad':"an adult man baker named Mr. Haddad, Lebanese, olive skin, a thick black moustache, a white chef jacket and tall chef hat, flour on his hands",
 'hugo':"a 13 year old boy named Hugo, French, light skin, curly brown hair, a green flower-stall apron, holding a bunch of tulips",
 'ruiz':"an adult woman named Ms. Ruiz, Mexican, tan skin, shoulder-length black hair, a denim jacket, holding a white cake box",
 'hallcam':"small security camera fixed under a big round hall clock"},
'pumpkin':{'bg':"A wide 16:9 view of a sunny rooftop garden on a city building: wooden planters with vegetables, a big empty planter marked 4 in front, a small garden shed on the right, tomato beds on the far side, a city skyline behind a railing, a gate with a sign, bright blue sky.",
 'abiodun':"an adult woman contest judge named Mrs. Abiodun, Nigerian, dark brown skin, a colourful head wrap, a green garden dress, a judge's ribbon rosette, a clipboard",
 'halvorsen':"an adult woman named Mrs. Halvorsen, Norwegian, pale skin, long straight blonde hair, a light blue raincoat, a sun hat",
 'keiko':"a 9 year old girl named Keiko, Japanese, light skin, shoulder-length black hair worn loose, a pink t-shirt with a pumpkin on it, dungarees, soil on her knees",
 'ueda':"an older man gardener named Mr. Ueda, Japanese, light skin, a short white beard, a straw hat, a brown work apron, holding a rake",
 'otto':"a 15 year old boy named Otto, German, light skin, red hair, freckles, a volunteer t-shirt, rubber boots, holding a garden hose",
 'roofcam':"small weatherproof camera on a pole above a garden planter"},
'ferry':{
 'bauer':"an adult man station master named Mr. Bauer, German, light skin, a grey moustache, a dark blue station uniform and peaked cap, a whistle",
 'selin':"a 10 year old girl named Selin, Turkish, light olive skin, long dark wavy hair, a green coat, a yellow backpack, a little white glue on her fingertips",
 'asante':"an adult woman cleaner named Mrs. Asante, Ghanaian, dark brown skin, short grey hair, a light grey cleaner's uniform, a mop, glasses pushed up on her head",
 'idris':"an 11 year old boy named Idris, Moroccan, light brown skin, short black hair, a bright yellow raincoat, a subway ticket in his hand",
 'pryce':"an adult woman named Ms. Pryce, Welsh, pale skin, short purple-dyed hair, a craft apron full of pockets, holding a hot glue gun",
 'stcam':"small station security camera on a tiled wall bracket"},
'page':{
 'ferro':"an adult woman florist named Ms. Ferro, Italian, olive skin, dark hair in a messy bun, a pink florist apron, holding a big bunch of red roses",
 'wainwright':"an adult woman named Mrs. Wainwright, English, pale skin, silver bob haircut, a smart navy dress, a party invitation card in her hand",
 'kenji':"a 15 year old boy named Kenji, Japanese, light skin, spiky black hair, a black t-shirt, a skateboard under his arm",
 'dube':"an older woman named Mrs. Dube, Zimbabwean, dark brown skin, white hair in a neat bun, a red knitted shawl, reading glasses",
 'lund':"an adult man named Mr. Lund, Danish, pale skin, light brown hair, a sweaty running shirt and shorts, a sports watch",
 'liftlog':"brass lift panel with a small screen showing a list of floors and times"},
'tag':{
 'fontaine':"an adult man floor manager named Mr. Fontaine, French, light skin, slick dark hair, a grey suit with a red store tie and a name badge",
 'ortega':"an older woman named Mrs. Ortega, Colombian, tan skin, curly grey hair, a bright orange cardigan, a shopping bag",
 'sorensen':"an adult woman named Ms. Sorensen, Danish, pale skin, a tidy blonde bun, a red store vest with a senior badge, a calm smile",
 'yusuf':"a young adult man named Yusuf, Somali, dark brown skin, short hair, a red store vest with a shiny new floor-lead badge",
 'hosseini':"an adult man named Mr. Hosseini, Iranian, olive skin, a short black beard, a warehouse jacket, holding a clipboard",
 'kemp':"an adult woman named Ms. Kemp, Australian, light skin, curly red hair, a red store vest, holding a spinning toy top",
 'badgelog':"badge reader on a staff door with a small green screen"},
'openkey':{
 'ribeiro':"an adult man bandleader named Mr. Ribeiro, Brazilian, tan skin, wavy black hair, a sparkly purple band jacket, a trumpet, dirty red soil on his shoes",
 'achebe':"an adult woman named Ms. Achebe, Nigerian, dark brown skin, short natural hair, a flower-patterned apron, holding a coffee cup",
 'kwame':"a 10 year old boy named Kwame, Ghanaian, dark brown skin, short hair, a green football shirt, a visitor pass on a lanyard",
 'yilmaz':"an adult man market cleaner named Mr. Yilmaz, Turkish, olive skin, a big black moustache, a grey cleaner's uniform, a broom",
 'delphine':"an adult woman ceremony host named Ms. Delphine, Haitian, dark brown skin, long braids, a smart red dress, holding a microphone",
 'roofgate':"metal rooftop gate with a pass reader and a small screen"}}
icons={'cheese':[],'pumpkin':[{'name':'pumpkin','desc':'a big orange pumpkin'}],'page':[{'name':'rose','desc':'a single red rose'}]}
cn={c:21+i for i,c in enumerate(order)}
for c in order:
    d=D[c]; sp={'case':f'case{cn[c]}'}
    if 'bg' in d: sp['bg']=d['bg']
    chars=[]
    for k,v in d.items():
        if k=='bg': continue
        if v.startswith(('clipboard','key card','small','open logbook','brass','badge reader','metal')) and k not in M[c]:
            chars.append({'id':k,'object':True,'desc':v})
        else:
            chars.append({'id':k,'desc':v,'moods':sorted(M[c].get(k,set()))})
    sp['chars']=chars; sp['icons']=icons.get(c,[])
    json.dump(sp,open(f'/mnt/user-data/outputs/gen/case{cn[c]}.json','w'),indent=1)
    print(c,cn[c],[ (x['id'],x.get('moods','obj')) for x in chars])
