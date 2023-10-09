using System;

namespace DK64BuildRoutine {
    internal class Text {

    }
    internal class Credits {
        static readonly string[] rando_dev_header = {"Randomizer Developers"};
        static readonly string[] rando_assocdev_header = {"Assistant Developers"};
        static readonly string[] rando_thanks = {"Additional Thanks"};

        static readonly string[] rando_devs_0 = {"2dos", "AlmostSeagull", "Ballaam"};
        static readonly string[] rando_devs_1 = {"Bismuth", "Cfox", "KillKlli"};
        static readonly string[] rando_devs_2 = {"Lrauq", "ShadowShine57", "Znernicus"};

        static readonly string[] rando_assocdevs_0 = {"Aljex", "GloriousLiar", "JXJacob"};
        static readonly string[] rando_assocdevs_1 = {"Mittenz", "Naramgamjan", "OnlySpaghettiCode"};
        static readonly string[] rando_assocdevs_2 = {"Plessy", "Rain", "The Sound Defense", "UmedMuzl"};

        static readonly string[] rando_thanks_0 = {"Game Developers", " ", "Rareware Ltd", "Nintendo"};
        static readonly string[] rando_thanks_1 = {"Cranky's Lab (Python) Developer", "Isotarge"};
        static readonly string[] rando_thanks_2 = {"Widescreen Hack Developer", "gamemasterplc"};
        static readonly string[] rando_thanks_3 = {"SpikeVegeta", "KeiperDontCare"};
        static readonly string[] rando_thanks_4 = {"Beta Testers", "Dev Branch Testers"};

        static readonly string[] rando_links_0 = {"You have been playing", "DK64 Randomizer", "dk64randomizer.com"};
        static readonly string[] rando_links_1 = {"Discord", " ", "discord.dk64randomizer.com"};

        // BETA TESTERS
        // Adam Whitmore
        // Auphonium
        // Candy Boots
        // ChelseyXLynn
        // ChristianVega64
        // Connor75
        // CornCobX0
        // Fuzzyness
        // KaptainKohl
        // Kiwikiller67
        // Nukkuler
        // Obiyo
        // Revven
        // Riley
        // SirSmackStrikesBack
        // UsedPizza
        // VidyaJames
        // Wex_AZ
        // Zorulda

        static readonly CreditsItem[] end_sequence_cards = {
            new CreditsItem(Globals.CreditsDirection.top, Globals.CreditsType.header, rando_dev_header),
            new CreditsItem(Globals.CreditsDirection.left, Globals.CreditsType.normal, rando_devs_0),
            new CreditsItem(Globals.CreditsDirection.right, Globals.CreditsType.normal, rando_devs_1),
            new CreditsItem(Globals.CreditsDirection.left, Globals.CreditsType.normal, rando_devs_2),

            new CreditsItem(Globals.CreditsDirection.top, Globals.CreditsType.header, rando_assocdev_header),
            new CreditsItem(Globals.CreditsDirection.right, Globals.CreditsType.normal, rando_assocdevs_0),
            new CreditsItem(Globals.CreditsDirection.left, Globals.CreditsType.normal, rando_assocdevs_1),
            new CreditsItem(Globals.CreditsDirection.right, Globals.CreditsType.normal, rando_assocdevs_2),
            
            new CreditsItem(Globals.CreditsDirection.top, Globals.CreditsType.header, rando_thanks),
            new CreditsItem(Globals.CreditsDirection.left, Globals.CreditsType.normal, rando_thanks_0),
            new CreditsItem(Globals.CreditsDirection.bottom, Globals.CreditsType.normal, rando_thanks_1),
            new CreditsItem(Globals.CreditsDirection.top, Globals.CreditsType.normal, rando_thanks_2),
            new CreditsItem(Globals.CreditsDirection.right, Globals.CreditsType.normal, rando_thanks_3),
            new CreditsItem(Globals.CreditsDirection.left, Globals.CreditsType.normal, rando_thanks_4),

            new CreditsItem(Globals.CreditsDirection.top, Globals.CreditsType.longheader, rando_links_0),
            new CreditsItem(Globals.CreditsDirection.bottom, Globals.CreditsType.longheader, rando_links_1),
        };

        public class CreditsItem {
            public static Globals.CreditsDirection item_squish_from;
            public static int duration;
            public static int cooldown;
            public static string[] item_text = {};

            public CreditsItem(Globals.CreditsDirection squish_from, Globals.CreditsType subtype, string[] text) {
                item_squish_from = squish_from;
                duration = 0xA0;
                switch(subtype) {
                    case Globals.CreditsType.header:
                        duration = 0x78;
                        break;
                    case Globals.CreditsType.longheader:
                        duration = 0x78 * 2;
                        break;
                }
                item_text = text;
                cooldown = 0x9A;
            }
        }

        static bool CheckSequenceValidity() {
            if (end_sequence_cards.Length > 21) {
                Console.WriteLine("Too many cards");
                return false;
            }
            return true;
        }

        public static void createTextFile() {
            if (CheckSequenceValidity()) {
                // TODO: Write ascii to bin file
            }
        }

        public static void createSquishFile() {
            if (CheckSequenceValidity()) {
                // TODO: Write bytes to file
            }
        }
    }
}