using System;
using ConnectorLib;
using ConnectorLib.Memory;
using CrowdControl.Common;
using JetBrains.Annotations;
using ConnectorType = CrowdControl.Common.ConnectorType;

namespace CrowdControl.Games.Packs.DonkeyKong64Randomizer;

[UsedImplicitly]
public class DonkeyKong64Randomizer : N64EffectPack
{
    //private DomainMappedConnector RDRAM;

    public DonkeyKong64Randomizer(UserRecord player, Func<CrowdControlBlock, bool> responseHandler,
        Action<object> statusUpdateHandler) : base(player, responseHandler, statusUpdateHandler)
    {
        ConnectorAttached += (_, _) => Init();
    }

    private void Init()
    {
        //RDRAM = new(Connector, "RDRAM");
        DRUNK_STATE = AddressChain.Begin(Connector).Move(ADDR_STATE_POINTER).Follow(4, Endianness.BigEndian, PointerType.Absolute).Move(0x0);
        NO_TA_STATE = AddressChain.Begin(Connector).Move(ADDR_STATE_POINTER).Follow(4, Endianness.BigEndian, PointerType.Absolute).Move(0x1);
        ICE_STATE = AddressChain.Begin(Connector).Move(ADDR_STATE_POINTER).Follow(4, Endianness.BigEndian, PointerType.Absolute).Move(0x2);
        ROCKFALL_STATE = AddressChain.Begin(Connector).Move(ADDR_STATE_POINTER).Follow(4, Endianness.BigEndian, PointerType.Absolute).Move(0x3);
        RAP_STATE = AddressChain.Begin(Connector).Move(ADDR_STATE_POINTER).Follow(4, Endianness.BigEndian, PointerType.Absolute).Move(0x4);
        KOP_STATE = AddressChain.Begin(Connector).Move(ADDR_STATE_POINTER).Follow(4, Endianness.BigEndian, PointerType.Absolute).Move(0x5);
        BALLOON_STATE = AddressChain.Begin(Connector).Move(ADDR_STATE_POINTER).Follow(4, Endianness.BigEndian, PointerType.Absolute).Move(0x6);
        SLIP_STATE = AddressChain.Begin(Connector).Move(ADDR_STATE_POINTER).Follow(4, Endianness.BigEndian, PointerType.Absolute).Move(0x7);
        TAG_STATE = AddressChain.Begin(Connector).Move(ADDR_STATE_POINTER).Follow(4, Endianness.BigEndian, PointerType.Absolute).Move(0x8);
        BACKFLIP_STATE = AddressChain.Begin(Connector).Move(ADDR_STATE_POINTER).Follow(4, Endianness.BigEndian, PointerType.Absolute).Move(0x9);
        ICEFLOOR_STATE = AddressChain.Begin(Connector).Move(ADDR_STATE_POINTER).Follow(4, Endianness.BigEndian, PointerType.Absolute).Move(0xA);
        GETOUT_STATE = AddressChain.Begin(Connector).Move(ADDR_STATE_POINTER).Follow(4, Endianness.BigEndian, PointerType.Absolute).Move(0xB);
        MINI_STATE = AddressChain.Begin(Connector).Move(ADDR_STATE_POINTER).Follow(4, Endianness.BigEndian, PointerType.Absolute).Move(0xC);
        BOULDER_STATE = AddressChain.Begin(Connector).Move(ADDR_STATE_POINTER).Follow(4, Endianness.BigEndian, PointerType.Absolute).Move(0xD);
        ANIMALTRANSFORM_STATE = AddressChain.Begin(Connector).Move(ADDR_STATE_POINTER).Follow(4, Endianness.BigEndian, PointerType.Absolute).Move(0xE);
    }

    private AddressChain DRUNK_STATE;
    private AddressChain NO_TA_STATE;
    private AddressChain ICE_STATE;
    private AddressChain ROCKFALL_STATE;
    private AddressChain RAP_STATE;
    private AddressChain KOP_STATE;
    private AddressChain BALLOON_STATE;
    private AddressChain SLIP_STATE;
    private AddressChain TAG_STATE;
    private AddressChain BACKFLIP_STATE;
    private AddressChain ICEFLOOR_STATE;
    private AddressChain GETOUT_STATE;
    private AddressChain MINI_STATE;
    private AddressChain BOULDER_STATE;
    private AddressChain ANIMALTRANSFORM_STATE;

    private const uint ADDR_STATE_POINTER = 0x807FFFB4;
    private const uint ADDR_MAP_TIMER = 0x8076A064;
    private const uint ADDR_PLAYER_POINTER = 0x807FBB4C;
    private const uint ADDR_AUTOWALK_STATE = 0x807463B8;
    private const uint ADDR_CURRENT_GAMEMODE = 0x80755314;
    private const uint ADDR_NEXT_GAMEMODE = 0x80755318;
    private const uint ADDR_TBVOID_BYTE = 0x807FBB63;
    private const uint ADDR_KONG_BASE = 0x807FC950;
    private const uint ADDR_RANDO_CANARY = 0x807FFFF4;
    private const uint ADDR_CUTSCENE_ACTIVE = 0x807444EC;
    private const uint ADDR_TRANSITION_SPEED = 0x807FD88C;
    private const uint ADDR_STANDARD_AMMO = 0x807FCC40;
    private const uint ADDR_HOMING_AMMO = 0x807FCC42;
    private const uint ADDR_ORANGES = 0x807FCC44;
    private const uint ADDR_CRYSTALS = 0x807FCC46;
    private const uint ADDR_FILM = 0x807FCC48;
    private const uint ADDR_HEALTH = 0x807FCC4B;
    private const uint ADDR_MELONS = 0x807FCC4C;
    private const uint ADDR_GLOBAL_INSTRUMENT = 0x807FCC4E;
    private const uint ADDR_APPLIED_DAMAGE_MULTIPLIER = 0x807FF8A5;
    private const uint ADDR_ORIGINAl_DAMAGE_MULTIPLIER = 0x807FFFF9;
    private const uint ADDR_BASE_ASPECT = 0x80010520;
    private const uint ADDR_CURRENT_MAP = 0x8076A0AB;
    private const uint ADDR_LEVEL_TABLE = 0x807445E0;

    private const byte COIN_CHANGE_AMOUNT = 2;
    private enum CC_STATE
    {
        CC_READY, // 0
        CC_ENABLING, // 1
        CC_ENABLED, // 2
        CC_DISABLING, // 3
        CC_LOCKED, // 4
    }

    public override Game Game { get; } = new("Donkey Kong 64 Randomizer", "DonkeyKong64Randomizer", "N64", ConnectorType.N64Connector);

    public override EffectList Effects { get; } = new List<Effect>
    {
        // Player
        new("Drunk Kong","drunky_kong") { Price = 0, Duration = 10, Description = "Makes the kong feel a little woozy. Reverses controls and slows down the player.", Category="Player" },
        new("Disable Tag Anywhere","disable_ta") { Price = 0, Duration = 25, Description = "Disables the ability for the player to use Tag Anywhere.", Category="Player" },
        new("Ice Trap the Player","ice_trap") { Price = 0, Description = "Locks the player in an ice trap bubble in which they have to escape.", Category="Player" },
        new("Spawn Stalactites","rockfall") { Price = 0, Duration = 30, Description = "Spawn a bunch of stalactites above the player throughout the duration of the effect.", Category="Player" },
        new("Instant Balloon","balloon") { Price = 0, Description = "Inflate the balloon (kong) just like a balloon.", Category="Player" },
        new("High Gravity","gravity_high") { Price = 0, Duration = 15, Description = "Crank(y) that gravity up to 11.", Category="Player" },
        new("Low Gravity","gravity_low") { Price = 0, Duration = 15, Description = "Make the moonkick not so special anymore.", Category="Player" },
        new("Slip","player_slip") { Price = 0, Description = "Who placed a banana under the DK's foot?", Category="Player" },
        new("Change Kong","tag_kong") { Price = 0, Duration = 20, Description = "Change the player to a different kong and lock tagging", Category="Player" },
        new("Do a Backflip","backflip") { Price = 0, Description = "Peppy says: 'Do a backflip'.", Category="Player" },
        new("Ice Floor","ice_floor") { Price = 0, Duration = 20, Description = "Donkey goes weeeeeeee.", Category="Player" },
        new("Mini Monkey","force_mini") { Price = 0, Duration = 20, Description = "Shrink the player's size to suit their mood.", Category="Player" },
        new("Transform into an Animal","animal_transform") { Price = 0, Duration = 15, Description = "Transforms the player into an animal. If they're in water, they'll be transformed to Enguarde, otherwise they'll be transformed to Rambi.", Category="Player" },
        // Inventory
        new("Give Coins","give_coins") { Price = 0, Description = "Gives each kong 2 coins.", Category="Inventory" },
        new("Remove Coins","remove_coins") { Price = 0, Description = "Takes 2 coins from each kong.", Category="Inventory" },
        new("Give Consumables","give_replenishibles") { Price = 0, Description = "Help the player out by giving them some ammo, crystals amongst other things.", Category="Inventory" },
        new("Remove all Consumables","remove_replenishibles") { Price = 0, Description = "Remove everything the player has in terms of ammo, crystals and other things.", Category="Inventory" },
        new("Give a Golden Banana","give_gb") { Price = 0, Description = "Gives the player a Golden Banana. OHHHHHHHH BANANA.", Category="Inventory" },
        new("Remove a Golden Banana","remove_gb") { Price = 0, Description = "Removes a Golden Banana from the player.", Category="Inventory" },
        // Health
        new("Refill Health","refill_health") { Price = 0, Description = "Refills the player's health to max.", Category="Health" },
        new("One Hit KO","damage_ohko") { Price = 0, Duration = 20, Description = "The player will be killed for any damage taken.", Category="Health" },
        new("Double Damage","damage_double") { Price = 0, Duration = 30, Description = "The player will take double damage.", Category="Health" },
        // Misc
        new("Get Kaught","spawn_kop") { Price = 0, Description = "Spawn the greatest kop on the service to catch the player in their tracks.", Category="Misc" },
        new("Get Out","get_out") { Price = 0, Description = "Gives the player 10 seconds to get into another map, otherwise they die.", Category="Misc" },
        new("Spawn a Boulder","spawn_boulder") { Price = 0, Description = "Spawns a boulder: Useful for breaking the logic of your favorite monkey game.", Category="Misc" },
        new("Flip Screen","flip_screen") { Price = 0, Duration = 10, Description = "Flips the screen vertically.", Category="Misc" },
        new("Warp to the DK Rap","play_the_rap") { Price = 0, Duration = 188, Description = "Warps the player to the DK Rap, and warps them back after the rap is finished or the effect is cancelled (whichever comes first). Effect is capped at 188 seconds.", Category="Misc" },
    };

    public override ROMTable ROMTable => new[]
    {
        new ROMInfo("DK64 (US)", null, Patching.Ignore, ROMStatus.NotSupported, s => Patching.MD5(s).Equals("9ec41abf2519fc386cadd0731f6e868c", StringComparison.InvariantCultureIgnoreCase), "This is the North American Vanilla ROM and is therefore not supported."),
        new ROMInfo("DK64 Randomizer", null, Patching.Ignore, ROMStatus.ValidPatched, s => Patching.Fingerprint(s, 0x3B, new byte[] { 0x4E, 0x44, 0x4F, 0x45 }))
    };

    protected override GameState GetGameState()
    {
        if (!Connector.Connected) return GameState.Unknown;

        if (!Connector.Read8(ADDR_CURRENT_GAMEMODE, out byte current_gamemode)) return GameState.Unknown;
        if (!Connector.Read8(ADDR_NEXT_GAMEMODE, out byte next_gamemode)) return GameState.Unknown;
        if (!Connector.Read32(ADDR_MAP_TIMER, out uint map_timer)) return GameState.Unknown;
        if (!Connector.Read32(ADDR_PLAYER_POINTER, out uint player_pointer)) return GameState.Unknown;
        if (!Connector.Read8(ADDR_TBVOID_BYTE, out byte tb_void_byte)) return GameState.Unknown;
        if (!Connector.Read8(ADDR_RANDO_CANARY, out byte rando_version)) return GameState.Unknown;
        if (!Connector.Read8(ADDR_CUTSCENE_ACTIVE, out byte cutscene_state)) return GameState.Unknown;
        if (!Connector.ReadFloat(ADDR_TRANSITION_SPEED, out float transition_speed)) return GameState.Unknown;
        if (!Connector.ReadFloat(ADDR_STATE_POINTER, out float state_pointer)) return GameState.Unknown;
        if (rando_version != 4)
        {
            // Not randomizer or a currently supported version
            return GameState.Unknown;
        }
        if (state_pointer == 0)
        {
            // CC Data not yet loaded
            return GameState.Unknown;
        }
        if ((current_gamemode != 6) || (next_gamemode != 6))
        {
            // Not in adventure mode
            return GameState.WrongMode;
        }
        if (map_timer < 2)
        {
            // Loading
            return GameState.BadPlayerState;
        }
        if (player_pointer == 0)
        {
            // No player, also loading
            return GameState.BadPlayerState;
        }
        if (Connector.IsNonZero8(ADDR_AUTOWALK_STATE))
        {
            // Player is autowalking
            return GameState.BadPlayerState;
        }
        if ((tb_void_byte & 3) != 0)
        {
            // Player is pausing or is paused
            return GameState.Paused;
        }
        if ((tb_void_byte & 0x30) == 0)
        {
            // Player is in tag
            return GameState.BadPlayerState;
        }
        if ((cutscene_state == 3) || (cutscene_state == 4))
        {
            // In Arcade/Jetpac
            return GameState.SafeArea;
        }
        if (cutscene_state != 0)
        {
            // Cutscene is playing
            return GameState.Paused;
        }
        if (transition_speed > 0.0f)
        {
            // Transitioning to another map
            return GameState.BadPlayerState;
        }
        //probably want to do a general state check here?
        //there are A LOT of GameState return values to choose from so be sure to pick the right one
        //nothing works unless you return GameState.Ready, every other state is just an informational failure state

        //if (!ADDR_CC_STATE.TryGetByte(out byte value)) return GameState.Unmodded;
        //return (value == (int)CC_STATE.CC_READY) ? GameState.Ready : GameState.PipelineBusy;
        return GameState.Ready;
    }

    public override List<string> MetadataCommon { get; } = ["lives"];

    protected override async Task<DataResponse> RequestData(string key)
    {
        switch (key)
        {
            case "lives":
                //read out whatever value you want here
                return DataResponse.Success(key, 0);
            default:
                return await base.RequestData(key);
        }
    }

    private bool Write16(uint address, ushort value)
    {
        byte upper = (byte)(value >> 8);
        byte lower = (byte)(value & 0xFF);
        bool result = true;
        result &= Connector.Write8(address + 0, upper);
        result &= Connector.Write8(address + 1, lower);
        return result;
    }

    private bool Add16(uint address, short change, short lower_bound, short upper_bound)
    {
        bool result = true;
        result &= Connector.Read8(address + 0, out byte upper);
        result &= Connector.Read8(address + 1, out byte lower);
        short value = (short)((upper << 8) + lower);
        value += change;
        if (value < lower_bound)
        {
            value = lower_bound;
        }
        else if (value > upper_bound)
        {
            value = upper_bound;
        }
        result &= Connector.Write8(address + 0, (byte)(value >> 8));
        result &= Connector.Write8(address + 1, (byte)(value & 0xFF));
        return result;
    }

    private bool Write32(uint address, int value)
    {
        bool result = true;
        byte b0 = (byte)((value >> 24) & 0xFF);
        byte b1 = (byte)((value >> 16) & 0xFF);
        byte b2 = (byte)((value >> 8) & 0xFF);
        byte b3 = (byte)((value >> 0) & 0xFF);
        result &= Connector.Write8(address + 0, b0);
        result &= Connector.Write8(address + 1, b1);
        result &= Connector.Write8(address + 2, b2);
        result &= Connector.Write8(address + 3, b3);
        return result;
    }

    private int floattoint(float value)
    {
        byte[] bytes = BitConverter.GetBytes(value);
        return BitConverter.ToInt32(bytes, 0);
    }

    private bool WriteFloat(uint address, float value)
    {
        int val_i = floattoint(value);
        return Write32(address, val_i);
    }

    private bool WriteDouble(uint address, double value)
    {
        bool result = true;
        byte[] bytes = BitConverter.GetBytes(value);
        int val_i = BitConverter.ToInt32(bytes, 0);
        result &= Write32(address, val_i);
        val_i = BitConverter.ToInt32(bytes, 4);
        result &= Write32((uint)(address + 4), val_i);
        return result;
    }

    private bool isDefaultGravity()
    {
        bool result = true;
        result &= Connector.Read16(0x80750300, out ushort gravity_checker);
        if (gravity_checker != 0xC1A0) {
            return false;
        }
        return result;
    }

    private bool ChangeGravity(float scale)
    {
        if (scale == 0) return false;
        float inverse_scale = 1 / scale; // Used for positive values
        bool result = true;
        // 8068B38C - Set by the trigger
        // 8068F858 - Hardcoded -30 // Boat
        result &= WriteFloat(0x80750300, (float)(-20 * scale));
        result &= WriteFloat(0x807502F8, (float)(-28 * scale)); // Subtracted from with a random value (???)
        // 806AE064 - Hardcoded -30 // Krossbones Head
        // 806b40ac - Hardcoded? // Enemies
        result &= WriteFloat(0x807502EC, (float)(-15 * scale));
        result &= WriteFloat(0x807502E8, (float)(-20 * scale));
        result &= WriteFloat(0x807502F4, (float)(-30 * scale)); // Seal

        result &= WriteFloat(0x80753578, (float)(-20 * scale)); // yaccel array
        result &= WriteFloat(0x8075357C, (float)(-20 * scale)); // yaccel array
        result &= WriteFloat(0x80753580, (float)(-30 * scale)); // yaccel array
        result &= WriteFloat(0x80753584, (float)(-30 * scale)); // yaccel array
        result &= WriteFloat(0x80753588, (float)(-20 * scale)); // yaccel array
        result &= WriteFloat(0x8075358C, (float)(-20 * scale)); // yaccel array
        result &= WriteFloat(0x80753590, (float)(-30 * scale)); // yaccel array
        for (byte i = 0; i < 7; i++)
        {
            result &= WriteFloat((uint)(0x807537A8 + (4 * i)), (float)(-10.66 * scale)); // 807537A8 array
            result &= WriteFloat((uint)(0x80753738 + (4 * i)), (float)(-14 * scale)); // 80753738 array
            result &= WriteFloat((uint)(0x80753024 + (4 * i)), (float)(-20 * scale)); // 80753024 array
            result &= WriteFloat((uint)(0x80753754 + (4 * i)), (float)(-14 * scale)); // 80753754 array
            result &= WriteFloat((uint)(0x80753700 + (4 * i)), (float)(-14 * scale)); // 80753700 array
            result &= WriteFloat((uint)(0x80753658 + (4 * i)), (float)(-25 * scale)); // 80753658 array
            result &= WriteFloat((uint)(0x807536E4 + (4 * i)), (float)(-10.67 * scale)); // 807536E4 array
            result &= WriteFloat((uint)(0x8075363C + (4 * i)), (float)(-17.78 * scale)); // 8075363C array
            result &= WriteFloat((uint)(0x8075310C + (4 * i)), (float)(-20 * scale)); // 8075310C array
        }
        // 806d146c - hardcoded -8 // Enguarde leap?
        // 806D5090 - hardcoded -30 // Simian Slam

        result &= WriteFloat(0x8075CE60, (float)(-0.001 * scale)); // Cannon short
        // 806d9dd4 - hardcoded 2
        result &= WriteDouble(0x8075CE80, 150 * (1 / scale));
        result &= WriteFloat(0x8075CE88, (float)(-0.001 * scale)); // Updraft
        result &= WriteDouble(0x8075CEA8, 0.036 * inverse_scale);
        result &= WriteFloat(0x8075CEB0, (float)(-0.001 * scale));
        result &= WriteFloat(0x8075EB4C, (float)(-2.5 * scale)); // Aerial attack, specially patching this for a moonkick (everyone is gonna do this, so need to plan for this)
        // 806DA13C - hardcoded -1
        // 806DA28C - hardcoded -1
        result &= WriteDouble(0x8075D308, 0.2 * inverse_scale); // balloon

        // Reset player yaccel
        AddressChain ADDR_YACCEL = AddressChain.Begin(Connector).Move(ADDR_PLAYER_POINTER).Follow(4, Endianness.BigEndian, PointerType.Absolute).Move(0xC4);
        result &= WriteFloat((uint)(ADDR_YACCEL.Address), -20 * scale);
        return result;
    }

    private bool resetDamageMultiplier()
    {
        bool result = true;
        result &= Connector.Read8(ADDR_ORIGINAl_DAMAGE_MULTIPLIER, out byte damage_multiplier);
        result &= Connector.Write8(ADDR_APPLIED_DAMAGE_MULTIPLIER, damage_multiplier);
        return result;
    }

    private static readonly short[] BANNED_GETOUT_MAPS = [
        0x00CB, // DK Phase
        0x00CC, // Diddy Phase
        0x00CD, // Lanky Phase
        0x00CE, // Tiny Phase
        0x00CF, // Chunky Phase
        0x00D6, // Shoe
        0x00D7, // Cutscene Map
        0x0006, // Japes Minecart
        0x0037, // Fungi Minecart
        0x006A, // Castle Minecart
        0x0061, // K. Lumsy
    ];

    private static readonly short[] BANNED_CONTROL_STATES = [
        0x0006, // Locked - Bonus
        0x0007, // Minecart - Idle
        0x0008, // Minecart - Crouch
        0x0009, // Minecart - Jump
        0x000A, // Minecart - Left
        0x000B, // Minecart - Right
        0x003B, // Death - Lava
        0x0042, // Tag Barrel lock
        0x0043, // Underwater
        0x0044, // BBlast shot
        0x0052, // Bananaport
        0x0053, // Monkeyport
        0x0054, // Bananaport (Multiplayer)
        0x0056, // Locked - Learning move
        0x0064, // Taking photo
        0x0065, // Taking photo (Underwater)
        0x0067, // Instrument
        0x006A, // Learning Gun
        0x006B, // Locked (Bonus Barrel)
        0x006D, // Boat
        0x0075, // Castle Car Race
        0x0076, // Entering Crown
        0x0077, // Cutscene Lock
        0x0078, // Gorilla Grab
        0x0079, // Learning Move
        0x007A, // Locked
        0x007B, // Locked
        0x007C, // Trap Bubble
        0x007D, // Beaver Bother
        0x0083, // Fairy Refill
        0x0087, // Enter Portal
        0x0088, // Exit Portal
    ];

    private bool isGoodMovementState()
    {
        bool result = true;
        AddressChain ADDR_CONTROL_STATE = AddressChain.Begin(Connector).Move(ADDR_PLAYER_POINTER).Follow(4, Endianness.BigEndian, PointerType.Absolute).Move(0x154);
        result &= Connector.Read8((uint)(ADDR_CONTROL_STATE.Address), out byte control_state_id);
        if (!result)
        {
            return false;
        }
        if (BANNED_CONTROL_STATES.Contains(control_state_id))
        {
            return false;
        }
        return true;
    }

    private bool resetScreen()
    {
        return Connector.Write8(ADDR_BASE_ASPECT, (byte)(0x3F));
    }

    private bool isNotBonus()
    {
        if (!Connector.Read8(ADDR_CURRENT_MAP, out byte map_id)) return false;
        uint level_addr = (uint)(ADDR_LEVEL_TABLE + map_id);
        if (!Connector.Read8(level_addr, out byte level_id)) return false;
        if ((level_id == 9) || (level_id == 13))
        {
            return false;
        }
        return true;
    }

    protected override void StartEffect(EffectRequest request)
    {
        switch (request.EffectID)
        {
            case "drunky_kong":
                StartTimed(request,
                    () => Connector.IsEqual8(DRUNK_STATE, (byte)CC_STATE.CC_READY),
                    () =>
                    {
                        bool result = DRUNK_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING);
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} gave you a bottle of rum.");
                        }
                        return result;
                    });
                return;
            case "disable_ta":
                StartTimed(request,
                    () => Connector.IsEqual8(NO_TA_STATE, (byte)CC_STATE.CC_READY),
                    () =>
                    {
                        bool result = NO_TA_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING);
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} disabled Tag Anywhere.");
                        }
                        return result;
                    });
                return;
            case "ice_trap":
                TryEffect(request,
                    () =>
                    {
                        Connector.SendMessage($"State Address: {ICE_STATE}.");
                        return Connector.IsEqual8(ICE_STATE, (byte)CC_STATE.CC_READY);
                    },
                    () =>
                    {
                        bool result = ICE_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING);
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} made a fool out of you.");
                        }
                        return result;
                    });
                return;
            case "rockfall":
                StartTimed(request,
                    () => Connector.IsEqual8(ROCKFALL_STATE, (byte)CC_STATE.CC_READY),
                    () =>
                    {
                        bool result = ROCKFALL_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING);
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} is raining down rocks.");
                        }
                        return result;
                    });
                return;
            case "force_mini":
                StartTimed(request,
                    () => Connector.IsEqual8(MINI_STATE, (byte)CC_STATE.CC_READY),
                    () =>
                    {
                        bool result = MINI_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING);
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} has shrunk your size.");
                        }
                        return result;
                    });
                return;
            case "animal_transform":
                StartTimed(request,
                    () => Connector.IsEqual8(ANIMALTRANSFORM_STATE, (byte)CC_STATE.CC_READY),
                    () =>
                    {
                        bool result = ANIMALTRANSFORM_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING);
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} has changed you into an animal buddy.");
                        }
                        return result;
                    });
                return;
            case "play_the_rap":
                StartTimed(request,
                    () => Connector.IsEqual8(RAP_STATE, (byte)CC_STATE.CC_READY),
                    () =>
                    {
                        bool result = RAP_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING);
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} is appreciating Grant Kirkhope.");
                        }
                        return result;
                    });
                return;
            case "spawn_kop":
                TryEffect(request,
                    () =>
                    {
                        bool result = Connector.IsEqual8(KOP_STATE, (byte)CC_STATE.CC_READY);
                        result &= isNotBonus();
                        return result;
                    },
                    () =>
                    {
                        bool result = KOP_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING);
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} recruited the best kop in the force (sorry, Service. 'Force' is too aggressive).");
                        }
                        return result;
                    });
                return;
            case "balloon":
                TryEffect(request,
                    () =>
                    {
                        bool result = true;
                        result &= Connector.IsEqual8(BALLOON_STATE, (byte)CC_STATE.CC_READY);
                        result &= isGoodMovementState();
                        return result;
                    },
                    () =>
                    {
                        bool result = BALLOON_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING);
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} inflated the balloon, just like a balloon.");
                        }
                        return result;
                    });
                return;
            case "player_slip":
                TryEffect(request,
                    () =>
                    {
                        bool result = true;
                        result &= Connector.IsEqual8(SLIP_STATE, (byte)CC_STATE.CC_READY);
                        result &= isGoodMovementState();
                        return result;
                    },
                    () =>
                    {
                        bool result = SLIP_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING);
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} placed a banana under your foot.");

                        }
                        return result;
                    });
                return;
            case "tag_kong":
                StartTimed(request,
                    () => Connector.IsEqual8(TAG_STATE, (byte)CC_STATE.CC_READY),
                    () =>
                    {
                        bool result = TAG_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING);
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} changed your kong and disabled tag anywhere.");
                        }
                        return result;
                    });
                return;
            case "backflip":
                TryEffect(request,
                    () => Connector.IsEqual8(BACKFLIP_STATE, (byte)CC_STATE.CC_READY),
                    () =>
                    {
                        bool result = BACKFLIP_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING);
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} made your kong backflip.");
                        }
                        return result;
                    });
                return;
            case "spawn_boulder":
                TryEffect(request,
                    () => Connector.IsEqual8(BOULDER_STATE, (byte)CC_STATE.CC_READY),
                    () =>
                    {
                        bool result = BOULDER_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING);
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} spawned a boulder for you.");
                        }
                        return result;
                    });
                return;
            case "ice_floor":
                StartTimed(request,
                    () => Connector.IsEqual8(ICEFLOOR_STATE, (byte)CC_STATE.CC_READY),
                    () =>
                    {
                        bool result = ICEFLOOR_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING);
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} turned the floor into ice.");
                        }
                        return result;
                    });
                return;
            case "get_out":
                TryEffect(request,
                    () =>
                    {
                        bool result = true;
                        result &= Connector.IsEqual8(GETOUT_STATE, (byte)CC_STATE.CC_READY);
                        // Doesn't seem to break if started in K Rool
                        // if (!Connector.Read8(ADDR_CURRENT_MAP, out byte map_id)) return false;
                        // if (BANNED_GETOUT_MAPS.Contains(map_id))
                        // {
                        //     result = false;
                        // }
                        result &= isNotBonus();
                        return result;
                    },
                    () =>
                    {
                        bool result = GETOUT_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING);
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} is making you GET OUT!");
                        }
                        return result;
                    });
                return;
            case "give_coins":
                TryEffect(request,
                    () =>
                    {
                        for (byte kong = 0; kong < 5; kong++)
                        {
                            if (!Connector.Read8((uint)(ADDR_KONG_BASE + (kong * 0x5E) + 7), out byte coin_count)) return false;
                            if (coin_count < 255)
                            {
                                return true;
                            }
                        }
                        return false;
                    },
                    () =>
                    {
                        bool result = true;
                        for (byte kong = 0; kong < 5; kong++)
                        {
                            uint coin_addr = (uint)(ADDR_KONG_BASE + (kong * 0x5E) + 7);
                            result &= Connector.Read8(coin_addr, out byte coin_count);
                            if (coin_count < (255 - COIN_CHANGE_AMOUNT))
                            {
                                result &= Connector.Write8(coin_addr, (byte)(coin_count + COIN_CHANGE_AMOUNT));
                            }
                            else
                            {
                                result &= Connector.Write8(coin_addr, 255);
                            }
                        }
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} gave you coins. How generous.");
                        }
                        return result;
                    });
                return;
            case "remove_coins":
                TryEffect(request,
                    () =>
                    {
                        for (byte kong = 0; kong < 5; kong++)
                        {
                            if (!Connector.Read8((uint)(ADDR_KONG_BASE + (kong * 0x5E) + 7), out byte coin_count)) return false;
                            if (coin_count > 0)
                            {
                                return true;
                            }
                        }
                        return false;
                    },
                    () =>
                    {
                        bool result = true;
                        for (byte kong = 0; kong < 5; kong++)
                        {
                            uint coin_addr = (uint)(ADDR_KONG_BASE + (kong * 0x5E) + 7);
                            result &= Connector.Read8(coin_addr, out byte coin_count);
                            if (coin_count > COIN_CHANGE_AMOUNT)
                            {
                                result &= Connector.Write8(coin_addr, (byte)(coin_count - COIN_CHANGE_AMOUNT));
                            }
                            else
                            {
                                result &= Connector.Write8(coin_addr, 0);
                            }
                        }
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} took some coins away. Scandalous!");
                        }
                        return result;
                    });
                return;
            case "give_replenishibles":
                TryEffect(request,
                    () => true,
                    () =>
                    {
                        bool result = true;
                        result &= Add16(ADDR_STANDARD_AMMO, 5, 0, 200);
                        result &= Add16(ADDR_HOMING_AMMO, 5, 0, 200);
                        result &= Add16(ADDR_ORANGES, 1, 0, 30);
                        result &= Add16(ADDR_CRYSTALS, 150, 0, 3000);
                        result &= Add16(ADDR_FILM, 1, 0, 20);
                        result &= Add16(ADDR_GLOBAL_INSTRUMENT, 1, 0, 20);
                        for (byte kong = 0; kong < 5; kong++)
                        {
                            result &= Add16((uint)(ADDR_KONG_BASE + (kong * 0x5E) + 8), 1, 0, 20);
                        }
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} restocked your inventory.");
                        }
                        return result;
                    });
                return;
            case "remove_replenishibles":
                TryEffect(request,
                    () => true,
                    () =>
                    {
                        bool result = true;
                        result &= Write16(ADDR_STANDARD_AMMO, 0);
                        result &= Write16(ADDR_HOMING_AMMO, 0);
                        result &= Write16(ADDR_ORANGES, 0);
                        result &= Write16(ADDR_CRYSTALS, 0);
                        result &= Write16(ADDR_FILM, 0);
                        result &= Write16(ADDR_GLOBAL_INSTRUMENT, 0);
                        for (byte kong = 0; kong < 5; kong++)
                        {
                            result &= Write16((uint)(ADDR_KONG_BASE + (kong * 0x5E) + 8), 0);
                        }
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} took all your consumables.");
                        }
                        return result;
                    });
                return;
            case "give_gb":
                TryEffect(request,
                    () => true,
                    () =>
                    {
                        byte min_kong = 0;
                        byte min_level = 0;
                        ushort min_gb = 65535;
                        bool result = true;
                        for (byte kong = 0; kong < 5; kong++)
                        {
                            for (byte level = 0; level < 8; level++)
                            {
                                result &= Connector.Read8((uint)(ADDR_KONG_BASE + (kong * 0x5E) + 0x43 + (2 * level)), out byte gb_count);
                                if (gb_count < min_gb)
                                {
                                    min_gb = gb_count;
                                    min_kong = kong;
                                    min_level = level;
                                }
                            }
                        }
                        uint gb_add_address = (uint)(ADDR_KONG_BASE + (min_kong * 0x5E) + 0x43 + (2 * min_level));
                        result &= Connector.Write8(gb_add_address, (byte)(min_gb + 1));
                        if (result)
                        {
                            Connector.SendMessage($"OHHHHHH BANANA! {request.DisplayViewer} gave you a banana.");
                        }
                        return result;
                    });
                return;
            case "remove_gb":
                TryEffect(request,
                    () =>
                    {
                        for (byte kong = 0; kong < 5; kong++)
                        {
                            for (byte level = 0; level < 8; level++)
                            {
                                uint gb_add_address = (uint)(ADDR_KONG_BASE + (kong * 0x5E) + 0x43 + (2 * level));
                                if (!Connector.Read8(gb_add_address, out byte gb_count)) return false;
                                if (gb_count > 0)
                                {
                                    return true;
                                }
                            }
                        }
                        return false;
                    },
                    () =>
                    {
                        bool result = true;
                        for (byte kong = 0; kong < 5; kong++)
                        {
                            for (byte level = 0; level < 8; level++)
                            {
                                uint gb_add_address = (uint)(ADDR_KONG_BASE + (kong * 0x5E) + 0x43 + (2 * level));
                                result &= Connector.Read8(gb_add_address, out byte gb_count);
                                if (gb_count > 0)
                                {
                                    result &= Connector.Write8(gb_add_address, (byte)(gb_count - 1));
                                    return result;
                                }
                            }
                        }
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} stole one of your bananas.");
                        }
                        return result;
                    });
                return;
            case "refill_health":
                TryEffect(request,
                    () => true,
                    () =>
                    {
                        bool result = true;
                        result &= Connector.Read8(ADDR_MELONS, out byte melon_count);
                        result &= Connector.Write8(ADDR_HEALTH, (byte)(melon_count * 4));
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} refilled your health.");
                        }
                        return result;
                    });
                return;
            case "damage_ohko":
                StartTimed(request,
                    () => true,
                    () =>
                    {
                        bool result = Connector.Write8(ADDR_APPLIED_DAMAGE_MULTIPLIER, (byte)(12));
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} enabled One-Hit KO.");
                        }
                        return result;
                    });
                return;
            case "damage_double":
                StartTimed(request,
                    () => true,
                    () =>
                    {
                        bool result = Connector.Write8(ADDR_APPLIED_DAMAGE_MULTIPLIER, (byte)(2));
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} enabled double damage.");
                        }
                        return result;
                    });
                return;
            case "gravity_high":
                StartTimed(request,
                    () => true,
                    () =>
                    {
                        bool result = ChangeGravity(4.0f);
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} relocated DK Isles to Jupiter.");
                        }
                        return result;
                    });
                return;
            case "gravity_low":
                StartTimed(request,
                    () => true,
                    () =>
                    {
                        bool result = ChangeGravity(0.25f);
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} relocated DK Isles to the moon.");
                        }
                        return result;
                    });
                return;
            case "flip_screen":
                StartTimed(request,
                    () => true,
                    () =>
                    {
                        bool result = Connector.Write8(ADDR_BASE_ASPECT, (byte)(0xBF));
                        if (result)
                        {
                            Connector.SendMessage($"{request.DisplayViewer} flipped the screen.");
                        }
                        return result;
                    });
                return;
            default:
                Respond(request, EffectStatus.FailPermanent, StandardErrors.UnknownEffect, request);
                return;
        }
    }

    protected override bool StopEffect(EffectRequest request)
    {
        switch (request.EffectID)
        {
            //set some value back to normal for effects that need turning off
            //this is the preferred method! - it's always preferable to let CC
            //(and thus the streamer) be in control of an effect's duration
            //rather than relying on fixed timers
            case "drunky_kong":
                if (Connector.IsEqual8(DRUNK_STATE, (byte)CC_STATE.CC_ENABLED))
                {
                    return DRUNK_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                if (Connector.IsEqual8(DRUNK_STATE, (byte)CC_STATE.CC_ENABLING))
                {
                    return DRUNK_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                return true;
            case "disable_ta":
                if (Connector.IsEqual8(NO_TA_STATE, (byte)CC_STATE.CC_ENABLED))
                {
                    return NO_TA_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                if (Connector.IsEqual8(NO_TA_STATE, (byte)CC_STATE.CC_ENABLING))
                {
                    return NO_TA_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                return true;
            case "rockfall":
                if (Connector.IsEqual8(ROCKFALL_STATE, (byte)CC_STATE.CC_ENABLED))
                {
                    return ROCKFALL_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                if (Connector.IsEqual8(ROCKFALL_STATE, (byte)CC_STATE.CC_ENABLING))
                {
                    return ROCKFALL_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                return true;
            case "play_the_rap":
                if (Connector.IsEqual8(RAP_STATE, (byte)CC_STATE.CC_ENABLED))
                {
                    return RAP_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                if (Connector.IsEqual8(RAP_STATE, (byte)CC_STATE.CC_ENABLING))
                {
                    return RAP_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                return true;
            case "gravity_high":
                return ChangeGravity(1);
            case "gravity_low":
                return ChangeGravity(1);
            case "damage_ohko":
                return resetDamageMultiplier();
            case "damage_double":
                return resetDamageMultiplier();
            case "flip_screen":
                return resetScreen();
            case "tag_kong":
                if (Connector.IsEqual8(TAG_STATE, (byte)CC_STATE.CC_ENABLED))
                {
                    return TAG_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                if (Connector.IsEqual8(TAG_STATE, (byte)CC_STATE.CC_ENABLING))
                {
                    return TAG_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                return true;
            case "ice_floor":
                if (Connector.IsEqual8(ICEFLOOR_STATE, (byte)CC_STATE.CC_ENABLED))
                {
                    return ICEFLOOR_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                if (Connector.IsEqual8(ICEFLOOR_STATE, (byte)CC_STATE.CC_ENABLING))
                {
                    return ICEFLOOR_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                return true;
            case "force_mini":
                if (Connector.IsEqual8(MINI_STATE, (byte)CC_STATE.CC_ENABLED))
                {
                    return MINI_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                if (Connector.IsEqual8(MINI_STATE, (byte)CC_STATE.CC_ENABLING))
                {
                    return MINI_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                return true;
            case "animal_transform":
                if (Connector.IsEqual8(ANIMALTRANSFORM_STATE, (byte)CC_STATE.CC_ENABLED))
                {
                    return ANIMALTRANSFORM_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                if (Connector.IsEqual8(ANIMALTRANSFORM_STATE, (byte)CC_STATE.CC_ENABLING))
                {
                    return ANIMALTRANSFORM_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                return true;
            default:
                return base.StopEffect(request);
        }
    }

    public override bool StopAllEffects()
    {
        bool result = base.StopAllEffects();
        if (Connector.IsEqual8(DRUNK_STATE, (byte)CC_STATE.CC_ENABLED))
        {
            result &= DRUNK_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
        }
        if (Connector.IsEqual8(DRUNK_STATE, (byte)CC_STATE.CC_ENABLING))
        {
            result &= DRUNK_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
        }
        if (Connector.IsEqual8(NO_TA_STATE, (byte)CC_STATE.CC_ENABLED))
        {
            result &= NO_TA_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
        }
        if (Connector.IsEqual8(NO_TA_STATE, (byte)CC_STATE.CC_ENABLING))
        {
            result &= NO_TA_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
        }
        if (Connector.IsEqual8(ROCKFALL_STATE, (byte)CC_STATE.CC_ENABLED))
        {
            result &= ROCKFALL_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
        }
        if (Connector.IsEqual8(ROCKFALL_STATE, (byte)CC_STATE.CC_ENABLING))
        {
            result &= ROCKFALL_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
        }
        if (Connector.IsEqual8(RAP_STATE, (byte)CC_STATE.CC_ENABLED))
        {
            result &= RAP_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
        }
        if (Connector.IsEqual8(RAP_STATE, (byte)CC_STATE.CC_ENABLING))
        {
            result &= RAP_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
        }
        result &= ChangeGravity(1);
        result &= resetDamageMultiplier();
        result &= resetScreen();
        if (Connector.IsEqual8(TAG_STATE, (byte)CC_STATE.CC_ENABLED))
        {
            result &= TAG_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
        }
        if (Connector.IsEqual8(TAG_STATE, (byte)CC_STATE.CC_ENABLING))
        {
            result &= TAG_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
        }
        if (Connector.IsEqual8(ICEFLOOR_STATE, (byte)CC_STATE.CC_ENABLED))
        {
            result &= ICEFLOOR_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
        }
        if (Connector.IsEqual8(ICEFLOOR_STATE, (byte)CC_STATE.CC_ENABLING))
        {
            result &= ICEFLOOR_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
        }
        if (Connector.IsEqual8(MINI_STATE, (byte)CC_STATE.CC_ENABLED))
        {
            result &= MINI_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
        }
        if (Connector.IsEqual8(MINI_STATE, (byte)CC_STATE.CC_ENABLING))
        {
            result &= MINI_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
        }
        if (Connector.IsEqual8(ANIMALTRANSFORM_STATE, (byte)CC_STATE.CC_ENABLED))
        {
            result &= ANIMALTRANSFORM_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
        }
        if (Connector.IsEqual8(ANIMALTRANSFORM_STATE, (byte)CC_STATE.CC_ENABLING))
        {
            result &= ANIMALTRANSFORM_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
        }
        return result;
    }
}