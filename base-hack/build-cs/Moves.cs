namespace DK64BuildRoutine {
    internal class VanillaMoves {
        public enum MoveType {
            nothing,
            special,
            slam,
            gun,
            ammo_belt,
            instrument,
            flag,
            gb,
        }
        static readonly int DEFAULT_SLAM_PURCHASE = 1;

        public class MoveSlot {
            public static MoveType slot_type;
            public static int slot_move_index;
            public static int slot_price;

            public MoveSlot(MoveType type, int index=1, int price=0) {
                slot_type = type;
                slot_move_index = index;
                slot_price = price;
            }
        }

        static readonly MoveSlot[] cranky_slots_0 = {
            new MoveSlot(MoveType.special, 1, 3),
            new MoveSlot(MoveType.special, 2, 5),
            new MoveSlot(MoveType.special, 3, 7),
            new MoveSlot(MoveType.nothing),
            new MoveSlot(MoveType.slam, DEFAULT_SLAM_PURCHASE, 5),
            new MoveSlot(MoveType.nothing),
            new MoveSlot(MoveType.slam, DEFAULT_SLAM_PURCHASE, 7),
            new MoveSlot(MoveType.nothing),
        };

        static readonly MoveSlot[] cranky_slots_1 = {
            new MoveSlot(MoveType.special, 1, 3),
            new MoveSlot(MoveType.nothing),
            new MoveSlot(MoveType.special, 2, 5),
            new MoveSlot(MoveType.nothing),
            new MoveSlot(MoveType.slam, DEFAULT_SLAM_PURCHASE, 5),
            new MoveSlot(MoveType.special, 3, 7),
            new MoveSlot(MoveType.slam, DEFAULT_SLAM_PURCHASE, 7),
            new MoveSlot(MoveType.nothing),
        };
        
        static readonly MoveSlot[] funky_slots = {
            new MoveSlot(MoveType.gun, 1, 3),
            new MoveSlot(MoveType.nothing),
            new MoveSlot(MoveType.ammo_belt, 1, 3),
            new MoveSlot(MoveType.nothing),
            new MoveSlot(MoveType.gun, 2, 5),
            new MoveSlot(MoveType.ammo_belt, 2, 5),
            new MoveSlot(MoveType.gun, 3, 7),
            new MoveSlot(MoveType.nothing),
        };

        static readonly MoveSlot[] candy_slots = {
            new MoveSlot(MoveType.nothing),
            new MoveSlot(MoveType.instrument, 1, 3),
            new MoveSlot(MoveType.nothing),
            new MoveSlot(MoveType.instrument, 2, 5),
            new MoveSlot(MoveType.nothing),
            new MoveSlot(MoveType.instrument, 3, 7),
            new MoveSlot(MoveType.instrument, 3, 9),
            new MoveSlot(MoveType.nothing),
        };

        static readonly MoveSlot[] training_slots = {
            new MoveSlot(MoveType.flag, 0x182),
            new MoveSlot(MoveType.flag, 0x184),
            new MoveSlot(MoveType.flag, 0x185),
            new MoveSlot(MoveType.flag, 0x183),
        };

        static readonly MoveSlot[] bfi_slots = {
            new MoveSlot(MoveType.flag, -2),
        };

        static readonly MoveSlot[] firstmove_slots = {
            new MoveSlot(MoveType.nothing),
        };
    }
}