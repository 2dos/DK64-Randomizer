"""Patch some common text."""

import shutil

from BuildEnums import Icons, MoveTypes
from BuildClasses import hint_region_list, MoveName
from text_decoder import grabText
from text_encoder import writeText
from typing import BinaryIO

move_hints = [
    {
        "move": "Baboon Blast",
        "kong": "Donkey",
        "cranky": "THIS POTION WILL MAKE YOU SOAR JUST LIKE I USED TO BEFORE YOU WERE BORN.",
        "funky": "YOU WON'T BELIEVE HOW HIGH THIS IS GONNA SEND YA! GET READY FOR BLASTOFF!",
        "candy": "WITH THIS THING, YOU'LL BE ON CLOUD NINE!",
    },
    {
        "move": "Strong Kong",
        "kong": "Donkey",
        "cranky": "WITH THIS, YOU'LL HAVE NO EXCUSE TO FAIL, NOTHING WILL HURT YOU!",
        "funky": "DRINK THIS AND SHOW THESE BADDIES WHO'S THE BOSS, HUH?",
        "candy": "IF YOU CAN FIND THE BARREL WITH YOUR HANDSOME FACE ON IT, NOTHING WILL HURT YOU.",
    },
    {
        "move": "Gorilla Grab",
        "kong": "Donkey",
        "cranky": "MAYBE YOU'LL FINALLY MATCH MY STRENGTH OF THE OLD DAYS ONCE YOU DRINK IT.",
        "funky": "WITH THAT MUCH STRENGTH, YOU'LL BE GRABBIN' LEVERS LEFT AND RIGHT, MAN!",
        "candy": "AFTER YOU DRINK THAT POTION, COULD YOU OPEN THIS JAR FOR ME, LOVE?",
    },
    {
        "move": "Chimpy Charge",
        "kong": "Diddy",
        "cranky": "NOW DON'T GO SMASHING YOUR HEAD TOO MUCH OR YOU'LL END UP LIKE DONKEY!",
        "funky": "THIS POTION WILL MAKE YOU ROCK! YOUR HEAD WILL BE AS HARD AS ONE!",
        "candy": "WITH THIS, YOU WILL HAVE A STRONG HEAD! NOW, PLEASE TAKE CARE OF YOUR PRETTY LITTLE FACE...",
    },
    {
        "move": "Rocketbarrel",
        "kong": "Diddy",
        "cranky": "FIND MY BARREL WITH YOUR FACE ON IT TO TRY OUT MY PROTOTYPE JETBARREL.",
        "funky": "YOU'LL LOVE THIS ONE! SWING BY THE SPECIAL BARREL AND BLAST OFF WITH ROCKETS ON YOUR BACK!",
        "candy": "BE CAREFUL WITH THIS ONE, YOU'LL BE FLYING HIGH!",
    },
    {
        "move": "Simian Spring",
        "kong": "Diddy",
        "cranky": "EVEN I COULD JUMP HIGHER THAN YOU, SO I'M SURE YOU'LL BE NEEDING THIS ONE.",
        "funky": "IT'S GONNA TURN YOUR TAIL INTO A TRAMPOLINE!",
        "candy": "LET'S ADD A BIT OF SPRING TO YOUR STEP, SHALL WE?",
    },
    {
        "move": "Orangstand",
        "kong": "Lanky",
        "cranky": "THIS HANDY LITTLE MOVE SHOULD HELP YOU GET UP STEEP SLOPES.",
        "funky": "THIS'LL BE THE PERFECT UPPER BODY WORKOUT!",
        "candy": "THIS DRINK WILL LET YOU MAKE USE OF THESE BIG LONG ARMS OF YOURS.",
    },
    {
        "move": "Baboon Balloon",
        "kong": "Lanky",
        "cranky": "THE BUBBLES IN THIS POTION ARE HELIUM.",
        "funky": "THIS MAGIC POTION WILL BLOW YOU AWAY!",
        "candy": "THIS WILL GET YOU FEELING FLOATY!",
    },
    {
        "move": "Orangstand Sprint",
        "kong": "Lanky",
        "cranky": "I CAN RUN FASTER THAN YOU, EVEN WITH K.ROOL ON MY BACK! THAT'S WHY THIS POTION IS A MUST.",
        "funky": "WITH THIS POTION, YOU'LL BE MOVING LIKE GREASED LIGHTNING!",
        "candy": "THIS BARREL WILL GIVE YOU A BIG BURST OF SPEED.",
    },
    {
        "move": "Mini Monkey",
        "kong": "Tiny",
        "cranky": "LEAP INTO MY SPECIAL BARREL AND PREPARE TO BE AMAZED AS YOU SHRINK IN SIZE!",
        "funky": "IT'S A MAGIC BARREL THAT'LL MAKE YOU THE SIZE OF A PEA.",
        "candy": "THIS MAGIC POTION WILL MAKE YOU ITSY BITSY, ~.",
    },
    {
        "move": "Ponytail Twirl",
        "kong": "Tiny",
        "cranky": "TIME TO DO SOMETHING WITH THAT SILLY HAIR OF YOURS.",
        "funky": "TAKE A BIG LEAP AND FLY LIKE A \x01HAIRYCOPTER!\x01",
        "candy": "NO GAP WILL BE TOO FAR FOR YOU TO CROSS!",
    },
    {
        "move": "Monkeyport",
        "kong": "Tiny",
        "cranky": "IN MY DAY, YOU WOULD HAVE TO WALK UPHILL BOTH WAYS, BUT THIS WILL WARP YOU IN AN INSTANT.",
        "funky": "THIS COOL MOVE WILL SEND YOU PLACES!",
        "candy": "IT'S YOUR VERY OWN PERSONAL WARP PAD!",
    },
    {
        "move": "Hunky Chunky",
        "kong": "Chunky",
        "cranky": "ALTHOUGH I'M NOT SURE WHY YOU WOULD NEED IT, YOU'RE ALREADY BIG ENOUGH AS IT IS.",
        "funky": "DRINK THIS AND YOU'LL BULK UP BIG TIME!",
        "candy": "ONE SIP OF THIS MAGICAL DRINK CAN MAKE A BIG STRONG FELLA LIKE YOU EVEN BIGGER.",
    },
    {
        "move": "Primate Punch",
        "kong": "Chunky",
        "cranky": "YOU CAN'T SOLVE ALL YOUR PROBLEMS WITH YOUR FISTS, BUT WITH THIS, AT LEAST YOU COULD TRY.",
        "funky": "POW! KNOCK 'EM OUT COLD WITH THIS ONE, DUDE!",
        "candy": "THIS WILL LET YOU SMASH OBSTACLES AND BIG BAD GUYS ALIKE.",
    },
    {
        "move": "Gorilla Gone",
        "kong": "Chunky",
        "cranky": "WE FINALLY WON'T HAVE TO LOOK AT YOUR UGLY FEATURES! DO US A FAVOR AND USE IT AS OFTEN AS POSSIBLE, HUH?",
        "funky": "USE THIS ONE TO GO UNDERCOVER. THEY WON'T SEE YOU COMIN'!",
        "candy": "THIS IS PERFECT FOR A BIG SHY GUY LIKE YOU.",
    },
    {
        "move": "Simian Slam Upgrade",
        "kong": "~",
        "cranky": "WITH IT YOU'LL BE ABLE TO PRESS DOWN TOUGHER SWITCHES.",
        "funky": "YOU'LL BE SMASHING SWITCHES EVEN HARDER THAN BEFORE!",
        "candy": "IT WILL MAKE THAT USEFUL GROUND SLAM OF YOURS EVEN MORE POWERFUL.",
    },
    {
        "move": "Coconut Gun",
        "kong": "Donkey",
        "cranky": "NOW, TAKE IT AND DON'T POINT IT AT ME! I DON'T WANT A COCONUT IN THE FACE!",
        "funky": "THIS IS A REAL COOL COCONUT SHOOTER THAT'LL TRASH K.ROOL'S ARMY.",
        "candy": "USE IT TO FIRE YOUR BIG COCONUTS AT YOUR ENEMIES.",
    },
    {
        "move": "Peanut Popguns",
        "kong": "Diddy",
        "cranky": "NOW, TAKE IT AND DON'T POINT IT AT ME! I HATE PEANUTS!",
        "funky": "THOSE ARE SOME REAL COOL LITTLE POPGUNS THAT'LL SUIT YOUR JETPACK PERFECTLY.",
        "candy": "USE THEM TO FIRE LITTLE PEANUTS TO HURT YOUR ENEMIES AND FEED YOUR FRIENDS.",
    },
    {
        "move": "Grape Shooter",
        "kong": "Lanky",
        "cranky": "NOW, TAKE IT AND DON'T POINT IT AT ME! YOU'LL POKE AN EYE OUT WITH THIS THING!",
        "funky": "THIS IS A REAL COOL BLOWGUN THAT'LL WRECK K.ROOL'S ARMY.",
        "candy": "USE IT TO PAINT YOUR ENEMIES PURPLE.",
    },
    {
        "move": "Feather Bow",
        "kong": "Tiny",
        "cranky": "NOW, TAKE IT AND DON'T POINT IT AT ME! THOSE FEATHERS ARE POINTY!",
        "funky": "THIS IS A REAL COOL CROSSBOW THAT'LL POKE HOLES IN K.ROOL'S TOES.",
        "candy": "USE IT TO FIRE FEATHERS TO STING YOUR ENEMIES.",
    },
    {
        "move": "Pineapple Launcher",
        "kong": "Chunky",
        "cranky": "NOW, TAKE IT AND DON'T POINT IT AT ME! YOU WOULD RIP MY FEEBLE HEAD OFF WITH THESE PINEAPPLES!",
        "funky": "THIS IS A REAL COOL LAUNCHER THAT'LL BLOW HOLES IN K.ROOL'S ARMY.",
        "candy": "USE IT TO FIRE MASSIVE PINEAPPLES TO CLEAR EVERYTHING ON YOUR PATH.",
    },
    {
        "move": "Homing Ammo",
        "kong": "~",
        "cranky": "I'VE SEEN HOW POORLY YOU AIM THESE WEAPONS. YOU NEED AMMO THAT DOES THE AIMING FOR YOU.",
        "funky": "I CAN UPGRADE YOUR SHOOTER WITH HEAT-SEEKING AMMO.",
        "candy": "IT'S GOT FANCY TECHNOLOGY TO MAKE YOUR SHOTS ALWAYS HIT THEIR TARGET.",
    },
    {
        "move": "Sniper Scope",
        "kong": "~",
        "cranky": "YOUR EYESIGHT IS SOMEHOW WORSE THAN MINE. YOU NEED THIS TO SEE PAST YOUR NOSE.",
        "funky": "I CAN UPGRADE YOUR SHOOTER WITH A LONG-RANGE SCOPE.",
        "candy": "THIS WILL LET YOU ZOOM IN ON FAR AWAY TARGETS.",
    },
    {
        "move": "Ammo Belt Upgrade",
        "kong": "~",
        "cranky": "ALWAYS RUNNING OUT OF AMMO? WELL, MAYBE WITH THIS, YOU'LL FINALLY HAVE ENOUGH!",
        "funky": "TAKE A LOOK AT THIS BELT. YOU'LL CARRY SO MUCH MORE AMMO WITH IT!",
        "candy": "YOU'LL NEVER RUN OUT AGAIN WITH THIS MUCH STORAGE!",
    },
    {
        "move": "Bongo Blast",
        "kong": "Donkey",
        "cranky": "I FOUND IT LYING SOMEWHERE. IT MAKES A FUNNY SOUND WHEN YOU SMACK IT.",
        "funky": "GO ON AND PLAY A SICK BEAT, ~!",
        "candy": "I'LL SHOW YOU MY TWO BONGOS, AND HOW TO PLAY THEM, TOO.",
    },
    {
        "move": "Guitar Gazump",
        "kong": "Diddy",
        "cranky": "IT MAKES AN AWFUL RACKET. DON'T PLAY IT IN HERE!",
        "funky": "WITH THIS, YOU'RE GONNA BE A ROCKSTAR!",
        "candy": "I'LL SHOW YOU MY GUITAR AND HOW TO PLUCK THE STRINGS.",
    },
    {
        "move": "Trombone Tremor",
        "kong": "Lanky",
        "cranky": "I MADE THIS OUT OF A SPARE PIECE OF PIPE. IT MAKES A STUPID SOUND WHEN YOU BLOW IN IT.",
        "funky": "A FUNNY INSTRUMENT FOR A FUNNY DUDE!",
        "candy": "I'LL SHOW YOU MY TROMBONE AND ALL THE SLIDE POSITIONS.",
    },
    {
        "move": "Saxophone Slam",
        "kong": "Tiny",
        "cranky": "THE WHIPPERSNAPPERS CALL THIS THING A MUSICAL INSTRUMENT. THIS IS NOT MUSIC!",
        "funky": "YOU'LL JAZZ THINGS UP WITH THIS!",
        "candy": "I'LL SHOW YOU MY SAXOPHONE AND HOW TO PLAY IT, TOO.",
    },
    {
        "move": "Triangle Trample",
        "kong": "Chunky",
        "cranky": "IT'S JUST SOME JUNK METAL. YOU COULD TRY SMACKING IT, I GUESS.",
        "funky": "DING DING, LOSERS! SMACK THIS AND K.ROOL'S EARS WILL BE RINGING FOR DAYS.",
        "candy": "I'LL SHOW YOU MY SPECIAL TRIANGLE AND HOW TO HIT IT JUST RIGHT.",
    },
    {
        "move": "Instrument Upgrade",
        "kong": "~",
        "cranky": "YOU'LL BE ABLE TO MAKE EVEN MORE RACKET THAN BEFORE.",
        "funky": "MORE MUSICAL ENERGY SO YOU CAN JAM OUT FOR LONGER!",
        "candy": "I HAVE AN INSTRUMENT UPGRADE AVAILABLE FOR YOU.",
    },
    {
        "move": "Dive Barrel",
        "kong": "~",
        "cranky": "YOU'LL BE SUBMERGING YOURSELF LIKE THEM SUBMARINES IN GALLEON.",
        "funky": "YOU'LL BE GLIDING UNDERWATER GROOVIER THAN BEFORE.",
        "candy": "I'LL SHOW YOU HOW TO LAST LONGER UNDERWATER.",
    },
    {
        "move": "Orange Barrel",
        "kong": "~",
        "cranky": "SET THE TIMER TO 5 AND THROW THIS FRUIT LIKE IT'S A WORMS GAME.",
        "funky": "YOU BETTER CALL THE BOMB SQUAD, CAUSE THESE FRUIT ARE LIKE DYNAMITE.",
        "candy": "I MAY HAVE MELONS, BUT I HAVE MORE EXPLOSIVE FRUIT LIKE THESE BAD BOYS.",
    },
    {
        "move": "Barrel Barrel",
        "kong": "~",
        "cranky": "YOU WON'T EVEN BE BREAKING A SWEAT LIFTING UP BARRELS.",
        "funky": "YOU'LL BE ABLE TO JAM OUT WITH DOGADON BY THROWING BARRELS IN HIS FACE.",
        "candy": "I'M SURE YOU'LL BE ABLE TO PICK UP THOSE LARGE BARRELS FOR ME.",
    },
    {
        "move": "Vine Barrel",
        "kong": "~",
        "cranky": "I DON'T REMEMBER THIS GAME BEING CALLED JUNGLE SWING, BUT THIS WILL CERTAINLY LET YOU SWING.",
        "funky": "SOME WOULD CALL THIS THE TWENTIES, CAUSE YOU GONNA BE SWINGING.",
        "candy": "THIS MOVE WILL ALLOW YOU TO GRAB ROPES.",
    },
    {
        "move": "Climbing",
        "kong": "~",
        "cranky": "I DON'T REMEMBER THIS GAME BEING CALLED JUNGLE CLIMBER, BUT THIS WILL CERTAINLY LET YOU PAVE THE PATH TO GOOD ASCENSIONS.",
        "funky": "ARE YOU TINY KONG, CAUSE IT LOOKS LIKE THIS WILL ALLOW YOU TO CLIMB UP TREES.",
        "candy": "THIS MOVE WILL ALLOW YOU TO CLIMB TREES.",
    },
    {
        "move": "Camera Solo",
        "kong": "~",
        "cranky": "WITH THAT DEVICE, YOU MIGHT AS WELL CALL ME PROFESSOR OAK! WONDERFUL.",
        "funky": "THIS DEVICE WILL ALLOW YOU TO TAKE THEM HIGH RESOLUTION POLAROIDS.",
        "candy": "YOU'LL BE ABLE TO TAKE PLENTY OF PICTURES OF ME!",
    },
    {
        "move": "Shockwave Solo",
        "kong": "~",
        "cranky": "THIS MOVE WILL LET YOU UNEARTH THOSE DASTARDLY MOUNDS WITH SOME LETTERS ON THEM.",
        "funky": "WITH THIS MOVE, YOU'LL BE SHOCKING THE REST OF THE COMPETITION IN THOSE CROWNS.",
        "candy": "I DIDN'T KNOW YOU HAD SO MUCH ENERGY IN YOU TO RELEASE SUCH A POWERFUL ENERGY CHARGE.",
    },
    {
        "move": "Shockwave Camera Combo",
        "kong": "~",
        "cranky": "TWO MOVES IN ONE. BACK IN MY DAY YOU HAD TO PAY DOUBLE THE CREDITS FOR THAT.",
        "funky": "I GOT A BONZA DEAL FOR YOU. TWO MOVES FOR THE PRICE OF... TWO. WHAT DO YOU SAY?",
        "candy": "TWO MOVES? WELL I GUESS SINCE YOU'VE BEEN WORKING HARD, WHAT DO YOU SAY?",
    },
    {
        "move": "Golden Banana",
        "kong": "~",
        "cranky": "ANOTHER GOLDEN BANANA. WHY DO YOU NEED SO MANY OF THESE STUPID THINGS?",
        "funky": "FOUND ANOTHER GOLDEN BANANA FOR YOU, MY DUDE!",
        "candy": "A SHINY GOLDEN BANANA. I KNOW THEY'RE YOUR FAVOURITE!",
    },
    {
        "move": "Battle Crown",
        "kong": "~",
        "cranky": "BACK IN MY DAY, YOU WOULD HAVE TO FIGHT IN THE RING FOR A PRIZE LIKE THAT!",
        "funky": "I FOUND THIS SICK LOOKIN' CROWN FOR YOU!",
        "candy": "HERE'S A PRETTY CROWN SO YOU CAN LOOK LIKE THE PRINCESS YOU ARE!",
    },
    {
        "move": "Banana Medal",
        "kong": "~",
        "cranky": "ONE MORE MEDAL. MAYBE ONE DAY YOU'LL FINALLY BE WORTHY ENOUGH TO PLAY MY SPECIAL GAME!",
        "funky": "HERE'S A SHINY BANANA MEDAL! THOSE GO FOR A PRETTY PENNY!",
        "candy": "A BEAUTIFUL BANANA MEDAL TO PUT AROUND YOUR NECK.",
    },
    {
        "move": "Boss Key",
        "kong": "~",
        "cranky": "THIS COULD HELP YOU OPEN UP SOME MORE LEVELS SO YOU CAN FINALLY STOP RUNNING IN CIRCLES.",
        "funky": "K. ROOL DOESN'T WANT ME TO GIVE YOU THIS! I HEAR IT CAN OPEN WHOLE NEW LEVELS!",
        "candy": "I HAVE THIS PRECIOUS KEY FOR YOU. MAYBE IT'S THE KEY TO MY HEART?",
    },
    {
        "move": "Blueprint",
        "kong": "~",
        "cranky": "THE OLD SNIDE WILL KNOW WHAT TO DO WITH THIS.",
        "funky": "HIT MY OLD PAL SNIDE'S PLACE AND HE'LL HOOK YOU UP WITH SOMETHING GOOD!",
        "candy": "GO PAY MY GOOD FRIEND SNIDE A VISIT, WILL YA?",
    },
    {
        "move": "Nintendo Coin",
        "kong": "~",
        "cranky": "WHAT! NOT THE NINTENDO COIN! YOU SHOULD WORK HARD TO HAVE THAT! THIS GAME IS PAY TO WIN!",
        "funky": "YOU GIVE ME COINS WITH BANANAS ON THEM, I GIVE YOU A COIN WITH A NINTENDO LOGO ON IT!",
        "candy": "YOU WANT TO TRADE COINS FOR ANOTHER COIN? SURE, WHY NOT. THIS ONE HAS A BIG N ON IT.",
    },
    {
        "move": "Rareware Coin",
        "kong": "~",
        "cranky": "WHAT! NOT THE RAREWARE COIN! YOU NEED TO PLAY MY BONUS GAME TO HAVE THAT! THIS GAME IS PAY TO WIN!",
        "funky": "YOU GIVE ME COINS WITH BANANAS ON THEM, I GIVE YOU A COIN WITH A RAREWARE LOGO ON IT!",
        "candy": "YOU WANT TO TRADE COINS FOR ANOTHER COIN? SURE, WHY NOT. THIS ONE HAS A BIG R ON IT.",
    },
    {
        "move": "Bean",
        "kong": "~",
        "cranky": "CHUCK THIS INTO FERTILE GROUND AND WATER IT WELL.",
        "funky": "IT'S A BIG OL' BEAN, DUDE!",
        "candy": "CAN YOU PLANT THIS SEED SOMEWHERE NICE FOR ME?",
    },
    {
        "move": "Pearl",
        "kong": "~",
        "cranky": "I'VE GOT THIS SHINY BALL. I WAS TOLD SOME MERMAID LOST IT.",
        "funky": "WHAT'S THAT I GOT? A SHINY LITTLE PEARL FOUND DEEP UNDERWATER!",
        "candy": "I HAVE A PRECIOUS GEM FOR YOU, BUT IT'S NOT GONNA BE CHEAP!",
    },
    {
        "move": "Kong",
        "kong": "~",
        "cranky": "I FOUND YOUR FLEA-BITTEN FRIEND MOPING AROUND AIMLESSLY. I'M NOT YOUR BABYSITTER!",
        "funky": "GUESS WHAT! WE CAN RECRUIT A NEW MEMBER TO THE CREW!",
        "candy": "I'VE BEEN SPENDING MY TIME WITH A FRIEND OF YOURS. YOU CAN HAVE THEM BACK IF YOU WANT!",
    },
    {
        "move": "Fairy",
        "kong": "~",
        "cranky": "IT'S A LOST FAIRY FOR THE GREAT BANANA FAIRY.",
        "funky": "I HEARD YOU BEEN LOOKIN' FOR THE LOST BANANA FAIRIES. WELL, I FOUND ONE!",
        "candy": "THIS POOR LITTLE FAIRY NEEDS TO GET BACK HOME. WILL YOU HELP HER?",
    },
    {
        "move": "Ice Trap",
        "kong": "~",
        "cranky": "THIS ITEM WAS DONATED BY A BARON K. ROOLENSTEIN. LOOKS FISHY BUT YOU CAN HAVE IT.",
        "funky": "THIS ONE LOOKS A BIT STRANGE MY DUDE. YOU CAN HAVE IT THOUGH!",
        "candy": "I AM NOT TOO SURE ABOUT THIS ITEM. ARE YOU SURE YOU WANT IT?",
    },
    {
        "move": "Hint",
        "kong": "~",
        "cranky": "IT'S A RIDDLE FOR 30 PICORATS. WHAT IS THE CONVERSION RATE FROM PICORATS TO COINS?",
        "funky": "THIS ONE WILL HELP YOU ON YOUR QUEST MY DUDE. GET YOUR PEN AND PAPER OUT!",
        "candy": "IT'S A PIECE OF PAPER. I THINK WRINKLY DROPPED IT IN HER SAVE CAVE.",
    },
    {
        "move": "Not enough coins - Special Move",
        "kong": "~",
        "cranky": "YOU'RE UNLUCKY TO BE SO POOR YOU CAN'T AFFORD MY SPECIAL MOVE.",
        "funky": "'FRAID I CAN'T JUST GIVE IT TO YA, THOUGH. SPECIAL MOVES DON'T GROW ON TREES!",
        "candy": "BUT YOU'LL NEED TO SCRAPE TOGETHER SOME MORE COINS TO GET MY SPECIAL MOVE.",
    },
    {
        "move": "Not enough coins - Slam",
        "kong": "~",
        "cranky": "YOU'RE UNLUCKY TO BE SO POOR YOU CAN'T AFFORD TO UPGRADE YOUR GROUND SLAM.",
        "funky": "'FRAID I CAN'T JUST GIVE IT TO YA, THOUGH. YOU'LL HAVE TO KEEP YOUR WEAK SLAM FOR NOW!",
        "candy": "BUT YOU'LL NEED TO SCRAPE TOGETHER SOME MORE COINS TO IMPROVE YOUR SLAM.",
    },
    {
        "move": "Not enough coins - Gun",
        "kong": "~",
        "cranky": "YOU'RE UNLUCKY TO BE SO POOR YOU CAN'T AFFORD THIS WEAPON.",
        "funky": "'FRAID I CAN'T JUST GIVE IT TO YA, THOUGH. MY COOL WEAPONS DON'T GROW ON TREES!",
        "candy": "BUT YOU'LL NEED TO SCRAPE TOGETHER SOME MORE COINS TO GET THIS WEAPON.",
    },
    {
        "move": "Not enough coins - Gun Upgrade",
        "kong": "~",
        "cranky": "YOU'RE UNLUCKY TO BE SO POOR YOU CAN'T AFFORD THIS WEAPON UPGRADE.",
        "funky": "'FRAID I CAN'T JUST GIVE IT TO YA, THOUGH. MY COOL WEAPON UPGRADES DON'T GROW ON TREES!",
        "candy": "BUT YOU'LL NEED TO SCRAPE TOGETHER SOME MORE COINS TO GET THIS WEAPON UPGRADE.",
    },
    {
        "move": "Not enough coins - Ammo Belt",
        "kong": "~",
        "cranky": "YOU'RE UNLUCKY TO BE SO POOR YOU CAN'T AFFORD TO UPGRADE YOUR AMMO COUNT.",
        "funky": "'FRAID I CAN'T JUST GIVE IT TO YA, THOUGH. AMMO BELTS DON'T GROW ON TREES!",
        "candy": "BUT YOU'LL NEED TO SCRAPE TOGETHER SOME MORE COINS TO GET MORE AMMO.",
    },
    {
        "move": "Not enough coins - Instrument",
        "kong": "~",
        "cranky": "YOU'RE UNLUCKY TO BE SO POOR YOU CAN'T AFFORD TO UPGRADE YOUR INSTRUMENT.",
        "funky": "'FRAID I CAN'T JUST GIVE IT TO YA, THOUGH. MUSICAL ENERGY DOESN'T GROW ON TREES!",
        "candy": "BUT YOU'LL NEED TO SCRAPE TOGETHER SOME MORE COINS TO UPGRADE YOUR INSTRUMENT.",
    },
    {
        "move": "Not enough coins - Training Barrels",
        "kong": "~",
        "cranky": "YOU'RE UNLUCKY TO BE SO POOR YOU CAN'T AFFORD THIS BASIC MOVE.",
        "funky": "'FRAID I CAN'T JUST GIVE IT TO YA, THOUGH. BASIC MOVES DON'T GROW ON TREES!",
        "candy": "BUT YOU'LL NEED TO SCRAPE TOGETHER SOME MORE COINS TO GET THIS BASIC MOVE.",
    },
    {
        "move": "Not enough coins - Fairy Moves",
        "kong": "~",
        "cranky": "YOU'RE UNLUCKY TO BE SO POOR YOU CAN'T AFFORD THIS FAIRY MOVE.",
        "funky": "'FRAID I CAN'T JUST GIVE IT TO YA, THOUGH. FAIRY MOVES DON'T GROW ON TREES!",
        "candy": "BUT YOU'LL NEED TO SCRAPE TOGETHER SOME MORE COINS TO GET THIS FAIRY MOVE.",
    },
    {
        "move": "Not enough coins - Item",
        "kong": "~",
        "cranky": "YOU'RE UNLUCKY TO BE SO POOR YOU CAN'T AFFORD THIS MAJOR ITEM.",
        "funky": "'FRAID I CAN'T JUST GIVE IT TO YA, THOUGH. MAJOR ITEMS DON'T GROW ON TREES!",
        "candy": "BUT YOU'LL NEED TO SCRAPE TOGETHER SOME MORE COINS TO GET THIS MAJOR ITEM.",
    },
    {
        "move": "Not enough coins - GB",
        "kong": "~",
        "cranky": "YOU'RE UNLUCKY TO BE SO POOR YOU CAN'T AFFORD THIS GOLDEN BANANA.",
        "funky": "'FRAID I CAN'T JUST GIVE IT TO YA, THOUGH. GOLDEN BANANAS DON'T GROW ON TREES!",
        "candy": "BUT YOU'LL NEED TO SCRAPE TOGETHER SOME MORE COINS TO GET THIS GOLDEN BANANA.",
    },
    {
        "move": "Not enough coins - BP",
        "kong": "~",
        "cranky": "YOU'RE UNLUCKY TO BE SO POOR YOU CAN'T AFFORD THIS BLUEPRINT.",
        "funky": "'FRAID I CAN'T JUST GIVE IT TO YA, THOUGH. BLUEPRINTS DON'T GROW ON TREES!",
        "candy": "BUT YOU'LL NEED TO SCRAPE TOGETHER SOME MORE COINS TO GET THIS BLUEPRINT.",
    },
    {
        "move": "Not enough coins - Medal",
        "kong": "~",
        "cranky": "YOU'RE UNLUCKY TO BE SO POOR YOU CAN'T AFFORD THIS BANANA MEDAL.",
        "funky": "'FRAID I CAN'T JUST GIVE IT TO YA, THOUGH. BANANA MEDALS DON'T GROW ON TREES!",
        "candy": "BUT YOU'LL NEED TO SCRAPE TOGETHER SOME MORE COINS TO GET THIS BANANA MEDAL.",
    },
    {
        "move": "Not enough coins - Kong",
        "kong": "~",
        "cranky": "YOU'RE UNLUCKY TO BE SO POOR YOU CAN'T AFFORD TO SAVE YOUR FRIEND.",
        "funky": "'FRAID I CAN'T JUST GIVE IT TO YA, THOUGH. FRIENDS DON'T GROW ON TREES!",
        "candy": "BUT YOU'LL NEED TO SCRAPE TOGETHER SOME MORE COINS TO RECRUIT YOUR FRIEND.",
    },
]

pre_amble = {
    "cranky": "YOU'RE BACK AGAIN, ~? YOU'RE LUCKY I HAVE SOMETHING FOR YOU. ",
    "funky": "WHAT'S UP, ~-DUDE! I JUST FINISHED MAKIN' THIS! ",
    "candy": "WHY, ~, HAVE I GOT A TREAT FOR YOU. ",
}

moves = [
    "Baboon Blast",
    "Strong Kong",
    "Gorilla Grab",
    "Chimpy Charge",
    "Rocketbarrel",
    "Simian Spring",
    "Orangstand",
    "Baboon Balloon",
    "Orangstand Sprint",
    "Mini Monkey",
    "Ponytail Twirl",
    "Monkeyport",
    "Hunky Chunky",
    "Primate Punch",
    "Gorilla Gone",
    "Simian Slam Upgrade",
    "Coconut Gun",
    "Peanut Popguns",
    "Grape Shooter",
    "Feather Bow",
    "Pineapple Launcher",
    "Homing Ammo",
    "Sniper Scope",
    "Ammo Belt Upgrade",
    "Bongo Blast",
    "Guitar Gazump",
    "Trombone Tremor",
    "Saxophone Slam",
    "Triangle Trample",
    "Instrument Upgrade",
    "Dive Barrel",
    "Orange Barrel",
    "Barrel Barrel",
    "Vine Barrel",
    "Camera Solo",
    "Shockwave Solo",
    "Shockwave Camera Combo",
    "Not enough coins - Special Move",
    "Not enough coins - Slam",
    "Not enough coins - Gun",
    "Not enough coins - Ammo Belt",
    "Not enough coins - Instrument",
    "Not enough coins - Training Barrels",
    "Not enough coins - Fairy Moves",
]

shop_owners = ["cranky", "funky", "candy"]

hint_text = []

for move in move_hints:
    for shop in shop_owners:
        hint_pre = pre_amble[shop]
        hint_post = move[shop]
        hint_text.append([{"text": [f"{hint_pre}{hint_post}"]}])

writeText(
    "dolby_text.bin",
    [[{"text": ["DONKEY KONG 64 RANDOMIZER"]}], [{"text": ["DEVELOPERS - 2DOS, BALLAAM, BISMUTH, CFOX, KILLKLLI, LRAUQ, SHADOWSHINE, ZNERNICUS"]}], [{"text": ["DK64RANDOMIZER.COM"]}]],
)

writeText("custom_text.bin", hint_text)

writeText(
    "dk_text.bin",
    [
        [{"text": ["WHAT DID CRANKY MEAN ABOUT TRAINING? DONKEY ALL CONFUSED..."]}],
        [{"text": ["AW NO! SO THAT WHAT CRANKY MEAN ABOUT REPTILE...", "DONKEY NOT BELIEVE IT. KING K.ROOL? WE FINISHED K. ROOL OFF IN LAST GAME!"]}],
        [
            {"text": ["OKAY!", "DONKEY IS FREE NOW. THANK YOU, MY FRIEND.", "DONKEY CAN COLLECT YELLOW BANANAS."]},
            {"text": [Icons.BananaDK_0]},
            {"text": ["DONKEY WILL BE INSIDE THE TAG BARREL UNTIL YOU NEED MY HELP."]},
        ],
    ],
)

move_names = [
    MoveName("Simian Slam", MoveTypes.slam, "Buttus Bashium"),
    MoveName("Super Simian Slam", MoveTypes.slam, "Big Buttus Bashium"),
    MoveName("Super Duper Simian Slam", MoveTypes.slam, "Bigga Buttus Bashium"),
    MoveName("Baboon Blast", MoveTypes.special, "Barrelum Perilous"),
    MoveName("Strong Kong", MoveTypes.special, "Strongum Kongus"),
    MoveName("Gorilla Grab", MoveTypes.special, "Simium Strainus"),
    MoveName("Chimpy Charge", MoveTypes.special, "Hurtus Cranium"),
    MoveName("Rocketbarrel Boost", MoveTypes.special, "Boostum Highus"),
    MoveName("Simian Spring", MoveTypes.special, "Leapus Largium"),
    MoveName("Orangstand", MoveTypes.special, "Palmus Walkum"),
    MoveName("Baboon Balloon", MoveTypes.special, "Baboonus Balloonus"),
    MoveName("Orangstand Sprint", MoveTypes.special, "Palmus Dashium"),
    MoveName("Mini Monkey", MoveTypes.special, "Kongum Smallus"),
    MoveName("Pony Tail Twirl", MoveTypes.special, "Roundum Roundus"),
    MoveName("Monkeyport", MoveTypes.special, "Warpum Craftious"),
    MoveName("Hunky Chunky", MoveTypes.special, "Kremlinous Crushum"),
    MoveName("Primate Punch", MoveTypes.special, "Sandwichium Knucklus"),
    MoveName("Gorilla Gone", MoveTypes.special, "Wheresim Gonium"),
    MoveName("Coconut Shooter", MoveTypes.weapon),
    MoveName("Peanut Popguns", MoveTypes.weapon),
    MoveName("Grape Shooter", MoveTypes.weapon),
    MoveName("Feather Bow", MoveTypes.weapon),
    MoveName("Pineapple Launcher", MoveTypes.weapon),
    MoveName("Bongo Blast", MoveTypes.instrument),
    MoveName("Guitar Gazump", MoveTypes.instrument),
    MoveName("Trombone Tremor", MoveTypes.instrument),
    MoveName("Saxophone Slam", MoveTypes.instrument),
    MoveName("Triangle Trample", MoveTypes.instrument),
    MoveName("Homing Ammo", MoveTypes.gun_upgrade),
    MoveName("Sniper Scope", MoveTypes.gun_upgrade),
    MoveName("Ammo Belt 1", MoveTypes.ammo_belt),
    MoveName("Ammo Belt 2", MoveTypes.ammo_belt),
    MoveName("3rd Melon", MoveTypes.instrument),
    MoveName("Instrument Upgrade 1", MoveTypes.instrument),
    MoveName("Instrument Upgrade 2", MoveTypes.instrument),
    MoveName("Diving", MoveTypes.flag),
    MoveName("Orange Throwing", MoveTypes.flag),
    MoveName("Barrel Throwing", MoveTypes.flag),
    MoveName("Vine Swinging", MoveTypes.flag),
    MoveName("Fairy Camera", MoveTypes.flag),
    MoveName("Shockwave", MoveTypes.flag),
    MoveName("Fairy Camera and Shockwave", MoveTypes.flag),
    MoveName("Golden Banana", MoveTypes.gb),  # 60
    MoveName("Banana Medal", MoveTypes.flag),  # 61
    MoveName("Donkey Blueprint", MoveTypes.flag),  # 62
    MoveName("Diddy Blueprint", MoveTypes.flag),  # 63
    MoveName("Lanky Blueprint", MoveTypes.flag),  # 64
    MoveName("Tiny Blueprint", MoveTypes.flag),  # 65
    MoveName("Chunky Blueprint", MoveTypes.flag),  # 66
    MoveName("Nintendo Coin", MoveTypes.flag),  # 67
    MoveName("Rareware Coin", MoveTypes.flag),  # 68
    MoveName("Boss Key", MoveTypes.flag),  # 69
    MoveName("Battle Crown", MoveTypes.flag),  # 70
    MoveName("Bean", MoveTypes.flag),  # 71
    MoveName("Key 1", MoveTypes.flag),  # 72
    MoveName("Key 2", MoveTypes.flag),  # 73
    MoveName("Key 3", MoveTypes.flag),  # 74
    MoveName("Key 4", MoveTypes.flag),  # 75
    MoveName("Key 5", MoveTypes.flag),  # 76
    MoveName("Key 6", MoveTypes.flag),  # 77
    MoveName("Key 7", MoveTypes.flag),  # 78
    MoveName("Key 8", MoveTypes.flag),  # 79
    MoveName("Pearl", MoveTypes.flag),  # 80
    MoveName("Donkey Kong", MoveTypes.flag),  # 81
    MoveName("Diddy Kong", MoveTypes.flag),  # 82
    MoveName("Lanky Kong", MoveTypes.flag),  # 83
    MoveName("Tiny Kong", MoveTypes.flag),  # 84
    MoveName("Chunky Kong", MoveTypes.flag),  # 85
    MoveName("Banana Fairy", MoveTypes.flag),  # 86
    MoveName("Rainbow Coin", MoveTypes.flag),  # 87
    MoveName("Ice Trap", MoveTypes.flag),  # 88
    MoveName("Cranky Kong", MoveTypes.flag),  # 89
    MoveName("Funky Kong", MoveTypes.flag),  # 90
    MoveName("Candy Kong", MoveTypes.flag),  # 91
    MoveName("Snide", MoveTypes.flag),  # 92
    MoveName("Hint", MoveTypes.flag),  # 93
    MoveName("Climbing", MoveTypes.flag),  # 94
]

move_names_arr = []
for move in move_names:
    init_len = len(move_names_arr)
    move_names_arr.append([{"text": [move.name.upper()]}])
    if move.latin is not None:
        move_names_arr.append([{"text": [f"({move.latin.upper()})"]}])

index_data = {
    "slam": {"indexes": [], "arr_name": "SimianSlamNames", "has_latin": True},
    "special": {"indexes": [], "arr_name": "SpecialMovesNames", "has_latin": True},
    "gun": {"indexes": [], "arr_name": "GunNames", "has_latin": False},
    "gun_upg": {"indexes": [], "arr_name": "GunUpgNames", "has_latin": False},
    "ammo_belt": {"indexes": [], "arr_name": "AmmoBeltNames", "has_latin": False},
    "instrument": {"indexes": [], "arr_name": "InstrumentNames", "has_latin": False},
    "ins_upg": {"indexes": [], "arr_name": "InstrumentUpgNames", "has_latin": False},
}
for kong_index in range(5):
    # Special Moves
    for move_index in range(4):
        for latin_index in range(2):
            if move_index == 0:
                index_data["special"]["indexes"].append(0)
            else:
                index_data["special"]["indexes"].append(6 + latin_index + (2 * (move_index - 1)) + (6 * kong_index))
    # Guns
    index_data["gun"]["indexes"].append(0x24 + kong_index)
    # Instruments
    index_data["instrument"]["indexes"].append(0x29 + kong_index)
# Slam
for move_index in range(4):
    for latin_index in range(2):
        if move_index == 0:
            index_data["slam"]["indexes"].append(0)
        else:
            index_data["slam"]["indexes"].append(latin_index + (2 * (move_index - 1)))
# Gun Upg
for move_index in range(4):
    if move_index < 2:
        index_data["gun_upg"]["indexes"].append(0)
    else:
        index_data["gun_upg"]["indexes"].append((move_index - 2) + 0x2E)
# Ammo Belt
for move_index in range(3):
    if move_index == 0:
        index_data["ammo_belt"]["indexes"].append(0)
    else:
        index_data["ammo_belt"]["indexes"].append((move_index - 1) + 0x30)
# Instrument Upgrades
index_data["ins_upg"]["indexes"] = [0x0, 0x0, 0x33, 0x32, 0x34]

text_enum = [
    "ITEMTEXT_SLAM1",  # 0x000
    "ITEMTEXT_SLAM1_LATIN",  # 0x001
    "ITEMTEXT_SLAM2",  # 0x002
    "ITEMTEXT_SLAM2_LATIN",  # 0x003
    "ITEMTEXT_SLAM3",  # 0x004
    "ITEMTEXT_SLAM3_LATIN",  # 0x005
    "ITEMTEXT_BBLAST",  # 0x006
    "ITEMTEXT_BBLAST_LATIN",  # 0x007
    "ITEMTEXT_SKONG",  # 0x008
    "ITEMTEXT_SKONG_LATIN",  # 0x009
    "ITEMTEXT_GGRAB",  # 0x00A
    "ITEMTEXT_GGRAB_LATIN",  # 0x00B
    "ITEMTEXT_CCHARGE",  # 0x00C
    "ITEMTEXT_CCHARGE_LATIN",  # 0x00D
    "ITEMTEXT_RBARREL",  # 0x00E
    "ITEMTEXT_RBARREL_LATIN",  # 0x00F
    "ITEMTEXT_SSPRING",  # 0x010
    "ITEMTEXT_SSPRING_LATIN",  # 0x011
    "ITEMTEXT_OSTAND",  # 0x012
    "ITEMTEXT_OSTAND_LATIN",  # 0x013
    "ITEMTEXT_BBALLOON",  # 0x014
    "ITEMTEXT_BBALLOON_LATIN",  # 0x015
    "ITEMTEXT_OSPRINT",  # 0x016
    "ITEMTEXT_OSPRINT_LATIN",  # 0x017
    "ITEMTEXT_MMONKEY",  # 0x018
    "ITEMTEXT_MMONKEY_LATIN",  # 0x019
    "ITEMTEXT_PTT",  # 0x01A
    "ITEMTEXT_PTT_LATIN",  # 0x01B
    "ITEMTEXT_MPORT",  # 0x01C
    "ITEMTEXT_MPORT_LATIN",  # 0x01D
    "ITEMTEXT_HCHUNKY",  # 0x01E
    "ITEMTEXT_HCHUNKY_LATIN",  # 0x01F
    "ITEMTEXT_PPUNCH",  # 0x020
    "ITEMTEXT_PPUNCH_LATIN",  # 0x021
    "ITEMTEXT_GGONE",  # 0x022
    "ITEMTEXT_GGONE_LATIN",  # 0x023
    "ITEMTEXT_COCONUT",  # 0x024
    "ITEMTEXT_PEANUT",  # 0x025
    "ITEMTEXT_GRAPE",  # 0x026
    "ITEMTEXT_FEATHER",  # 0x027
    "ITEMTEXT_PINEAPPLE",  # 0x028
    "ITEMTEXT_BONGOS",  # 0x029
    "ITEMTEXT_GUITAR",  # 0x02A
    "ITEMTEXT_TROMBONE",  # 0x02B
    "ITEMTEXT_SAX",  # 0x02C
    "ITEMTEXT_TRIANGLE",  # 0x02D
    "ITEMTEXT_HOMING",  # 0x02E
    "ITEMTEXT_SNIPER",  # 0x02F
    "ITEMTEXT_BELT1",  # 0x030
    "ITEMTEXT_BELT2",  # 0x031
    "ITEMTEXT_THIRDMELON",  # 0x032
    "ITEMTEXT_INSUPGRADE1",  # 0x033
    "ITEMTEXT_INSUPGRADE2",  # 0x034
    "ITEMTEXT_DIVE",  # 0x035
    "ITEMTEXT_ORANGE",  # 0x036
    "ITEMTEXT_BARREL",  # 0x037
    "ITEMTEXT_VINE",  # 0x038
    "ITEMTEXT_CAMERA",  # 0x039
    "ITEMTEXT_SHOCKWAVE",  # 0x03A
    "ITEMTEXT_CAMERACOMBO",  # 0x03B
    "ITEMTEXT_BANANA",  # 0x03C
    "ITEMTEXT_MEDAL",  # 0x03D
    "ITEMTEXT_BLUEPRINT_DK",  # 0x03E
    "ITEMTEXT_BLUEPRINT_DIDDY",  # 0x03F
    "ITEMTEXT_BLUEPRINT_LANKY",  # 0x040
    "ITEMTEXT_BLUEPRINT_TINY",  # 0x041
    "ITEMTEXT_BLUEPRINT_CHUNKY",  # 0x042
    "ITEMTEXT_NINTENDO",  # 0x043
    "ITEMTEXT_RAREWARE",  # 0x044
    "ITEMTEXT_KEYGENERIC",  # 0x045
    "ITEMTEXT_CROWN",  # 0x046
    "ITEMTEXT_BEAN",  # 0x047
    "ITEMTEXT_KEY1",  # 0x048
    "ITEMTEXT_KEY2",  # 0x049
    "ITEMTEXT_KEY3",  # 0x04A
    "ITEMTEXT_KEY4",  # 0x04B
    "ITEMTEXT_KEY5",  # 0x04C
    "ITEMTEXT_KEY6",  # 0x04D
    "ITEMTEXT_KEY7",  # 0x04E
    "ITEMTEXT_KEY8",  # 0x04F
    "ITEMTEXT_PEARL",  # 0x050
    "ITEMTEXT_KONG_DK",  # 0x051
    "ITEMTEXT_KONG_DIDDY",  # 0x052
    "ITEMTEXT_KONG_LANKY",  # 0x053
    "ITEMTEXT_KONG_TINY",  # 0x054
    "ITEMTEXT_KONG_CHUNKY",  # 0x055
    "ITEMTEXT_FAIRY",  # 0x056
    "ITEMTEXT_RAINBOWCOIN",  # 0x057
    "ITEMTEXT_FAKEITEM",  # 0x058
    "ITEMTEXT_CRANKYITEM",  # 0x059
    "ITEMTEXT_FUNKYITEM",  # 0x05A
    "ITEMTEXT_CANDYITEM",  # 0x05B
    "ITEMTEXT_SNIDEITEM",  # 0x05C
    "ITEMTEXT_HINTITEM",  # 0x05D
    "ITEMTEXT_CLIMBING",  # 0x05E
]


# Item Locations
class ItemReference:
    """Class to store information regarding an item's location."""

    def __init__(self, item: str, locations):
        """Initialize with given parameters."""
        self.item = item
        self.locations = [locations] if isinstance(locations, str) else locations


location_references = [
    # DK Moves
    ItemReference("Baboon Blast", "DK Japes Cranky"),
    ItemReference("Strong Kong", "DK Aztec Cranky"),
    ItemReference("Gorilla Grab", "DK Factory Cranky"),
    ItemReference("Coconut Gun", "DK Japes Funky"),
    ItemReference("Bongo Blast", "DK Aztec Candy"),
    # Diddy Moves
    ItemReference("Chimpy Charge", "Diddy Japes Cranky"),
    ItemReference("Rocketbarrel Boost", "Diddy Aztec Cranky"),
    ItemReference("Simian Spring", "Diddy Factory Cranky"),
    ItemReference("Peanut Popguns", "Diddy Japes Funky"),
    ItemReference("Guitar Gazump", "Diddy Aztec Candy"),
    # Lanky Moves
    ItemReference("Orangstand", "Lanky Japes Cranky"),
    ItemReference("Baboon Balloon", "Lanky Factory Cranky"),
    ItemReference("Orangstand Sprint", "Lanky Caves Cranky"),
    ItemReference("Grape Shooter", "Lanky Japes Funky"),
    ItemReference("Trombone Tremor", "Lanky Aztec Candy"),
    # Tiny Moves
    ItemReference("Mini Monkey", "Tiny Japes Cranky"),
    ItemReference("Pony Tail Twirl", "Tiny Factory Cranky"),
    ItemReference("Monkeyport", "Tiny Caves Cranky"),
    ItemReference("Feather Bow", "Tiny Japes Funky"),
    ItemReference("Saxophone Slam", "Tiny Aztec Candy"),
    # Chunky Moves
    ItemReference("Hunky Chunky", "Chunky Japes Cranky"),
    ItemReference("Primate Punch", "Chunky Factory Cranky"),
    ItemReference("Gorilla Gone", "Chunky Caves Cranky"),
    ItemReference("Pineapple Launcher", "Chunky Japes Funky"),
    ItemReference("Triangle Trample", "Chunky Aztec Candy"),
    # Gun Upgrades and Funky Moves
    ItemReference("Homing Ammo", "Shared Forest Funky"),
    ItemReference("Sniper Scope", "Shared Castle Funky"),
    ItemReference("Progressive Ammo Belt", ["Shared Factory Funky", "Shared Caves Funky"]),
    ItemReference("Fairy Camera", "Banana Fairy Gift"),
    ItemReference("Shockwave", "Banana Fairy Gift"),
    # Basic Moves
    ItemReference("Diving", "Dive Barrel"),
    ItemReference("Orange Throwing", "Orange Barrel"),
    ItemReference("Barrel Throwing", "Barrel Barrel"),
    ItemReference("Vine Swinging", "Vine Barrel"),
    ItemReference("Climbing", "Starting Move"),
    # Instrument Upgrades & Slams
    ItemReference("Progressive Instrument Upgrade", ["Shared Galleon Candy", "Shared Caves Candy", "Shared Castle Candy"]),
    ItemReference("Progressive Slam", ["Shared Isles Cranky", "Shared Forest Cranky", "Shared Castle Cranky"]),
    # Kongs
    ItemReference("Donkey Kong", "Starting Kong"),
    ItemReference("Diddy Kong", "Japes Diddy Cage"),
    ItemReference("Lanky Kong", "Llama Lanky Cage"),
    ItemReference("Tiny Kong", "Aztec Tiny Cage"),
    ItemReference("Chunky Kong", "Factory Chunky Cage"),
    # Shopkeepers
    ItemReference("Cranky Kong", "Starting Item"),
    ItemReference("Candy Kong", "Starting Item"),
    ItemReference("Funky Kong", "Starting Item"),
    ItemReference("Snide", "Starting Item"),
    # Early Keys
    ItemReference("Key 1", "Japes Boss Defeated"),
    ItemReference("Key 2", "Aztec Boss Defeated"),
    ItemReference("Key 3", "Factory Boss Defeated"),
    ItemReference("Key 4", "Galleon Boss Defeated"),
    # Late Keys
    ItemReference("Key 5", "Forest Boss Defeated"),
    ItemReference("Key 6", "Caves Boss Defeated"),
    ItemReference("Key 7", "Castle Boss Defeated"),
    ItemReference("Key 8", "The End of Helm"),
]

with open("src/randomizers/move_text.c", "w") as fh:
    with open("include/text_items.h", "w") as fg:
        fh.write('#include "../../include/common.h"\n\n')
        fg.write('#include "common.h"\n\n')
        disclaimer = ["/*\n", "\tFile is automatically generated from build/patch_text.py\n", "\tIf you wish to modify this file, please modify the code there\n", "*/\n\n"]
        for line in disclaimer:
            fh.write(line)
            fg.write(line)

        loc_count = 0
        for ref in location_references:
            loc_count += 1 + len(ref.locations)
        fg.write(f"#define LOCATION_ITEM_COUNT {loc_count}\n")
        fg.write("typedef struct name_latin_struct {\n")
        fg.write("\t/* 0x000 */ unsigned char name;\n")
        fg.write("\t/* 0x001 */ unsigned char latin;\n")
        fg.write("} name_latin_struct;\n\n")
        for move_type in index_data:
            arr_item_type = "unsigned char"
            divisor = 1
            if index_data[move_type]["has_latin"]:
                arr_item_type = "name_latin_struct"
                divisor = 2
            fh.write(f"const {arr_item_type} {index_data[move_type]['arr_name']}[] = {{\n")
            fg.write(f"extern const {arr_item_type} {index_data[move_type]['arr_name']}[{int(len(index_data[move_type]['indexes']) / divisor)}];\n")
            for item_index in range(int(len(index_data[move_type]["indexes"]) / divisor)):
                if index_data[move_type]["has_latin"]:
                    fh.write("\t{\n")
                    fh.write(f"\t\t.name = {text_enum[index_data[move_type]['indexes'][divisor * item_index]]},\n")
                    fh.write(f"\t\t.latin = {text_enum[index_data[move_type]['indexes'][(divisor * item_index) + 1]]},\n")
                    fh.write("\t},\n")
                else:
                    fh.write(f"\t{text_enum[index_data[move_type]['indexes'][divisor * item_index]]},\n")
            fh.write("};\n\n")

location_items_arr = []
for ref in location_references:
    location_items_arr.append([{"text": [ref.item.upper()]}])
    for loc in ref.locations:
        location_items_arr.append([{"text": [loc.upper()]}])

writeText("move_names.bin", move_names_arr)
writeText("item_locations.bin", location_items_arr)

move_explanations = [
    {
        "move": "dive_barrel",  # 0x25
        "explanation": [{"text": ["PAY ATTENTION, ~. YOU AND ALL THE OTHER KONGS CAN NOW DIVE UNDERWATER. PRESS"]}, {"text": [Icons.ButtonZ]}, {"text": ["TO SUBMERGE YOURSELF."]}],
    },
    {
        "move": "orange_barrel",  # 0x26
        "explanation": [
            {"text": ["PAY ATTENTION, ~. YOU AND ALL THE OTHER KONGS CAN NOW THROW ORANGE GRENADES. PRESS"]},
            {"text": [Icons.ButtonZ]},
            {"text": ["THEN"]},
            {"text": [Icons.ButtonCL]},
            {"text": ["TO FIRE AN EXPLOSIVE FRUIT."]},
        ],
    },
    {
        "move": "barrel_barrel",  # 0x27
        "explanation": [{"text": ["PAY ATTENTION, ~. YOU AND ALL THE OTHER KONGS CAN NOW PICK UP OBJECTS. PRESS"]}, {"text": [Icons.ButtonB]}, {"text": ["TO GRAB AN OBJECT WITH RELATIVE EASE."]}],
    },
    {
        "move": "vine_barrel",  # 0x28
        "explanation": [
            {"text": ["PAY ATTENTION, ~. YOU AND ALL THE OTHER KONGS CAN NOW SWING ON VINES. JUMP TO GRAB ONTO THE VINE AND PRESS "]},
            {"text": [Icons.ButtonA]},
            {"text": ["TO LAUNCH YOURSELF FROM IT."]},
        ],
    },
    {
        "move": "camera_solo",  # 0x29
        "explanation": [
            {"text": ["PAY ATTENTION, ~. YOU AND ALL THE OTHER KONGS CAN NOW USE A CAMERA TO SNAP BANANA FAIRIES. PRESS"]},
            {"text": [Icons.ButtonZ]},
            {"text": ["THEN"]},
            {"text": [Icons.ButtonCD]},
            {"text": ["TO PULL OUT THE CAMERA. PRESS"]},
            {"text": [Icons.ButtonB]},
            {"text": ["TO TAKE A PICTURE."]},
        ],
    },
    {
        "move": "shockwave_solo",  # 0x2A
        "explanation": [
            {"text": ["PAY ATTENTION, ~. YOU AND ALL THE OTHER KONGS CAN NOW RELEASE A SHOCKWAVE CHARGE. PRESS AND HOLD"]},
            {"text": [Icons.ButtonB]},
            {"text": ["TO CHARGE THE SHOCKWAVE."]},
        ],
    },
    {
        "move": "camera_shockwave_combo",  # 0x2B
        "explanation": [
            {"text": ["PAY ATTENTION, ~. YOU AND ALL THE OTHER KONGS CAN NOW RELEASE A SHOCKWAVE CHARGE AND USE A CAMERA TO SNAP BANANA FAIRIES. PRESS AND HOLD"]},
            {"text": [Icons.ButtonB]},
            {"text": ["TO CHARGE THE SHOCKWAVE. PRESS "]},
            {"text": [Icons.ButtonZ]},
            {"text": ["THEN"]},
            {"text": [Icons.ButtonCD]},
            {"text": ["TO PULL OUT THE CAMERA."]},
        ],
    },
    {"move": "generic_item", "explanation": [{"text": ["PAY ATTENTION, ~. THERE'S PLENTY MORE ITEMS TO GATHER IN THIS GAME. GET MOVING SO WE CAN DISPENSE OF K. ROOL"]}]},  # 0x2C
]

cranky_text = grabText(8)
cranky_text.append(
    [
        {"text": ["DID DIDDY DROP SOME OF YOUR COCONUTS AGAIN? LET US TRADE. DIDDY FOR THE COCONUTS, THE COCONUTS FOR DIDDY."]},
    ]
)  # Item 0x24
for move in move_explanations:
    cranky_text.append(move["explanation"])
writeText("cranky_text.bin", cranky_text)

menu_text = grabText(37)
menu_text[46] = [{"text": ["FIRST PERSON CAMERA"]}]
writeText("menu_text.bin", menu_text)

kongname_text = grabText(2)
kongname_text.append([{"text": ["KRUSHA"]}])
kongname_text.append([{"text": ["K. ROOL"]}])
kongname_text.append([{"text": ["CRANKY"]}])
kongname_text.append([{"text": ["CANDY"]}])
kongname_text.append([{"text": ["FUNKY"]}])
writeText("kongname_text.bin", kongname_text)

fairy_text = grabText(40)
fairy_text[4] = [{"text": ["~ REMEMBER, MUST GET FAIRIES TO OBTAIN SPECIAL REWARD."]}]
writeText("fairy_rw_text.bin", fairy_text)

# byte_lst = ["\x04","\x05","\x06","\x07","\x08","\x09","\x0A","\x0B","\x0C","\x0D",]
squawks_text = grabText(19)
# squawks_text.append([{"text": [f"TEST {' '.join([(x + 'TEST' + x) for x in byte_lst])}."]}])
squawks_text.append([{"text": ["YOU CAN FIND \x04GORILLA GONE\x04 IN \x05CAVES CRANKY\x05."]}])
squawks_text.append([{"text": ["YOU CAN FIND \x04MONKEYPORT\x04 IN \x05CAVES CRANKY\x05."]}])
squawks_text.append([{"text": ["YOU CAN FIND \x04BONGO BLAST\x04 IN \x05AZTEC CANDY\x05."]}])
squawks_text.append([{"text": ["YOU CAN FIND \x04TRIANGLE TRAMPLE\x04 IN \x05AZTEC CANDY\x05."]}])
squawks_text.append([{"text": ["YOU CAN FIND \x04SAXOPHONE SLAM\x04 IN \x05AZTEC CANDY\x05."]}])
squawks_text.append([{"text": ["YOU CAN FIND \x04TROMBONE TREMOR\x04 IN \x05AZTEC CANDY\x05."]}])
squawks_text.append([{"text": ["YOU CAN FIND \x04GUITAR GAZUMP\x04 IN \x05AZTEC CANDY\x05."]}])
squawks_text.append([{"text": ["MYUM, MYUM. I WILL NEVER GIVE UP MY \x04GOLDEN BANANA\x04 TO THIS INTRUDER."]}])
squawks_text.append(
    [
        {
            "text": [
                "LADIES AND GENTLEMEN! IT APPEARS THAT ONE FIGHTER HAS COME UNEQUIPPED TO PROPERLY HANDLE THIS REPTILIAN BEAST. PERHAPS THEY SHOULD HAVE LOOKED IN \x07FUNGI FOREST\x07 OR \x09CREEPY CASTLE\x09 FOR THE ELUSIVE SLAM."
            ]
        }
    ]
)
squawks_text.append([{"text": ["A \x04GOLDEN BANANA\x04 FOR YOU IF YOU SAVE ME FROM THESE FIREBALLS. HEE HEE."]}])
squawks_text.append([{"text": ["DEAR STREAMER, IT APPEARS YOU HAVE WANDERED INTO A PLACE WHERE THERE IS PLACEHOLDER TEXT. YOUR SEED, AS A RESULT, IS TEN PERCENT WORSE. GOOD LUCK"]}])
squawks_text.append([{"text": ["DEAR STREAMER, IT APPEARS YOU HAVE WANDERED INTO A PLACE WHERE THERE IS PLACEHOLDER TEXT. YOUR SEED, AS A RESULT, IS TEN PERCENT WORSE. GOOD LUCK"]}])
squawks_text.append([{"text": ["DEAR STREAMER, IT APPEARS YOU HAVE WANDERED INTO A PLACE WHERE THERE IS PLACEHOLDER TEXT. YOUR SEED, AS A RESULT, IS TEN PERCENT WORSE. GOOD LUCK"]}])
squawks_text.append([{"text": ["DEAR STREAMER, IT APPEARS YOU HAVE WANDERED INTO A PLACE WHERE THERE IS PLACEHOLDER TEXT. YOUR SEED, AS A RESULT, IS TEN PERCENT WORSE. GOOD LUCK"]}])
writeText("misc_squawks_text.bin", squawks_text)

hint_region_text = []
for region in hint_region_list:
    hint_region_text.append([{"text": [region.region_name.upper()]}])
writeText("hint_region_text.bin", hint_region_text)
writeText("short_wrinkly.bin", grabText(41))

vanilla_track_names = [
    "Silence",
    "Jungle Japes (Starting Area)",
    "Cranky's Lab",
    "Jungle Japes (Minecart)",
    "Jungle Japes (Army Dillo)",
    "Jungle Japes (Caves and Underground)",
    "Funky's Hut",
    "Unused Coin Pickup",
    "Bonus Minigames",
    "Triangle Trample",
    "Guitar Gazump",
    "Bongo Blast",
    "Trombone Tremor",
    "Saxaphone Slam",
    "Angry Aztec",
    "Transformation",
    "Mini Monkey",
    "Hunky Chunky",
    "GB/Key Get",
    "Angry Aztec (Beetle Slide)",
    "Oh Banana",
    "Angry Aztec (Temple)",
    "Company Coin Get",
    "Banana Coin Get",
    "Going through Vulture Ring",
    "Angry Aztec (Dogadon)",
    "Angry Aztec (5DT)",
    "Frantic Factory (Car Race)",
    "Frantic Factory",
    "Snide's HQ",
    "Jungle Japes (Tunnels)",
    "Candy's Music Shop",
    "Minecart Coin Get",
    "Melon Slice Get",
    "Pause Menu",
    "Crystal Coconut Get",
    "Rambi",
    "Angry Aztec (Tunnels)",
    "Water Droplets",
    "Frantic Factory (Mad Jack)",
    "Success",
    "Start (To pause game)",
    "Failure",
    "DK Transition (Opening)",
    "DK Transition (Closing)",
    "Unused High-Pitched Japes",
    "Fairy Tick",
    "Melon Slice Drop",
    "Angry Aztec (Chunky Klaptraps)",
    "Frantic Factory (Crusher Room)",
    "Jungle Japes (Baboon Blast)",
    "Frantic Factory (R&D)",
    "Frantic Factory (Production Room)",
    "Troff 'n' Scoff",
    "Boss Defeat",
    "Angry Aztec (Baboon Blast)",
    "Gloomy Galleon (Outside)",
    "Boss Unlock",
    "Awaiting Entering the Boss",
    "Generic Twinkly Sounds",
    "Gloomy Galleon (Pufftoss)",
    "Gloomy Galleon (Seal Race)",
    "Gloomy Galleon (Tunnels)",
    "Gloomy Galleon (Lighthouse)",
    "Battle Arena",
    "Drop Coins (Minecart)",
    "Fairy Nearby",
    "Checkpoint",
    "Fungi Forest (Day)",
    "Blueprint Get",
    "Fungi Forest (Night)",
    "Strong Kong",
    "Rocketbarrel Boost",
    "Orangstand Sprint",
    "Fungi Forest (Minecart)",
    "DK Rap",
    "Blueprint Drop",
    "Gloomy Galleon (2DS)",
    "Gloomy Galleon (5DS and Submarine)",
    "Gloomy Galleon (Pearls Chest)",
    "Gloomy Galleon (Mermaid Palace)",
    "Fungi Forest (Dogadon)",
    "Mad Maze Maul",
    "Crystal Caves",
    "Crystal Caves (Giant Kosha Tantrum)",
    "Nintendo Logo (Old)",
    "Success (Races)",
    "Failure (Races & Try Again)",
    "Bonus Barrel Introduction",
    "Stealthy Snoop",
    "Minecart Mayhem",
    "Gloomy Galleon (Mechanical Fish)",
    "Gloomy Galleon (Baboon Blast)",
    "Fungi Forest (Anthill)",
    "Fungi Forest (Barn)",
    "Fungi Forest (Mill)",
    "Generic Seaside Sounds",
    "Fungi Forest (Spider)",
    "Fungi Forest (Mushroom Top Rooms)",
    "Fungi Forest (Giant Mushroom)",
    "Boss Introduction",
    "Tag Barrel (All of them)",
    "Crystal Caves (Beetle Race)",
    "Crystal Caves (Igloos)",
    "Mini Boss",
    "Creepy Castle",
    "Creepy Castle (Minecart)",
    "Baboon Balloon",
    "Gorilla Gone",
    "DK Isles",
    "DK Isles (K Rool's Ship)",
    "DK Isles (Banana Fairy Island)",
    "DK Isles (K-Lumsy's Prison)",
    "Hideout Helm (Blast-O-Matic On)",
    "Move Get",
    "Gun Get",
    "Hideout Helm (Blast-O-Matic Off)",
    "Hideout Helm (Bonus Barrels)",
    "Crystal Caves (Cabins)",
    "Crystal Caves (Rotating Room)",
    "Crystal Caves (Tile Flipping)",
    "Creepy Castle (Tunnels)",
    "Intro Story Medley",
    "Training Grounds",
    "Enguarde",
    "K-Lumsy Celebration",
    "Creepy Castle (Crypt)",
    "Headphones Get",
    "Pearl Get",
    "Creepy Castle (Dungeon with Chains)",
    "Angry Aztec (Lobby)",
    "Jungle Japes (Lobby)",
    "Frantic Factory (Lobby)",
    "Gloomy Galleon (Lobby)",
    "Main Menu",
    "Creepy Castle (Inner Crypts)",
    "Creepy Castle (Ballroom)",
    "Creepy Castle (Greenhouse)",
    "K Rool's Theme",
    "Creepy Castle (Shed)",
    "Creepy Castle (Wind Tower)",
    "Creepy Castle (Tree)",
    "Creepy Castle (Museum)",
    "BBlast Final Star",
    "Drop Rainbow Coin",
    "Rainbow Coin Get",
    "Normal Star",
    "Bean Get",
    "Crystal Caves (Army Dillo)",
    "Creepy Castle (Kut Out)",
    "Creepy Castle (Dungeon without Chains)",
    "Banana Medal Get",
    "K Rool's Battle",
    "Fungi Forest (Lobby)",
    "Crystal Caves (Lobby)",
    "Creepy Castle (Lobby)",
    "Hideout Helm (Lobby)",
    "Creepy Castle (Trash Can)",
    "End Sequence",
    "K-Lumsy Ending",
    "Jungle Japes",
    "Jungle Japes (Cranky's Area)",
    "K Rool Takeoff",
    "Crystal Caves (Baboon Blast)",
    "Fungi Forest (Baboon Blast)",
    "Creepy Castle (Baboon Blast)",
    "DK Isles (Snide's Room)",
    "K Rool's Entrance",
    "Monkey Smash",
    "Fungi Forest (Rabbit Race)",
    "Game Over",
    "Wrinkly Kong",
    "100th CB Get",
    "K Rool's Defeat",
    "Nintendo Logo",
]

music_text = []
for name in vanilla_track_names:
    music_text.append([{"text": [f"DONKEY KONG 64\n{name.upper()}"]}])
writeText("music_names.bin", music_text)


misc_char_table = {
    "6": "h",
    "4": "f",
    "t": "{",  # Trademark
    ".": "[",
    "r": "~",  # R symbol
}


class ExpansionMessageInfo:
    """Class to store information regarding the expansion pak messages."""

    def __init__(self, limit: int, address: int, old_message: str, new_message: str):
        """Initialize with given parameters."""
        self.limit = limit
        self.address = address
        self.old_message = old_message
        self.new_message = new_message
        self.old_message_padding = len(old_message) - limit

    def convertNewMessage(self):
        """Convert new message to filter out any bad characters."""
        new_str = ""
        for x in self.new_message:
            if x in list(misc_char_table.keys()):
                new_str += misc_char_table[x]
            else:
                new_str += x
        total_length = len(self.old_message) + (2 * self.old_message_padding)
        new_padding = int((total_length - len(self.new_message)) / 2)
        max_padding = self.limit - len(self.new_message)
        new_padding = min(new_padding, max_padding)
        padding_str = ""
        if new_padding > 0:
            for x in range(new_padding):
                padding_str += " "
        self.new_message = padding_str + new_str + "\0"

    def writeMessage(self, fh: BinaryIO):
        """Write message to ROM."""
        self.convertNewMessage()
        if self.limit >= (len(self.new_message) - 1):  # Message is short enough
            fh.seek(self.address)
            fh.write((self.new_message).encode("ascii"))
            # diff = self.limit - len(self.new_message)
            # for d in range(diff):
            #     fh.write((0).to_bytes(1, "big"))


def writeNoExpPakMessages(fh: BinaryIO):
    """Write no expansion pak messages to ROM."""
    noexp_msg = [
        ExpansionMessageInfo(25, 0xF924, "N64 EXPANSION PAKt", "NO EXPANSION PAK FOUND."),
        ExpansionMessageInfo(23, 0xF940, "NOT INSTALLED.", "THIS IS LIKELY DUE TO"),
        ExpansionMessageInfo(31, 0xF958, "THE N64 EXPANSION PAK ACCESSORY", "AN INCORRECTLY SET UP EMULATOR"),
        ExpansionMessageInfo(33, 0xF978, "MUST BE INSTALLED IN THE N64r FOR", "OR CONSOLE. PLEASE CONTACT THE"),
        ExpansionMessageInfo(32, 0xF99C, "THIS GAME. SEE THE N64 EXPANSION", "DISCORD FOR HELP."),
        ExpansionMessageInfo(27, 0xF9C0, "PAK INSTRUCTION BOOKLET.", "DISCORD.DK64RANDOMIZER.COM"),
    ]
    for m in noexp_msg:
        m.writeMessage(fh)
