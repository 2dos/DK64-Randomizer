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
        DRUNKY_STATE = AddressChain.Begin(Connector).Move(0x807FFFB4).Follow(4, Endianness.BigEndian, PointerType.Absolute);
        MAP_TIMER = AddressChain.Begin(Connector).Move(0x8076A064); // u32
        PLAYER_POINTER = AddressChain.Begin(Connector).Move(0x807FBB4C); // u32
        AUTOWALK_STATE = AddressChain.Begin(Connector).Move(0x807463B8); // u8
        CURRENT_GAMEMODE = AddressChain.Begin(Connector).Move(0x80755314); // u8
        NEXT_GAMEMODE = AddressChain.Begin(Connector).Move(0x80755318); // u8
    }

    private AddressChain DRUNKY_STATE;
    private AddressChain MAP_TIMER;
    private AddressChain PLAYER_POINTER;
    private AddressChain AUTOWALK_STATE;
    private AddressChain CURRENT_GAMEMODE;
    private AddressChain NEXT_GAMEMODE;
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
    };

    public override ROMTable ROMTable => new[]
    {
        new ROMInfo("Donkey Kong 64 Randomizer", "DonkeyKong64Randomizer.bps", Patching.BPS, ROMStatus.ValidUnpatched, s => Patching.MD5(s,"9ec41abf2519fc386cadd0731f6e868c"))
    };

    protected override GameState GetGameState()
    {
        if (!Connector.Connected) return GameState.Unknown;
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
                    () => Connector.IsEqual8(DRUNKY_STATE, (byte)CC_STATE.CC_READY),
                    () => DRUNKY_STATE.TrySetByte((byte)CC_STATE.CC_ENABLING));
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