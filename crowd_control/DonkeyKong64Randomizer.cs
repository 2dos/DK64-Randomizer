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
    private const uint ADDR_HEALTH = 0x807FCC4B;
    private const uint ADDR_MELONS = 0x807FCC4C;
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
        // Inventory
        new("Give Coins","give_coins") { Price = 0, Description = "Gives each kong 2 coins.", Category="Inventory" },
        new("Remove Coins","remove_coins") { Price = 0, Description = "Takes 2 coins from each kong.", Category="Inventory" },
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