"""Patch some common text."""

from text_encoder import writeText
import shutil

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
    {"move": "Baboon Balloon", "kong": "Lanky", "cranky": "THE BUBBLES IN THIS POTION ARE HELIUM.", "funky": "THIS MAGIC POTION WILL BLOW YOU AWAY!", "candy": "THIS WILL GET YOU FEELING FLOATY!"},
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
        "cranky": "IN MY DAY, YOU'D HAVE TO WALK UPHILL BOTH WAYS, BUT THIS WILL WARP YOU IN AN INSTANT.",
        "funky": "THIS COOL MOVE WILL SEND YOU PLACES!",
        "candy": "IT'S YOUR VERY OWN PERSONAL WARP PAD!",
    },
    {
        "move": "Hunky Chunky",
        "kong": "Chunky",
        "cranky": "ALTHOUGH I'M NOT SURE WHY YOU'D NEED IT, YOU'RE ALREADY BIG ENOUGH AS IT IS.",
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
        "kong": "Tiny",
        "cranky": "NOW, TAKE IT AND DONT POINT IT AT ME! YOU'D RIP MY FEEBLE HEAD OFF WITH THESE PINEAPPLES!",
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
    "Not enough coins - Special Move",
    "Not enough coins - Slam",
    "Not enough coins - Gun",
    "Not enough coins - Ammo Belt",
    "Not enough coins - Instrument",
]

shop_owners = [
    "cranky",
    "funky",
    "candy",
]

hint_text = []

for move in move_hints:
    for shop in shop_owners:
        hint_pre = pre_amble[shop]
        hint_post = move[shop]
        hint_text.append([f"{hint_pre}{hint_post}"])


writeText(
    "dolby_text.bin",
    [
        ["DONKEY KONG 64 RANDOMIZER"],
        ["DEVELOPERS - 2DOS, BALLAAM, BISMUTH, CFOX, KILLKLLI, SHADOWSHINE, ZNERNICUS"],
        ["DK64RANDOMIZER.COM"],
    ],
)

writeText("custom_text.bin", hint_text)

writeText(
    "dk_text.bin",
    [
        ["WHAT DID CRANKY MEAN ABOUT TRAINING? DONKEY ALL CONFUSED..."],
        ["AW NO! SO THAT WHAT CRANKY MEAN ABOUT REPTILE...", "DONKEY NOT BELIEVE IT. KING K.ROOL? WE FINISHED K. ROOL OFF IN LAST GAME!"],
        ["OKAY!", "DONKEY IS FREE NOW. THANK YOU, MY FRIEND.", "DONKEY CAN COLLECT YELLOW BANANAS.", "DONKEY WILL BE INSIDE THE TAG BARREL UNTIL YOU NEED MY HELP."],
    ],
)
