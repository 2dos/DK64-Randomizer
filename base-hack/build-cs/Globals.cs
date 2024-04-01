using System.Net;
using System.IO;
using System.Diagnostics;
using System;

namespace DK64BuildRoutine {
    internal class Globals {
        public static readonly int main_pointer_table_offset = 0x101C50;
        public static readonly int BLOCK_COLOR_SIZE = 64; // Bytes allocated to a block 32x32 image. Brute forcer says we can go as low as 0x25 bytes, but leaving some room for me to have left out something
        public static readonly string ROMName = "rom/dk64.z64";
        public static readonly string newROMName = "rom/dk64-randomizer-base.z64";
        public static readonly string finalROM = "rom/dk64-randomizer-base-dev.z64";
        public static readonly int music_size = 0x8000;
        public static readonly int heap_size = 0x34000 + music_size;
        public static readonly int flut_size = 0;
        public static readonly string MODEL_DIRECTORY = "assets/models/";
        public static readonly string TEMP_FILE = "temp.bin";
        public static readonly string BIN_FOLDER = "bin/";
        public static readonly string ROOT_FOLDER = "C:/Users/courtney/Documents/Development/DK64-Randomizer/base-hack/";
    
        public static string getBinDirectory() {
            return Path.Combine(ROOT_FOLDER, BIN_FOLDER);
        }

        public static void DeleteFile(string file) {
            try {
                if (File.Exists(Path.Combine(Globals.ROOT_FOLDER, file))) {
                    File.Delete(Path.Combine(Globals.ROOT_FOLDER, file));
                } else {
                    Console.WriteLine($"File ({file}) doesn't exist");
                }
            } catch (IOException ioExp) {
                Console.WriteLine(ioExp.Message);
            }
        }

        public static void CopyFile(string file1, string file2) {
            try {
                if (File.Exists(Path.Combine(Globals.ROOT_FOLDER, file1))) {
                    File.Copy(Path.Combine(Globals.ROOT_FOLDER, file1), Path.Combine(Globals.ROOT_FOLDER, file2));
                } else {
                    Console.WriteLine($"File ({file1}) doesn't exist");
                }
            } catch (IOException ioExp) {
                Console.WriteLine(ioExp.Message);
            }
        }

        public enum ChangeType {
            Undefined,
            PointerTable,
            FixedLocation,
        }

        public enum TextureFormat {
            Null,
            RGBA5551,
            RGBA32,
            I8,
            I4,
            IA8,
            IA4,
        }

        public enum CompressionMethods {
            PythonGzip,
            ExternalGzip,
            Zlib,
        }

        public enum TableNames {
            MusicMIDI,
            MapGeometry,
            MapWalls,
            MapFloors,
            ModelTwoGeometry,
            ActorGeometry,
            Unknown6,
            TexturesUncompressed,
            Cutscenes,
            Setups,
            InstanceScripts,
            Animations,
            Text,
            Unknown13,
            TexturesHUD,
            Paths,
            Spawners,
            DKTVInputs,
            Triggers,
            Unknown19,
            Unknown20,
            Autowalks,
            Unknown22,
            Exits,
            RaceCheckpoints,
            TexturesGeometry,
            UncompressedFileSizes,
            Unknown27,
            Unknown28,
            Unknown29,
            Unknown30,
            Unknown31,
        }

        public enum Maps {
            TestMap,
            Funky,
            DKArcade,
            HelmBarrel_LankyMaze,
            JapesMountain,
            Cranky,
            JapesMinecart,
            Japes,
            JapesDillo,
            Jetpac,
            Kosh_VEasy,
            Snoop_NormalNoLogo,
            JapesShell,
            JapesPainting,
            AztecBeetle,
            Snide,
            AztecTinyTemple,
            Helm,
            Turtles_VEasy,
            Aztec5DTDK,
            AztecLlamaTemple,
            Aztec5DTDiddy,
            Aztec5DTTiny,
            Aztec5DTLanky,
            Aztec5DTChunky,
            Candy,
            Factory,
            FactoryCarRace,
            Helm_IntrosGameOver,
            FactoryPowerShed,
            Galleon,
            GalleonSeasickShip,
            BattyBarrel_VEasy,
            JapesUnderground,
            Isles,
            HelmBarrel_Target,
            FactoryCrusher,
            JapesBBlast,
            Aztec,
            GalleonSealRace,
            NintendoLogo,
            AztecBBlast,
            TroffNScoff,
            Galleon5DSDiddyLankyChunky,
            GalleonTreasureChest,
            GalleonMermaid,
            Galleon5DSDKTiny,
            Galleon2DS,
            Fungi,
            GalleonLighthouse,
            HelmBarrel_MushroomBounce,
            GalleonMechFish,
            FungiAntHill,
            BattleArena_BeaverBrawl,
            GalleonBBlast,
            FungiMinecart,
            FungiDiddyBarn,
            FungiDiddyAttic,
            FungiLankyAttic,
            FungiDKBarn,
            FungiSpider,
            FungiMillFront,
            FungiMillRear,
            FungiMushroomSlam,
            FungiGiantMushroom,
            Snoop_Normal,
            Maul_Hard,
            Snatch_Normal,
            Maul_Easy,
            Maul_Normal,
            FungiMushroomLeap,
            FungiShootingGame,
            Caves,
            BattleArena_KritterKarnage,
            Snatch_Easy,
            Snatch_Hard,
            DKRap,
            MMayhem_Easy,
            Barrage_Easy,
            Barrage_Normal,
            MainMenu,
            NFRTitleScreen,
            CavesBeetleRace,
            FungiDogadon,
            Caves5DITiny,
            Caves5DILanky,
            Caves5DIDK,
            Castle,
            CastleBallroom,
            CavesRotatingRoom,
            Caves5DCChunky,
            Caves5DCDK,
            Caves5DCDiddyLow,
            Caves5DCTiny,
            Caves1DC,
            Caves5DIChunky,
            Salvage_Normal,
            KLumsy,
            CavesTileFlip,
            Sortie_Easy,
            Caves5DIDiddy,
            Klamour_Easy,
            Bash_VEasy,
            Searchlight_VEasy,
            BBother_Easy,
            CastleTower,
            CastleMinecart,
            MultiplayerBattleArena,
            CastleCryptLankyTiny,
            MultiplayerArena1,
            FactoryBBlast,
            GalleonPufftoss,
            CastleCryptDKDiddyChunky,
            CastleMuseum,
            CastleLibrary,
            Kosh_Easy,
            Kosh_Normal,
            Kosh_Hard,
            Turtles_Easy,
            Turtles_Normal,
            Turtles_Hard,
            BattyBarrel_Easy,
            BattyBarrel_Normal,
            BattyBarrel_Hard,
            Maul_Insane,
            Snatch_Insane,
            Snoop_VEasy,
            Snoop_Easy,
            Snoop_Hard,
            MMayhem_Normal,
            MMayhem_Hard,
            Barrage_Hard,
            Salvage_Hard,
            Salvage_Easy,
            Sortie_Normal,
            Sortie_Hard,
            BBother_Normal,
            BBother_Hard,
            Searchlight_Easy,
            Searchlight_Normal,
            Searchlight_Hard,
            Klamour_Normal,
            Klamour_Hard,
            Klamour_Insane,
            PPPanic_VEasy,
            PPPanic_Easy,
            PPPanic_Normal,
            PPPanic_Hard,
            Bash_Easy,
            Bash_Normal,
            Bash_Hard,
            CastleDungeon,
            Helm_IntroStory,
            Isles_DKTheatre,
            FactoryJack,
            BattleArena_ArenaAmbush,
            BattleArena_MoreKritterKarnage,
            BattleArena_ForestFracas,
            BattleArena_BishBashBrawl,
            BattleArena_KamikazeKremlings,
            BattleArena_PlinthPanic,
            BattleArena_PinnaclePalaver,
            BattleArena_ShockwaveShowdown,
            CastleBasement,
            CastleTree,
            HelmBarrel_RandomKremling,
            CastleShed,
            CastleTrash,
            CastleGreenhouse,
            JapesLobby,
            HelmLobby,
            Treehouse,
            Isles_IntroStoryRock,
            AztecLobby,
            GalleonLobby,
            FactoryLobby,
            TrainingGrounds,
            TBarrel_Dive,
            FungiLobby,
            GalleonSubmarine,
            TBarrel_Orange,
            TBarrel_Barrel,
            TBarrel_Vine,
            CastleCrypt,
            EnguardeArena,
            CastleCarRace,
            CavesBBlast,
            CastleBBlast,
            FungiBBlast,
            FairyIsland,
            MultiplayerArena2,
            RambiArena,
            MultiplayerArena3,
            CastleLobby,
            CavesLobby,
            Isles_SnideRoom,
            CavesDillo,
            AztecDogadon,
            TrainingGrounds_EndSequence,
            CastleKutOut,
            CavesShackDiddyHigh,
            HelmBarrel_Rocketbarrel,
            HelmBarrel_LankyShooting,
            KRoolDK,
            KRoolDiddy,
            KRoolLanky,
            KRoolTiny,
            KRoolChunky,
            BloopersEnding,
            HelmBarrel_HiddenKremling,
            HelmBarrel_FloorIsLava,
            HelmBarrel_ChunkyShooting,
            HelmBarrel_Rambi,
            KLumsyEnding,
            KRoolShoe,
            KRoolArena,
        }

        public enum Icons {
            WaterfallTall,
            WaterfallShort,
            Water,
            Lava,
            Sparkles,
            ExplosionPop,
            ExplosionLava,
            LeafGreen,
            ExplosionSmoke,
            ExplosionSmall,
            SolarFlare,
            Splash,
            Bubble,
            SparklePurple,
            SparkleYellow,
            SparkleGreen,
            SparklePurple_0,
            SparkleYellow_0,
            SparkleGreen_0,
            ExplosionLargeSmoke,
            ExplosionPink,
            PlankBrownHorizontal,
            PlankBirchHorizontal,
            PlankBrownVertical,
            RippleStar,
            RippleCircle,
            ExplosionSmallSmoke,
            StaticStar,
            StaticZ,
            FlareWhite,
            StaticRain,
            ExplosionMediumSmoke,
            MelonBouncing,
            MelonRolling,
            FlareRed,
            Sparks,
            Peanut,
            FlareStar,
            PeanutShell,
            ExplosionSmall_0,
            ExplosionLargeSmoke_0,
            LaserBlue,
            Pineapple,
            Fireball,
            Orange,
            Grape,
            GrapeSplat,
            SparkleTNT,
            ExplosionFire,
            FireballSmall,
            CoinDiddy,
            CoinChunky,
            CoinLanky,
            CoinDK,
            CoinTiny,
            BananaDK,
            Film,
            OrangeBouncing,
            Crystal,
            GB,
            Medal,
            BananaDiddy,
            BananaChunky,
            BananaLanky,
            BananaDK_0,
            BananaTiny,
            ExplosionKrash,
            ExplosionWhite,
            Coconut,
            CoconutShell,
            MelonSpinning,
            Tooth,
            CrateAmmo,
            CoinRace,
            BlueprintLanky,
            Cannonball,
            Crystal_0,
            Feather,
            Guitar,
            Bongos,
            Sax,
            Triangle,
            Trombone,
            NoteYellowDouble,
            NoteYellowSingle,
            NoteGreenSingle,
            NotePurpleDouble,
            NoteRedDouble,
            NoteRedSingle,
            NoteWhiteDouble,
            BlueprintDiddy,
            BlueprintChunky,
            BlueprintDK,
            BlueprintTiny,
            SparkleSpinning,
            StaticRain_0,
            WaterTranslucent,
            unk61,
            ScreenBlack,
            CloudWhite,
            LaserThin,
            BubbleBlue,
            CircleWhiteFaded,
            CircleWhite,
            ParticleGreen,
            SparkleBlue,
            ExplosionWhiteSmoke,
            Joystick,
            FireWall,
            StaticRainBubble,
            ButtonA,
            ButtonB,
            ButtonZ,
            ButtonCD,
            ButtonCU,
            ButtonCL,
            Acid,
            ExplosionAcid,
            RaceHoop,
            AcidGoop,
            unk78,
            BrokenBridge,
            WhitePole,
            BridgeChip,
            BeamRivets,
            BunchChunky,
            BunchDiddy,
            BunchLanky,
            BunchDK,
            BunchTiny,
            BalloonChunky,
            BalloonDiddy,
            BalloonDK,
            BalloonLanky,
            BalloonTiny,
            ButtonR,
            ButtonL,
            Fairy,
            BossKey,
            Crown,
            CoinRareware,
            CoinNintendo,
            NoSymbol,
            Headphones,
            WaterOpaque,
            ButtonStart,
            QuestionMark,
            FaceCandy,
            FaceCranky,
            FaceSnide,
            FaceFunky,
            ArrowLeft,
            SparkleWhite,
            BoulderChunkBlack,
            BoulderChunkGreen,
            WoodChip,
            Snowflake,
            StaticWater,
            SpinningLeaf,
            FlashingWater,
            CoinRainbow,
            ShockwaveParticle,
            Implosion,
            RarewareEmployeeFace,
            Smoke,
            StaticSmoke,
            BarrelBottomChunk,
            FaceScoff,
            BunchMulti,
            FaceDK,
            FaceDiddy,
            FaceLanky,
            FaceTiny,
            FaceChunky,
            FairyTick,
            Wrinkly,
        }

        public enum CreditsDirection {
            top,
            left,
            bottom,
            right,
        }

        public enum CreditsType {
            normal,
            header,
            longheader,
        }

        public enum Enemies {
            BeaverBlue = 0,
            GiantClam = 1,
            Krash = 2,
            Book = 3,
            ZingerCharger = 5,
            Klobber = 6,
            Snide = 7,
            ArmyDillo = 8,
            Klump = 9,
            Cranky = 11,
            Funky = 12,
            Candy = 13,
            Beetle = 14,
            Mermaid = 15,
            Kaboom = 16,
            VultureTemple = 17,
            Squawks = 18,
            CutsceneDK = 19,
            CutsceneDiddy = 20,
            CutsceneLanky = 21,
            CutsceneTiny = 22,
            CutsceneChunky = 23,
            TandSPadlock = 24,
            Llama = 25,
            MadJack = 26,
            KlaptrapGreen = 27,
            ZingerLime = 28,
            VultureRace = 29,
            KlaptrapPurple = 30,
            KlaptrapRed = 31,
            GetOut = 32,
            BeaverGold = 33,
            FireColumn = 35,
            TNTMinecart0 = 36,
            TNTMinecart1 = 37,
            Pufftoss = 38,
            SeasickCannon = 39,
            KRoolFoot = 40,
            Fireball = 42,
            MushroomMan = 44,
            Troff = 46,
            BadHitDetectionMan = 48,
            Ruler = 51,
            ToyBox = 52,
            Squawks1 = 53,
            Seal = 54,
            Scoff = 55,
            RoboKremling = 56,
            Dogadon = 57,
            Kremling = 59,
            SpotlightFish = 60,
            KasplatDK = 61,
            KasplatDiddy = 62,
            KasplatLanky = 63,
            KasplatTiny = 64,
            KasplatChunky = 65,
            MechFish = 66,
            Seal1 = 67,
            Fairy = 68,
            SquawksSpotlight = 69,
            Rabbit = 72,
            Owl = 73,
            NintendoLogo = 74,
            FireBreath = 75,
            MinigameController = 76,
            BattleCrownController = 77,
            ToyCar = 78,
            TNTMinecart2 = 79,
            CutsceneObject = 80,
            Guard = 81,
            RarewareLogo = 82,
            ZingerRobo = 83,
            Krossbones = 84,
            Shuri = 85,
            Gimpfish = 86,
            MrDice0 = 87,
            SirDomino = 88,
            MrDice1 = 89,
            Rabbit1 = 90,
            FireballGlasses = 92,
            KLumsy = 93,
            SpiderBoss = 94,
            SpiderSmall = 95,
            Squawks2 = 96,
            KRoolDK = 97,
            SkeletonHead = 98,
            Bat = 99,
            EvilTomato = 100,
            Ghost = 101,
            Pufftup = 102,
            Kosha = 103,
            EnemyCar = 105,
            KRoolDiddy = 106,
            KRoolLanky = 107,
            KRoolTiny = 108,
            KRoolChunky = 109,
            Bug = 110,
            FairyQueen = 111,
            IceTomato = 112,
        }

        public enum Kong {
            DK,
            Diddy,
            Lanky,
            Tiny,
            Chunky,
        }

        public enum Song {
            Silence,
            JapesStart,
            Cranky,
            JapesCart,
            JapesDillo,
            JapesCaves,
            Funky,
            UnusedCoin,
            Minigames,
            Triangle,
            Guitar,
            Bongos,
            Trombone,
            Saxophone,
            AztecMain,
            Transformation,
            MiniMonkey,
            HunkyChunky,
            GBGet,
            AztecBeetle,
            OhBanana,
            AztecTemple,
            CompanyCoinGet,
            BananaCoinGet,
            VultureRing,
            AztecDogadon,
            Aztec5DT,
            FactoryCarRace,
            FactoryMain,
            Snide,
            JapesTunnels,
            Candy,
            MinecartCoinGet,
            MelonSliceGet,
            PauseMenu,
            CrystalCoconutGet,
            Rambi,
            AztecTunnels,
            WaterDroplets,
            FactoryJack,
            Success,
            StartPause,
            Failure,
            TransitionOpen,
            TransitionClose,
            JapesHighPitched,
            FairyTick,
            MelonSliceDrop,
            AztecChunkyKlaptraps,
            FactoryCrusher,
            JapesBlast,
            FactoryResearchAndDevelopment,
            FactoryProduction,
            TroffNScoff,
            BossDefeat,
            AztecBlast,
            GalleonOutside,
            BossUnlock,
            AwaitingBossEntry,
            TwinklySounds,
            GalleonPufftoss,
            GalleonSealRace,
            GalleonTunnels,
            GalleonLighthouse,
            BattleArena,
            DropCoins,
            FairyNearby,
            Checkpoint,
            ForestDay,
            BlueprintGet,
            ForestNight,
            StrongKong,
            Rocketbarrel,
            Sprint,
            ForestCart,
            DKRap,
            BlueprintDrop,
            Galleon2DS,
            Galleon5DS,
            GalleonChest,
            GalleonMermaid,
            ForestDogadon,
            MadMazeMaul,
            Caves,
            CavesTantrum,
            NintendoLogoOld,
            SuccessRaces,
            FailureRaces,
            BonusBarrelIntroduction,
            StealthySnoop,
            MinecartMayhem,
            GalleonMechFish,
            GalleonBlast,
            ForestAnthill,
            ForestBarn,
            ForestMill,
            SeasideSounds,
            ForestSpider,
            ForestMushroomRooms,
            ForestMushroom,
            BossIntroduction,
            TagBarrel,
            CavesBeetleRace,
            CavesIgloos,
            MiniBoss,
            Castle,
            CastleCart,
            BaboonBalloon,
            GorillaGone,
            Isles,
            IslesKremIsle,
            IslesBFI,
            IslesKLumsy,
            HelmBoMOn,
            MoveGet,
            GunGet,
            HelmBoMOff,
            HelmBonus,
            CavesCabins,
            CavesRotatingRoom,
            CavesIceCastle,
            CastleTunnels,
            IntroStory,
            TrainingGrounds,
            Enguarde,
            KLumsyCelebration,
            CastleCrypt,
            HeadphonesGet,
            PearlGet,
            CastleDungeon_Chains,
            AztecLobby,
            JapesLobby,
            FactoryLobby,
            GalleonLobby,
            MainMenu,
            CastleInnerCrypts,
            CastleBallroom,
            CastleGreenhouse,
            KRoolTheme,
            CastleShed,
            CastleTower,
            CastleTree,
            CastleMuseum,
            BBlastFinalStar,
            DropRainbowCoin,
            RainbowCoinGet,
            NormalStar,
            BeanGet,
            CavesDillo,
            CastleKutOut,
            CastleDungeon_NoChains,
            BananaMedalGet,
            KRoolBattle,
            ForestLobby,
            CavesLobby,
            CastleLobby,
            HelmLobby,
            CastleTrash,
            EndSequence,
            KLumsyEnding,
            JapesMain,
            JapesStorm,
            KRoolTakeoff,
            CavesBlast,
            ForestBlast,
            CastleBlast,
            IslesSnideRoom,
            KRoolEntrance,
            MonkeySmash,
            ForestRabbitRace,
            GameOver,
            WrinklyKong,
            FinalCBGet,
            KRoolDefeat,
            NintendoLogo,
        }

        public enum NullBoolean {
            none, // null
            disabled, // false
            enabled, // true
        }

        public class NewFile {
            public static string file_name = "";
            public static ChangeType file_subtype;
            public static int file_start;
            public static int file_compressed_size;
            public static string file_source = "";
            public static CompressionMethods file_compression_method;
            public static int file_patcher;
            public static TableNames file_pointer_table_index;
            public static int file_pointer_file_index;
            public static TextureFormat file_texture_format;
            public static string file_bps = "";
            public static bool file_do_not_delete_source;
            public static bool file_do_not_delete_output;
            public static bool file_do_not_delete;
            public static int file_target_compressed_size;
            public static int file_target_uncompressed_size;
            public static bool file_do_not_extract;
            public static bool file_do_not_compress;
            public static bool file_do_not_recompress;
            public static bool file_bloat_compression;
            public static string file_output = "";

            public NewFile (
                string name = "",
                ChangeType subtype = ChangeType.PointerTable,
                int start = 0, // 0 = null
                int compressed_size = 0,
                string source_file = "",
                CompressionMethods compression_method = CompressionMethods.PythonGzip,
                int patcher = 0, // 0 = null
                TableNames pointer_table_index = TableNames.MusicMIDI,
                int file_index = 0,
                TextureFormat texture_format = TextureFormat.Null,
                string bps_file = "", // empty string = null
                bool do_not_delete_source = false,
                bool do_not_delete_output = false,
                bool do_not_delete = false,
                int target_compressed_size = 0, // 0 = null
                int target_uncompressed_size = 0, // 0 = null
                int target_size = 0, // 0 = null
                bool do_not_extract = false,
                bool do_not_compress = false,
                bool do_not_recompress = false,
                bool bloat_compression = false
            ) {
                file_name = name;
                file_subtype = subtype;
                file_start = start;
                file_compressed_size = compressed_size;
                file_source = source_file;
                file_compression_method = compression_method;
                file_patcher = patcher;
                file_pointer_table_index = pointer_table_index;
                file_pointer_file_index = file_index;
                file_texture_format = texture_format;
                file_bps = bps_file;
                file_do_not_delete_source = do_not_delete_source;
                file_do_not_delete_output = do_not_delete_output;
                file_do_not_delete = do_not_delete;
                file_do_not_extract = do_not_extract;
                file_do_not_compress = do_not_compress;
                file_do_not_recompress = do_not_recompress;
                file_target_compressed_size = target_compressed_size;
                file_target_uncompressed_size = target_uncompressed_size;
                file_bloat_compression = bloat_compression;
                if (target_size > 0) {
                    file_target_compressed_size = target_size;
                    file_target_uncompressed_size = target_size;
                } else if ((bloat_compression) && (source_file != "")) {
                    FileInfo fi = new FileInfo(source_file);
                    file_target_compressed_size = (int)fi.Length;
                    file_target_uncompressed_size = (int)fi.Length;
                }
                file_output = "";
            }

            static string getTextureFormatName() {
                switch (file_texture_format) {
                    case TextureFormat.Null:
                        return "null";
                    case TextureFormat.RGBA5551:
                        return "rgba5551";
                    case TextureFormat.RGBA32:
                        return "rgba32";
                    case TextureFormat.I8:
                        return "i8";
                    case TextureFormat.I4:
                        return "i4";
                    case TextureFormat.IA8:
                        return "ia8";
                    case TextureFormat.IA4:
                        return "ia4";
                    default:
                        break;
                }
                return "";
            }

            static bool isN64TexFormat() {
                switch (file_texture_format) {
                    case TextureFormat.RGBA5551:
                    case TextureFormat.I4:
                    case TextureFormat.I8:
                    case TextureFormat.IA4:
                    case TextureFormat.IA8:
                        return true;
                    default:
                        break;
                }
                return false;
            }

            public static void generateTextureFile() {
                if (file_texture_format != TextureFormat.Null) {
                    if (isN64TexFormat()) {
                        ProcessStartInfo startInfo = new ProcessStartInfo();
                        startInfo.FileName = Path.Combine(Globals.ROOT_FOLDER, "build/n64tex.exe");
                        startInfo.Arguments = $"{getTextureFormatName()} {file_source}";
                        if (file_target_compressed_size > 0) {
                            file_source =  file_source.Replace(".png", $".{getTextureFormatName()}");
                        }
                    } else if (file_texture_format == TextureFormat.RGBA32) {
                        // convertToRGBA32(file_source); // TODO
                        file_source = file_source.Replace(".png",".rgba32");
                    } else {
                        Console.WriteLine($"- ERROR: Unsupported texture format {getTextureFormatName()}");
                    }
                }
            }

            public static void setTargetSize(int size) {
                file_target_compressed_size = size;
                file_target_uncompressed_size = size;
            }
        }

        public class TableEntry {
            public static int table_entry_index;
            public static int pointer_address = 0; // 0 = null
            public static int absolute_address = 0; // 0 = null
            public static int new_absolute_address = 0; // 0 = null
            public static int next_absolute_address = 0; // 0 = null
            public static bool bit_set = false;
            public static string original_sha1 = "";
            public static string new_sha1 = ""; // empty string = null
            public static string filename = ""; // empty string = null

            public TableEntry(int index) {
                table_entry_index = index;
            }

            static int debitifyAddress(int address) {
                return address & 0x7FFFFFFF;
            }

            public static void initVanillaFile(int index, int base_address, int raw_address, int next_address) {
                table_entry_index = index;
                pointer_address = base_address + (index << 2);
                absolute_address = debitifyAddress(raw_address) + Globals.main_pointer_table_offset;
                new_absolute_address = debitifyAddress(raw_address) + Globals.main_pointer_table_offset;
                next_absolute_address = next_address;
                bit_set = (raw_address & 0x80000000) != 0;
                original_sha1 = "";
                new_sha1 = "";
            }

            public static void initVanillaFile(string target_sha) {
                original_sha1 = target_sha;
                new_sha1 = target_sha;
            }

            public static bool hasChanged() {
                return original_sha1 != new_sha1;
            }
        }

        public class TableInfo {
            public static string table_name = "";
            public static TableNames table_index;
            public static string table_encoded_filename = "";
            public static string table_decoded_filename = "";
            public static bool table_dont_overwrite_compressed_sizes;
            public static int table_encoder;
            public static int table_decoder;
            public static bool table_do_not_compress;
            public static bool table_force_rewrite;
            public static bool table_force_relocate;
            public static TableEntry[] entries = {};
            public static int num_entries = 0;
            public static int absolute_address = 0; // 0 = null
            public static int new_absolute_address = 0; // 0 = null
            public static int original_compressed_size = 0; // 0 = null

            public TableInfo(
                string name = "",
                TableNames index = TableNames.MusicMIDI,
                string encoded_filename = "", // empty string = null
                string decoded_filename = "", // empty string = null
                bool dont_overwrite_compressed_sizes = false,
                int encoder = 0, // 0 = null
                int decoder = 0, // 0 = null
                bool do_not_compress = false,
                bool force_rewrite = false,
                bool force_relocate = false
            ) {
                if (name.Length == 0) {
                    table_name = $"Unknown {index}";
                } else {
                    table_name = name;
                }
                table_index = index;
                table_encoded_filename = encoded_filename;
                table_decoded_filename = decoded_filename;
                table_dont_overwrite_compressed_sizes = dont_overwrite_compressed_sizes;
                table_encoder = encoder;
                table_decoder = decoder;
                table_do_not_compress = do_not_compress;
                table_force_rewrite = force_rewrite;
                table_force_relocate = force_relocate;
            }
        }
    }
}