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
    }

    private AddressChain DRUNK_STATE;
    private AddressChain NO_TA_STATE;
    private AddressChain ICE_STATE;
    private AddressChain ROCKFALL_STATE;

    private const uint ADDR_STATE_POINTER = 0x807FFFB4;
    private const uint ADDR_MAP_TIMER = 0x8076A064;
    private const uint ADDR_PLAYER_POINTER = 0x807FBB4C;
    private const uint ADDR_AUTOWALK_STATE = 0x807463B8;
    private const uint ADDR_CURRENT_GAMEMODE = 0x80755314;
    private const uint ADDR_NEXT_GAMEMODE = 0x80755318;
    private const uint ADDR_TBVOID_BYTE = 0x807FBB63;
    private const uint ADDR_KONG_BASE = 0x807FC950;
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
        new("Drunk Kong","drunky_kong") { Price = 0, Duration = 30, Description = "Makes the kong feel a little woozy. Reverses controls and slows down the player.", Category="Player" },
        new("Disable Tag Anywhere","disable_ta") { Price = 0, Duration = 30, Description = "Disables the ability for the player to use Tag Anywhere.", Category="Player" },
        new("Ice Trap the Player","ice_trap") { Price = 0, Description = "Locks the player in an ice trap bubble in which they have to escape.", Category="Player" },
        new("Spawn Rocks","rockfall") { Price = 0, Duration = 30, Description = "Spawn a bunch of stalactites above the player throughout the duration of the effect.", Category="Player" },
        new("Give Coins","give_coins") { Price = 0, Description = "Gives each kong 2 coins.", Category="Player" },
        new("Remove Coins","remove_coins") { Price = 0, Description = "Takes 2 coins from each kong.", Category="Player" },
        new("Give a Golden Banana","give_gb") { Price = 0, Description = "Gives the player a Golden Banana. OHHHHHHHH BANANA.", Category="Player" },
        new("Remove a Golden Banana","remove_gb") { Price = 0, Description = "Removes a Golden Banana from the player.", Category="Player" },
    };

    public override ROMTable ROMTable => new[]
    {
        new ROMInfo("Donkey Kong 64 Randomizer", "DonkeyKong64Randomizer.bps", Patching.BPS, ROMStatus.ValidUnpatched, s => Patching.MD5(s,"9ec41abf2519fc386cadd0731f6e868c"))
    };

    protected override GameState GetGameState()
    {
        if (!Connector.Connected) return GameState.Unknown;

        // if (!Connector.Read8(ADDR_CURRENT_GAMEMODE, out byte current_gamemode)) return GameState.Unknown;
        // if (!Connector.Read8(ADDR_NEXT_GAMEMODE, out byte next_gamemode)) return GameState.Unknown;
        // if (!Connector.Read32(ADDR_MAP_TIMER, out uint map_timer)) return GameState.Unknown;
        // if (!Connector.Read32(ADDR_PLAYER_POINTER, out uint player_pointer)) return GameState.Unknown;
        // if (!Connector.Read32(ADDR_TBVOID_BYTE, out uint tb_void_byte)) return GameState.Unknown;
        // if ((current_gamemode != 6) || (next_gamemode != 6)) {
        //     // Not in adventure mode
        //     return GameState.WrongMode;
        // }
        // if (map_timer < 2) {
        //     // Loading
        //     return GameState.BadPlayerState;
        // }
        // if (player_pointer != 0) {
        //     // No player, also loading
        //     return GameState.BadPlayerState;
        // }
        // if (Connector.IsNonZero8(ADDR_AUTOWALK_STATE)) {
        //     // Player is autowalking
        //     return GameState.BadPlayerState;
        // }
        // if ((tb_void_byte & 3) != 0) {
        //     // Player is pausing or is paused
        //     return GameState.Paused;
        // }
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
                //set some value back to normal for effects that need turning off
                //this is the preferred method! - it's always preferable to let CC
                //(and thus the streamer) be in control of an effect's duration
                //rather than relying on fixed timers

                //return ADDR_CC_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING))
                return true;
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