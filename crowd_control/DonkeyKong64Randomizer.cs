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
    }

    private AddressChain DRUNK_STATE;
    private AddressChain NO_TA_STATE;
    private AddressChain ICE_STATE;
    private AddressChain ROCKFALL_STATE;
    private AddressChain RAP_STATE;
    private AddressChain KOP_STATE;
    private AddressChain BALLOON_STATE;

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
        new("Drunk Kong","drunky_kong") { Price = 0, Duration = 5, Description = "Makes the kong feel a little woozy. Reverses controls and slows down the player.", Category="Player" },
        new("Disable Tag Anywhere","disable_ta") { Price = 0, Duration = 5, Description = "Disables the ability for the player to use Tag Anywhere.", Category="Player" },
        new("Ice Trap the Player","ice_trap") { Price = 0, Description = "Locks the player in an ice trap bubble in which they have to escape.", Category="Player" },
        new("Spawn Rocks","rockfall") { Price = 0, Duration = 5, Description = "Spawn a bunch of stalactites above the player throughout the duration of the effect.", Category="Player" },
        new("Instant Balloon","balloon") { Price = 0, Description = "Inflate the balloon (kong) just like a balloon.", Category="Player" },
        new("High Gravity","gravity_high") { Price = 0, Duration = 5, Description = "Crank(y) that gravity up to 11.", Category="Player" },
        new("Low Gravity","gravity_low") { Price = 0, Duration = 5, Description = "Make the moonkick not so special anymore.", Category="Player" },
        // Inventory
        new("Give Coins","give_coins") { Price = 0, Description = "Gives each kong 2 coins.", Category="Inventory" },
        new("Remove Coins","remove_coins") { Price = 0, Description = "Takes 2 coins from each kong.", Category="Inventory" },
        new("Give Replenishibles","give_replenishibles") { Price = 0, Description = "Help the player out by giving them some ammo, crystals amongst other things.", Category="Inventory" },
        new("Remove all Replenishibles","remove_replenishibles") { Price = 0, Description = "Remove everything the player has in terms of ammo, crystals and other things.", Category="Inventory" },
        new("Give a Golden Banana","give_gb") { Price = 0, Description = "Gives the player a Golden Banana. OHHHHHHHH BANANA.", Category="Inventory" },
        new("Remove a Golden Banana","remove_gb") { Price = 0, Description = "Removes a Golden Banana from the player.", Category="Inventory" },
        // Health
        new("Refill Health","refill_health") { Price = 0, Description = "Refills the player's health to max.", Category="Health" },
        new("One Hit KO","damage_ohko") { Price = 0, Description = "From now onwards, the player will be killed for any damage taken.", Category="Health" },
        new("Double Damage","damage_double") { Price = 0, Description = "From now onwards, the player will take double damage.", Category="Health" },
        new("Single Damage","damage_single") { Price = 0, Description = "From now onwards, the player will take the normal amount of damage.", Category="Health" },
        // Misc
        new("Get Kaught","spawn_kop") { Price = 0, Description = "Spawn the greatest kop on the service to catch the player in their tracks.", Category="Misc" },
        new("Warp to the DK Rap","play_the_rap") { Price = 0, Duration = 190, Description = "Warps the player to the DK Rap, and warps them back after the rap is finished or the effect is cancelled (whichever comes first). Effect is capped at 190 seconds.", Category="Misc" },
    };

    public override ROMTable ROMTable => new[]
    {
        new ROMInfo("Donkey Kong 64 Randomizer", "DonkeyKong64Randomizer.bps", Patching.BPS, ROMStatus.ValidUnpatched, s => Patching.MD5(s,"9ec41abf2519fc386cadd0731f6e868c"))
    };

    protected override GameState GetGameState()
    {
        if (!Connector.Connected) return GameState.Unknown;

        if (!Connector.Read8(ADDR_CURRENT_GAMEMODE, out byte current_gamemode)) return GameState.Unknown;
        if (!Connector.Read8(ADDR_NEXT_GAMEMODE, out byte next_gamemode)) return GameState.Unknown;
        if (!Connector.Read32(ADDR_MAP_TIMER, out uint map_timer)) return GameState.Unknown;
        if (!Connector.Read32(ADDR_PLAYER_POINTER, out uint player_pointer)) return GameState.Unknown;
        if (!Connector.Read32(ADDR_TBVOID_BYTE, out uint tb_void_byte)) return GameState.Unknown;
        if (!Connector.Read8(ADDR_RANDO_CANARY, out byte rando_version)) return GameState.Unknown;
        if (!Connector.Read8(ADDR_CUTSCENE_ACTIVE, out byte cutscene_state)) return GameState.Unknown;
        if (!Connector.ReadFloat(ADDR_TRANSITION_SPEED, out float transition_speed)) return GameState.Unknown;
        if (rando_version != 4) {
            // Not randomizer or a currently supported version
            return GameState.Unknown;
        }
        if ((current_gamemode != 6) || (next_gamemode != 6)) {
            // Not in adventure mode
            return GameState.WrongMode;
        }
        if (map_timer < 2) {
            // Loading
            return GameState.BadPlayerState;
        }
        if (player_pointer == 0) {
            // No player, also loading
            return GameState.BadPlayerState;
        }
        if (Connector.IsNonZero8(ADDR_AUTOWALK_STATE)) {
            // Player is autowalking
            return GameState.BadPlayerState;
        }
        if ((tb_void_byte & 3) != 0) {
            // Player is pausing or is paused
            return GameState.Paused;
        }
        if ((cutscene_state == 2) || (cutscene_state == 3)) {
            // In Arcade/Jetpac
            return GameState.SafeArea;
        }
        if (cutscene_state != 0) {
            // Cutscene is playing
            return GameState.Paused;
        }
        if (transition_speed > 0.0f) {
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
        if (value < lower_bound) {
            value = lower_bound;
        } else if (value > upper_bound) {
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

    private bool ChangeGravity(float scale)
    {
        if (scale == 0) return false;
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
        for (byte i = 0; i < 7; i++) {
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
        result &= WriteDouble(0x8075CEA8, 0.036 * scale);
        result &= WriteFloat(0x8075CEB0, (float)(-0.001 * scale));
        result &= WriteFloat(0x8075EB4C, (float)(-2.5 * scale)); // Aerial attack, specially patching this for a moonkick (everyone is gonna do this, so need to plan for this)
        // 806DA13C - hardcoded -1
        // 806DA28C - hardcoded -1
        result &= WriteDouble(0x8075D308, 0.2 * scale); // balloon

        // Reset player yaccel
        AddressChain ADDR_YACCEL = AddressChain.Begin(Connector).Move(ADDR_PLAYER_POINTER).Follow(4, Endianness.BigEndian, PointerType.Absolute).Move(0xC4);
        result &= WriteFloat((uint)(ADDR_YACCEL.Address), -20 * scale);
        return result;
    }

    protected override void StartEffect(EffectRequest request)
    {
        switch (request.EffectID)
        {
            case "drunky_kong":
                TryEffect(request,
                    () => Connector.IsEqual8(DRUNK_STATE, (byte)CC_STATE.CC_READY),
                    () => DRUNK_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING));
                return;
            case "disable_ta":
                TryEffect(request,
                    () => Connector.IsEqual8(NO_TA_STATE, (byte)CC_STATE.CC_READY),
                    () => NO_TA_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING));
                return;
            case "ice_trap":
                TryEffect(request,
                    () => {
                        Connector.SendMessage($"State Address: {ICE_STATE}.");
                        return Connector.IsEqual8(ICE_STATE, (byte)CC_STATE.CC_READY);
                    },
                    () => ICE_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING));
                return;
            case "rockfall":
                TryEffect(request,
                    () => Connector.IsEqual8(ROCKFALL_STATE, (byte)CC_STATE.CC_READY),
                    () => ROCKFALL_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING));
                return;
            case "play_the_rap":
                TryEffect(request,
                    () => Connector.IsEqual8(RAP_STATE, (byte)CC_STATE.CC_READY),
                    () => RAP_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING));
                return;
            case "spawn_kop":
                TryEffect(request,
                    () => Connector.IsEqual8(KOP_STATE, (byte)CC_STATE.CC_READY),
                    () => KOP_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING));
                return;
            case "balloon":
                TryEffect(request,
                    () => Connector.IsEqual8(BALLOON_STATE, (byte)CC_STATE.CC_READY),
                    () => BALLOON_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING));
                return;
            case "give_coins":
                TryEffect(request,
                    () => {
                        for (byte kong = 0; kong < 5; kong++) {
                            if (!Connector.Read8((uint)(ADDR_KONG_BASE + (kong * 0x5E) + 7), out byte coin_count)) return false;
                            if (coin_count < 255) {
                                return true;
                            }
                        }
                        return false;
                    },
                    () => {
                        bool result = true;
                        for (byte kong = 0; kong < 5; kong++) {
                            uint coin_addr = (uint)(ADDR_KONG_BASE + (kong * 0x5E) + 7);
                            result &= Connector.Read8(coin_addr, out byte coin_count);
                            if (coin_count < (255 - COIN_CHANGE_AMOUNT)) {
                                result &= Connector.Write8(coin_addr, (byte)(coin_count + COIN_CHANGE_AMOUNT));
                            } else {
                                result &= Connector.Write8(coin_addr, 255);
                            }
                        }
                        return result;
                    });
                return;
            case "remove_coins":
                TryEffect(request,
                    () => {
                        for (byte kong = 0; kong < 5; kong++) {
                            if (!Connector.Read8((uint)(ADDR_KONG_BASE + (kong * 0x5E) + 7), out byte coin_count)) return false;
                            if (coin_count > 0) {
                                return true;
                            }
                        }
                        return false;
                    },
                    () => {
                        bool result = true;
                        for (byte kong = 0; kong < 5; kong++) {
                            uint coin_addr = (uint)(ADDR_KONG_BASE + (kong * 0x5E) + 7);
                            result &= Connector.Read8(coin_addr, out byte coin_count);
                            if (coin_count > COIN_CHANGE_AMOUNT) {
                                result &= Connector.Write8(coin_addr, (byte)(coin_count - COIN_CHANGE_AMOUNT));
                            } else {
                                result &= Connector.Write8(coin_addr, 0);
                            }
                        }
                        return result;
                    });
                return;
            case "give_replenishibles":
                TryEffect(request,
                    () => true,
                    () => {
                        bool result = true;
                        result &= Add16(ADDR_STANDARD_AMMO, 5, 0, 200);
                        result &= Add16(ADDR_HOMING_AMMO, 5, 0, 200);
                        result &= Add16(ADDR_ORANGES, 1, 0, 30);
                        result &= Add16(ADDR_CRYSTALS, 150, 0, 3000);
                        result &= Add16(ADDR_FILM, 1, 0, 20);
                        result &= Add16(ADDR_GLOBAL_INSTRUMENT, 1, 0, 20);
                        for (byte kong = 0; kong < 5; kong++) {
                            result &= Add16((uint)(ADDR_KONG_BASE + (kong * 0x5E) + 8), 1, 0, 20);
                        }
                        return result;
                    });
                return;
            case "remove_replenishibles":
                TryEffect(request,
                    () => true,
                    () => {
                        bool result = true;
                        result &= Write16(ADDR_STANDARD_AMMO, 0);
                        result &= Write16(ADDR_HOMING_AMMO, 0);
                        result &= Write16(ADDR_ORANGES, 0);
                        result &= Write16(ADDR_CRYSTALS, 0);
                        result &= Write16(ADDR_FILM, 0);
                        result &= Write16(ADDR_GLOBAL_INSTRUMENT, 0);
                        for (byte kong = 0; kong < 5; kong++) {
                            result &= Write16((uint)(ADDR_KONG_BASE + (kong * 0x5E) + 8), 0);
                        }
                        return result;
                    });
                return;
            case "give_gb":
                TryEffect(request,
                    () => true,
                    () => {
                        byte min_kong = 0;
                        byte min_level = 0;
                        ushort min_gb = 65535;
                        bool result = true;
                        for (byte kong = 0; kong < 5; kong++) {
                            for (byte level = 0; level < 8; level++) {
                                result &= Connector.Read8((uint)(ADDR_KONG_BASE + (kong * 0x5E) + 0x43 + (2 * level)), out byte gb_count);
                                if (gb_count < min_gb) {
                                    min_gb = gb_count;
                                    min_kong = kong;
                                    min_level = level;
                                }
                            }
                        }
                        uint gb_add_address = (uint)(ADDR_KONG_BASE + (min_kong * 0x5E) + 0x43 + (2 * min_level));
                        result &= Connector.Write8(gb_add_address, (byte)(min_gb + 1));
                        return result;
                    });
                return;
            case "remove_gb":
                TryEffect(request,
                    () => {
                        for (byte kong = 0; kong < 5; kong++) {
                            for (byte level = 0; level < 8; level++) {
                                uint gb_add_address = (uint)(ADDR_KONG_BASE + (kong * 0x5E) + 0x43 + (2 * level));
                                if (!Connector.Read8(gb_add_address, out byte gb_count)) return false;
                                if (gb_count > 0) {
                                    return true;
                                }
                            }
                        }
                        return false;
                    },
                    () => {
                        bool result = true;
                        for (byte kong = 0; kong < 5; kong++) {
                            for (byte level = 0; level < 8; level++) {
                                uint gb_add_address = (uint)(ADDR_KONG_BASE + (kong * 0x5E) + 0x43 + (2 * level));
                                result &= Connector.Read8(gb_add_address, out byte gb_count);
                                if (gb_count > 0) {
                                    result &= Connector.Write8(gb_add_address, (byte)(gb_count - 1));
                                    return result;
                                }
                            }
                        }
                        return result;
                    });
                return;
            case "refill_health":
                TryEffect(request,
                    () => true,
                    () => {
                        bool result = true;
                        result &= Connector.Read8(ADDR_MELONS, out byte melon_count);
                        result &= Connector.Write8(ADDR_HEALTH, (byte)(melon_count * 4));
                        return result;
                    });
                return;
            case "damage_ohko":
                TryEffect(request,
                    () => true,
                    () => Connector.Write8(ADDR_APPLIED_DAMAGE_MULTIPLIER, (byte)(12)));
                return;
            case "damage_double":
                TryEffect(request,
                    () => true,
                    () => Connector.Write8(ADDR_APPLIED_DAMAGE_MULTIPLIER, (byte)(2)));
                return;
            case "damage_single":
                TryEffect(request,
                    () => true,
                    () => Connector.Write8(ADDR_APPLIED_DAMAGE_MULTIPLIER, (byte)(1)));
                return;
            case "gravity_high":
                TryEffect(request,
                    () => true,
                    () => ChangeGravity(4.0f));
                return;
            case "gravity_low":
                TryEffect(request,
                    () => true,
                    () => ChangeGravity(0.25f));
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
            case "drunky_kong":
                if (Connector.IsEqual8(DRUNK_STATE, (byte)CC_STATE.CC_ENABLED)) {
                    return DRUNK_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                return true;
            case "disable_ta":
                if (Connector.IsEqual8(NO_TA_STATE, (byte)CC_STATE.CC_ENABLED)) {
                    return NO_TA_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                return true;
            case "rockfall":
                if (Connector.IsEqual8(ROCKFALL_STATE, (byte)CC_STATE.CC_ENABLED)) {
                    return ROCKFALL_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                return true;
            case "play_the_rap":
                if (Connector.IsEqual8(RAP_STATE, (byte)CC_STATE.CC_ENABLED)) {
                    return RAP_STATE.TrySetByte((byte)CC_STATE.CC_DISABLING);
                }
                return true;
            case "gravity_high":
                return ChangeGravity(1);
            case "gravity_low":
                return ChangeGravity(1);

                //set some value back to normal for effects that need turning off
                //this is the preferred method! - it's always preferable to let CC
                //(and thus the streamer) be in control of an effect's duration
                //rather than relying on fixed timers

                //return ADDR_CC_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING))
            default:
                return base.StopEffect(request);
        }
    }

    public override bool StopAllEffects()
    {
        bool result = base.StopAllEffects();
        //something here
        return result;
    }
}