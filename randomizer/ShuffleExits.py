"""File that shuffles loading zone exits."""
import random

import randomizer.Fill as Fill
from randomizer.ItemPool import AllItems
from randomizer.Location import LocationList
import randomizer.Exceptions as Ex

from randomizer.Enums.Exits import Exits
from randomizer.Enums.ExitCategories import ExitCategories
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Levels import Levels


class ShufflableExit:
    """Class that stores data about an exit to be shuffled."""
    def __init__(self, region, reverse, category=None):
        self.region = region
        self.reverse = reverse
        self.category = category
        # Here dest is the entrance to go to, rather than just the target region
        self.dest = None
        self.shuffled = False
        self.ignore = False # used for spoiler so reverse entrances are not printed if not decoupled

ShufflableExits = {
    # Level Exits
    Exits.IslesToJapes: ShufflableExit(Regions.JungleJapesLobby, Exits.JapesToIsles, ExitCategories.IslesLevelExits),
    Exits.JapesToIsles: ShufflableExit(Regions.JungleJapesMain, Exits.IslesToJapes, ExitCategories.LevelExits),
    Exits.IslesToAztec: ShufflableExit(Regions.AngryAztecLobby, Exits.AztecToIsles, ExitCategories.IslesLevelExits),
    Exits.AztecToIsles: ShufflableExit(Regions.AngryAztecStart, Exits.IslesToAztec, ExitCategories.LevelExits),
    Exits.IslesToFactory: ShufflableExit(Regions.FranticFactoryLobby, Exits.FactoryToIsles, ExitCategories.IslesLevelExits),
    Exits.FactoryToIsles: ShufflableExit(Regions.FranticFactoryStart, Exits.IslesToFactory, ExitCategories.LevelExits),
    Exits.IslesToGalleon: ShufflableExit(Regions.GloomyGalleonLobby, Exits.GalleonToIsles, ExitCategories.IslesLevelExits),
    Exits.GalleonToIsles: ShufflableExit(Regions.GloomyGalleonStart, Exits.IslesToGalleon, ExitCategories.LevelExits),
    Exits.IslesToForest: ShufflableExit(Regions.FungiForestLobby, Exits.ForestToIsles, ExitCategories.IslesLevelExits),
    Exits.ForestToIsles: ShufflableExit(Regions.FungiForestStart, Exits.IslesToForest, ExitCategories.LevelExits),
    Exits.IslesToCaves: ShufflableExit(Regions.CrystalCavesLobby, Exits.CavesToIsles, ExitCategories.IslesLevelExits),
    Exits.CavesToIsles: ShufflableExit(Regions.CrystalCavesMain, Exits.IslesToCaves, ExitCategories.LevelExits),
    Exits.IslesToCastle: ShufflableExit(Regions.CreepyCastleLobby, Exits.CastleToIsles, ExitCategories.IslesLevelExits),
    Exits.CastleToIsles: ShufflableExit(Regions.CreepyCastleMain, Exits.IslesToCastle, ExitCategories.LevelExits),
    Exits.IslesToHelm: ShufflableExit(Regions.HideoutHelmLobby, Exits.HelmToIsles, ExitCategories.IslesLevelExits),
    Exits.HelmToIsles: ShufflableExit(Regions.HideoutHelmStart, Exits.IslesToHelm, ExitCategories.LevelExits),
    # DK Isles Exits
    Exits.IslesStartToMain: ShufflableExit(Regions.Start, Exits.IslesMainToStart),
    Exits.IslesMainToStart: ShufflableExit(Regions.IslesMain, Exits.IslesStartToMain, ExitCategories.IslesExterior),
    Exits.IslesMainToPrison: ShufflableExit(Regions.IslesMain, Exits.IslesPrisonToMain, ExitCategories.IslesExterior),
    Exits.IslesPrisonToMain: ShufflableExit(Regions.Prison, Exits.IslesMainToPrison),
    Exits.IslesMainToFairy: ShufflableExit(Regions.IslesMain, Exits.IslesFairyToMain, ExitCategories.IslesExterior),
    Exits.IslesFairyToMain: ShufflableExit(Regions.BananaFairyRoom, Exits.IslesMainToFairy),
    Exits.IslesMainToSnideRoom: ShufflableExit(Regions.CrocodileIsleBeyondLift, Exits.IslesSnideRoomToMain, ExitCategories.IslesExterior),
    Exits.IslesSnideRoomToMain: ShufflableExit(Regions.IslesSnideRoom, Exits.IslesMainToSnideRoom),
    Exits.IslesMainToJapesLobby: ShufflableExit(Regions.IslesMain, Exits.IslesJapesLobbyToMain, ExitCategories.IslesExterior),
    Exits.IslesJapesLobbyToMain: ShufflableExit(Regions.JungleJapesLobby, Exits.IslesMainToJapesLobby),
    Exits.IslesMainToAztecLobby: ShufflableExit(Regions.IslesMain, Exits.IslesAztecLobbyToMain, ExitCategories.IslesExterior),
    Exits.IslesAztecLobbyToMain: ShufflableExit(Regions.AngryAztecLobby, Exits.IslesMainToAztecLobby),
    Exits.IslesMainToFactoryLobby: ShufflableExit(Regions.CrocodileIsleBeyondLift, Exits.IslesFactoryLobbyToMain, ExitCategories.IslesExterior),
    Exits.IslesFactoryLobbyToMain: ShufflableExit(Regions.FranticFactoryLobby, Exits.IslesMainToFactoryLobby),
    Exits.IslesMainToGalleonLobby: ShufflableExit(Regions.IslesMain, Exits.IslesGalleonLobbyToMain, ExitCategories.IslesExterior),
    Exits.IslesGalleonLobbyToMain: ShufflableExit(Regions.GloomyGalleonLobby, Exits.IslesMainToGalleonLobby),
    Exits.IslesMainToForestLobby: ShufflableExit(Regions.CabinIsle, Exits.IslesForestLobbyToMain, ExitCategories.IslesExterior),
    Exits.IslesForestLobbyToMain: ShufflableExit(Regions.FungiForestLobby, Exits.IslesMainToForestLobby),
    Exits.IslesMainToCavesLobby: ShufflableExit(Regions.IslesMain, Exits.IslesCavesLobbyToMain, ExitCategories.IslesExterior),
    Exits.IslesCavesLobbyToMain: ShufflableExit(Regions.CrystalCavesLobby, Exits.IslesMainToCavesLobby),
    Exits.IslesMainToCastleLobby: ShufflableExit(Regions.IslesMain, Exits.IslesCastleLobbyToMain, ExitCategories.IslesExterior),
    Exits.IslesCastleLobbyToMain: ShufflableExit(Regions.CreepyCastleLobby, Exits.IslesMainToCastleLobby),
    Exits.IslesMainToHelmLobby: ShufflableExit(Regions.IslesMain, Exits.IslesHelmLobbyToMain, ExitCategories.IslesExterior),
    Exits.IslesHelmLobbyToMain: ShufflableExit(Regions.HideoutHelmLobby, Exits.IslesMainToHelmLobby),
    # Jungle Japes Exits
    Exits.JapesMainToMine: ShufflableExit(Regions.JungleJapesMain, Exits.JapesMineToMain, ExitCategories.JapesExterior),
    Exits.JapesMineToMain: ShufflableExit(Regions.Mine, Exits.JapesMainToMine, ExitCategories.JapesMine),
    Exits.JapesMainToLankyCave: ShufflableExit(Regions.IslesMain, Exits.JapesLankyCaveToMain, ExitCategories.JapesExterior),
    Exits.JapesLankyCaveToMain: ShufflableExit(Regions.JapesLankyCave, Exits.JapesMainToLankyCave),
    Exits.JapesMainToCatacomb: ShufflableExit(Regions.JungleJapesMain, Exits.JapesCatacombToMain, ExitCategories.JapesExterior),
    Exits.JapesCatacombToMain: ShufflableExit(Regions.JapesCatacomb, Exits.JapesMainToCatacomb),
    Exits.JapesMainToTinyHive: ShufflableExit(Regions.JapesBeyondFeatherGate, Exits.JapesTinyHiveToMain, ExitCategories.JapesExterior),
    Exits.JapesTinyHiveToMain: ShufflableExit(Regions.TinyHive, Exits.JapesMainToTinyHive),
    Exits.JapesMineToCarts: ShufflableExit(Regions.Mine, Exits.JapesCartsToMine, ExitCategories.JapesMine),
    Exits.JapesCartsToMine: ShufflableExit(Regions.JapesMinecarts, Exits.JapesMineToCarts),
    # Angry Aztec Exits
    Exits.AztecStartToTemple: ShufflableExit(Regions.AngryAztecStart, Exits.AztecTempleToStart, ExitCategories.AztecExterior),
    Exits.AztecTempleToStart: ShufflableExit(Regions.TempleStart, Exits.AztecStartToTemple),
    Exits.AztecMainToDonkey: ShufflableExit(Regions.AngryAztecMain, Exits.AztecDonkeyToMain, ExitCategories.AztecExterior),
    Exits.AztecDonkeyToMain: ShufflableExit(Regions.DonkeyTemple, Exits.AztecMainToDonkey),
    Exits.AztecMainToDiddy: ShufflableExit(Regions.AngryAztecMain, Exits.AztecDiddyToMain, ExitCategories.AztecExterior),
    Exits.AztecDiddyToMain: ShufflableExit(Regions.DiddyTemple, Exits.AztecMainToDiddy),
    Exits.AztecMainToLanky: ShufflableExit(Regions.AngryAztecMain, Exits.AztecLankyToMain, ExitCategories.AztecExterior),
    Exits.AztecLankyToMain: ShufflableExit(Regions.LankyTemple, Exits.AztecMainToLanky),
    Exits.AztecMainToTiny: ShufflableExit(Regions.AngryAztecMain, Exits.AztecTinyToMain, ExitCategories.AztecExterior),
    Exits.AztecTinyToMain: ShufflableExit(Regions.TinyTemple, Exits.AztecMainToTiny),
    Exits.AztecMainToChunky: ShufflableExit(Regions.AngryAztecMain, Exits.AztecChunkyToMain, ExitCategories.AztecExterior),
    Exits.AztecChunkyToMain: ShufflableExit(Regions.ChunkyTemple, Exits.AztecMainToChunky),
    Exits.AztecMainToRace: ShufflableExit(Regions.AngryAztecMain, Exits.AztecRaceToMain, ExitCategories.AztecExterior),
    Exits.AztecRaceToMain: ShufflableExit(Regions.AztecTinyRace, Exits.AztecMainToRace),
    Exits.AztecMainToLlama: ShufflableExit(Regions.AngryAztecMain, Exits.AztecLlamaToMain, ExitCategories.AztecExterior),
    Exits.AztecLlamaToMain: ShufflableExit(Regions.LlamaTemple, Exits.AztecMainToLlama),
    # Frantic Factory Exits
    Exits.FactoryRandDToRace: ShufflableExit(Regions.RandD, Exits.FactoryRaceToRandD, ExitCategories.FactoryExterior),
    Exits.FactoryRaceToRandD: ShufflableExit(Regions.FactoryTinyRace, Exits.FactoryRandDToRace),
    Exits.FactoryChunkyRoomToPower: ShufflableExit(Regions.ChunkyRoomPlatform, Exits.FactoryPowerToChunkyRoom, ExitCategories.FactoryExterior),
    Exits.FactoryPowerToChunkyRoom: ShufflableExit(Regions.PowerHut, Exits.FactoryChunkyRoomToPower),
    Exits.FactoryBeyondHatchToInsideCore: ShufflableExit(Regions.BeyondHatch, Exits.FactoryInsideCoreToBeyondHatch, ExitCategories.FactoryExterior),
    Exits.FactoryInsideCoreToBeyondHatch: ShufflableExit(Regions.InsideCore, Exits.FactoryBeyondHatchToInsideCore),
    # Gloomy Galleon Exits
    Exits.GalleonLighthouseAreaToLighthouse: ShufflableExit(Regions.LighthouseArea, Exits.GalleonLighthouseToLighthouseArea, ExitCategories.GalleonExterior),
    Exits.GalleonLighthouseToLighthouseArea: ShufflableExit(Regions.Lighthouse, Exits.GalleonLighthouseAreaToLighthouse),
    Exits.GalleonLighthousAreaToMermaid: ShufflableExit(Regions.LighthouseArea, Exits.GalleonMermaidToLighthouseArea, ExitCategories.GalleonExterior),
    Exits.GalleonMermaidToLighthouseArea: ShufflableExit(Regions.MermaidRoom, Exits.GalleonLighthousAreaToMermaid),
    Exits.GalleonLighthouseAreaToSickBay: ShufflableExit(Regions.LighthouseArea, Exits.GalleonSickBayToLighthouseArea, ExitCategories.GalleonExterior),
    Exits.GalleonSickBayToLighthouseArea: ShufflableExit(Regions.SickBay, Exits.GalleonLighthouseAreaToSickBay),
    Exits.GalleonShipyardToSeal: ShufflableExit(Regions.Shipyard, Exits.GalleonSealToShipyard, ExitCategories.GalleonExterior),
    Exits.GalleonSealToShipyard: ShufflableExit(Regions.SealRace, Exits.GalleonShipyardToSeal),
    Exits.GalleonShipyardToSubmarine: ShufflableExit(Regions.Shipyard, Exits.GalleonSubmarineToShipyard, ExitCategories.GalleonExterior),
    Exits.GalleonSubmarineToShipyard: ShufflableExit(Regions.Submarine, Exits.GalleonShipyardToSubmarine),
    Exits.GalleonShipyardToMechafish: ShufflableExit(Regions.Shipyard, Exits.GalleyonMechafishToShipyard, ExitCategories.GalleonExterior),
    Exits.GalleyonMechafishToShipyard: ShufflableExit(Regions.Mechafish, Exits.GalleonShipyardToMechafish),
    Exits.GalleonShipyardToLanky: ShufflableExit(Regions.Shipyard, Exits.GalleonLankyToShipyard, ExitCategories.GalleonExterior),
    Exits.GalleonLankyToShipyard: ShufflableExit(Regions.LankyShip, Exits.GalleonShipyardToLanky),
    Exits.GalleonShipyardToTiny: ShufflableExit(Regions.Shipyard, Exits.GalleonTinyToShipyard, ExitCategories.GalleonExterior),
    Exits.GalleonTinyToShipyard: ShufflableExit(Regions.TinyShip, Exits.GalleonShipyardToTiny),
    Exits.GalleonShipyardToBongos: ShufflableExit(Regions.Shipyard, Exits.GalleonBongosToShipyard, ExitCategories.GalleonExterior),
    Exits.GalleonBongosToShipyard: ShufflableExit(Regions.BongosShip, Exits.GalleonShipyardToBongos),
    Exits.GalleonShipyardToGuitar: ShufflableExit(Regions.Shipyard, Exits.GalleonGuitarToShipyard, ExitCategories.GalleonExterior),
    Exits.GalleonGuitarToShipyard: ShufflableExit(Regions.GuitarShip, Exits.GalleonShipyardToGuitar),
    Exits.GalleonShipyardToTrombone: ShufflableExit(Regions.Shipyard, Exits.GalleonTromboneToShipyard, ExitCategories.GalleonExterior),
    Exits.GalleonTromboneToShipyard: ShufflableExit(Regions.TromboneShip, Exits.GalleonShipyardToTrombone),
    Exits.GalleonShipyardToSaxophone: ShufflableExit(Regions.Shipyard, Exits.GalleonSaxophoneToShipyard, ExitCategories.GalleonExterior),
    Exits.GalleonSaxophoneToShipyard: ShufflableExit(Regions.SaxophoneShip, Exits.GalleonShipyardToSaxophone),
    Exits.GalleonShipyardToTriangle: ShufflableExit(Regions.Shipyard, Exits.GalleonTriangleToShipyard, ExitCategories.GalleonExterior),
    Exits.GalleonTriangleToShipyard: ShufflableExit(Regions.TriangleShip, Exits.GalleonShipyardToTriangle),
    Exits.GalleonTreasureToChest: ShufflableExit(Regions.TreasureRoom, Exits.GalleonChestToTreasure, ExitCategories.GalleonExterior),
    Exits.GalleonChestToTreasure: ShufflableExit(Regions.TinyChest, Exits.GalleonTreasureToChest),
    # Fungi Forest Exits
    Exits.ForestMainToCarts: ShufflableExit(Regions.FungiForestStart, Exits.ForestCartsToMain, ExitCategories.ForestExterior),
    Exits.ForestCartsToMain: ShufflableExit(Regions.ForestMinecarts, Exits.ForestMainToCarts),
    Exits.ForestMainToLowerMushroom: ShufflableExit(Regions.GiantMushroomArea, Exits.ForestLowerMushroomToMain, ExitCategories.ForestExterior),
    Exits.ForestLowerMushroomToMain: ShufflableExit(Regions.MushroomLower, Exits.ForestMainToLowerMushroom, ExitCategories.ForestMushroom),
    Exits.ForestLowerExteriorToLowerMushroom: ShufflableExit(Regions.MushroomLowerExterior, Exits.ForestLowerMushroomToLowerExterior, ExitCategories.ForestExterior),
    Exits.ForestLowerMushroomToLowerExterior: ShufflableExit(Regions.MushroomLower, Exits.ForestLowerExteriorToLowerMushroom, ExitCategories.ForestMushroom),
    Exits.ForestLowerExteriorToUpperMushroom: ShufflableExit(Regions.MushroomLowerExterior, Exits.ForestUpperMushroomToLowerExterior, ExitCategories.ForestExterior),
    Exits.ForestUpperMushroomToLowerExterior: ShufflableExit(Regions.MushroomUpper, Exits.ForestLowerExteriorToUpperMushroom, ExitCategories.ForestMushroom),
    Exits.ForestUpperExteriorToUpperMushroom: ShufflableExit(Regions.MushroomUpperExterior, Exits.ForestUpperMushroomToUpperExterior, ExitCategories.ForestExterior),
    Exits.ForestUpperMushroomToUpperExterior: ShufflableExit(Regions.MushroomUpper, Exits.ForestUpperExteriorToUpperMushroom, ExitCategories.ForestMushroom),
    Exits.ForestExteriorToNight: ShufflableExit(Regions.MushroomNightExterior, Exits.ForestNightToExterior, ExitCategories.ForestExterior),
    Exits.ForestNightToExterior: ShufflableExit(Regions.MushroomNightDoor, Exits.ForestExteriorToNight, ExitCategories.ForestMushroom),
    Exits.ForestExteriorToChunky: ShufflableExit(Regions.MushroomUpperExterior, Exits.ForestChunkyToExterior, ExitCategories.ForestExterior),
    Exits.ForestChunkyToExterior: ShufflableExit(Regions.MushroomChunkyRoom, Exits.ForestExteriorToChunky),
    Exits.ForestExteriorToZingers: ShufflableExit(Regions.MushroomUpperExterior, Exits.ForestZingersToExterior, ExitCategories.ForestExterior),
    Exits.ForestZingersToExterior: ShufflableExit(Regions.MushroomLankyZingersRoom, Exits.ForestExteriorToZingers),
    Exits.ForestExteriorToMushrooms: ShufflableExit(Regions.MushroomUpperExterior, Exits.ForestMushroomsToExterior, ExitCategories.ForestExterior),
    Exits.ForestMushroomsToExterior: ShufflableExit(Regions.MushroomLankyMushroomsRoom, Exits.ForestExteriorToMushrooms),
    Exits.ForestTreeToAnthill: ShufflableExit(Regions.HollowTreeArea, Exits.ForestAnthillToTree, ExitCategories.ForestExterior),
    Exits.ForestAnthillToTree: ShufflableExit(Regions.Anthill, Exits.ForestTreeToAnthill),
    Exits.ForestMainToChunkyMill: ShufflableExit(Regions.MillArea, Exits.ForestChunkyMillToMain, ExitCategories.ForestExterior),
    Exits.ForestChunkyMillToMain: ShufflableExit(Regions.MillChunkyArea, Exits.ForestMainToChunkyMill, ExitCategories.ForestMill),
    Exits.ForestMainToTinyMill: ShufflableExit(Regions.MillArea, Exits.ForestTinyMillToMain, ExitCategories.ForestExterior),
    Exits.ForestTinyMillToMain: ShufflableExit(Regions.MillTinyArea, Exits.ForestMainToTinyMill, ExitCategories.ForestMill),
    Exits.ForestMainToGrinder: ShufflableExit(Regions.MillArea, Exits.ForestGrinderToMain, ExitCategories.ForestExterior),
    Exits.ForestGrinderToMain: ShufflableExit(Regions.GrinderRoom, Exits.ForestMainToGrinder, ExitCategories.ForestGrinder),
    Exits.ForestMainToRafters: ShufflableExit(Regions.MillArea, Exits.ForestRaftersToMain, ExitCategories.ForestExterior),
    Exits.ForestRaftersToMain: ShufflableExit(Regions.MillRafters, Exits.ForestMainToRafters),
    Exits.ForestMainToWench: ShufflableExit(Regions.MillArea, Exits.ForestWenchToMain, ExitCategories.ForestExterior),
    Exits.ForestWenchToMain: ShufflableExit(Regions.WenchRoom, Exits.ForestMainToWench),
    Exits.ForestMainToAttic: ShufflableExit(Regions.MillArea, Exits.ForestAtticToMain, ExitCategories.ForestExterior),
    Exits.ForestAtticToMain: ShufflableExit(Regions.MillAttic, Exits.ForestMainToAttic),
    Exits.ForestTinyMillToSpider: ShufflableExit(Regions.MillTinyArea, Exits.ForestSpiderToTinyMill, ExitCategories.ForestMill),
    Exits.ForestSpiderToTinyMill: ShufflableExit(Regions.SpiderRoom, Exits.ForestTinyMillToSpider),
    Exits.ForestTinyMillToGrinder: ShufflableExit(Regions.MillTinyArea, Exits.ForestGrinderToTinyMill, ExitCategories.ForestMill),
    Exits.ForestGrinderToTinyMill: ShufflableExit(Regions.GrinderRoom, Exits.ForestTinyMillToGrinder, ExitCategories.ForestGrinder),
    Exits.ForestMainToBarn: ShufflableExit(Regions.ThornvineArea, Exits.ForestBarnToMain, ExitCategories.ForestExterior),
    Exits.ForestBarnToMain: ShufflableExit(Regions.ThornvineBarn, Exits.ForestMainToBarn),
    # Crystal Caves Exits
    Exits.CavesMainToRace: ShufflableExit(Regions.CrystalCavesMain, Exits.CavesRaceToMain, ExitCategories.CavesExterior),
    Exits.CavesRaceToMain: ShufflableExit(Regions.CavesLankyRace, Exits.CavesMainToRace),
    Exits.CavesMainToCastle: ShufflableExit(Regions.CrystalCavesMain, Exits.CavesCastleToMain, ExitCategories.CavesExterior),
    Exits.CavesCastleToMain: ShufflableExit(Regions.FrozenCastle, Exits.CavesMainToCastle),
    Exits.CavesIglooToDonkey: ShufflableExit(Regions.IglooArea, Exits.CavesDonkeyToIgloo, ExitCategories.CavesExterior),
    Exits.CavesDonkeyToIgloo: ShufflableExit(Regions.DonkeyIgloo, Exits.CavesIglooToDonkey),
    Exits.CavesIglooToDiddy: ShufflableExit(Regions.IglooArea, Exits.CavesDiddyToIgloo, ExitCategories.CavesExterior),
    Exits.CavesDiddyToIgloo: ShufflableExit(Regions.DiddyIgloo, Exits.CavesIglooToDiddy),
    Exits.CavesIglooToLanky: ShufflableExit(Regions.IglooArea, Exits.CavesLankyToIgloo, ExitCategories.CavesExterior),
    Exits.CavesLankyToIgloo: ShufflableExit(Regions.LankyIgloo, Exits.CavesIglooToLanky),
    Exits.CavesIglooToTiny: ShufflableExit(Regions.IglooArea, Exits.CavesTinyToIgloo, ExitCategories.CavesExterior),
    Exits.CavesTinyToIgloo: ShufflableExit(Regions.TinyIgloo, Exits.CavesIglooToTiny),
    Exits.CavesIglooToChunky: ShufflableExit(Regions.IglooArea, Exits.CavesChunkyToIgloo, ExitCategories.CavesExterior),
    Exits.CavesChunkyToIgloo: ShufflableExit(Regions.ChunkyIgloo, Exits.CavesIglooToChunky),
    Exits.CavesCabinToRotating: ShufflableExit(Regions.CabinArea, Exits.CavesRotatingToCabin, ExitCategories.CavesExterior),
    Exits.CavesRotatingToCabin: ShufflableExit(Regions.RotatingCabin, Exits.CavesCabinToRotating),
    Exits.CavesCabinToDonkey: ShufflableExit(Regions.CabinArea, Exits.CavesDonkeyToCabin, ExitCategories.CavesExterior),
    Exits.CavesDonkeyToCabin: ShufflableExit(Regions.DonkeyCabin, Exits.CavesCabinToDonkey),
    Exits.CavesCabinToDiddyLower: ShufflableExit(Regions.CabinArea, Exits.CavesDiddyLowerToCabin, ExitCategories.CavesExterior),
    Exits.CavesDiddyLowerToCabin: ShufflableExit(Regions.DiddyLowerCabin, Exits.CavesCabinToDiddyLower),
    Exits.CavesCabinToDiddyUpper: ShufflableExit(Regions.CabinArea, Exits.CavesDiddyUpperToCabin, ExitCategories.CavesExterior),
    Exits.CavesDiddyUpperToCabin: ShufflableExit(Regions.DiddyUpperCabin, Exits.CavesCabinToDiddyUpper),
    Exits.CavesCabinToLanky: ShufflableExit(Regions.CabinArea, Exits.CavesLankyToCabin, ExitCategories.CavesExterior),
    Exits.CavesLankyToCabin: ShufflableExit(Regions.LankyCabin, Exits.CavesCabinToLanky),
    Exits.CavesCabinToTiny: ShufflableExit(Regions.CabinArea, Exits.CavesTinyToCabin, ExitCategories.CavesExterior),
    Exits.CavesTinyToCabin: ShufflableExit(Regions.TinyCabin, Exits.CavesCabinToTiny),
    Exits.CavesCabinToChunky: ShufflableExit(Regions.CabinArea, Exits.CavesChunkyToCabin, ExitCategories.CavesExterior),
    Exits.CavesChunkyToCabin: ShufflableExit(Regions.ChunkyCabin, Exits.CavesCabinToChunky),
    # Creepy Castle Exits
    Exits.CastleMainToTree: ShufflableExit(Regions.CreepyCastleMain, Exits.CastleTreeToMain, ExitCategories.CastleExterior),
    Exits.CastleTreeToMain: ShufflableExit(Regions.CastleTree, Exits.CastleMainToTree),
    Exits.CastleMainToLibrary: ShufflableExit(Regions.CreepyCastleMain, Exits.CastleLibraryToMain, ExitCategories.CastleExterior),
    Exits.CastleLibraryToMain: ShufflableExit(Regions.Library, Exits.CastleMainToLibrary),
    Exits.CastleMainToBallroom: ShufflableExit(Regions.CreepyCastleMain, Exits.CastleBallroomToMain, ExitCategories.CastleExterior),
    Exits.CastleBallroomToMain: ShufflableExit(Regions.Ballroom, Exits.CastleMainToBallroom, ExitCategories.CastleBallroom),
    Exits.CastleMainToTower: ShufflableExit(Regions.CreepyCastleMain, Exits.CastleTowerToMain, ExitCategories.CastleExterior),
    Exits.CastleTowerToMain: ShufflableExit(Regions.Tower, Exits.CastleMainToTower),
    Exits.CastleMainToGreenhouse: ShufflableExit(Regions.CreepyCastleMain, Exits.CastleGreenhouseToMain, ExitCategories.CastleExterior),
    Exits.CastleGreenhouseToMain: ShufflableExit(Regions.Greenhouse, Exits.CastleMainToGreenhouse),
    Exits.CastleMainToTrash: ShufflableExit(Regions.CreepyCastleMain, Exits.CastleTrashToMain, ExitCategories.CastleExterior),
    Exits.CastleTrashToMain: ShufflableExit(Regions.TrashCan, Exits.CastleMainToTrash),
    Exits.CastleMainToShed: ShufflableExit(Regions.CreepyCastleMain, Exits.CastleShedToMain, ExitCategories.CastleExterior),
    Exits.CastleShedToMain: ShufflableExit(Regions.Shed, Exits.CastleMainToShed),
    Exits.CastleMainToMuseum: ShufflableExit(Regions.CreepyCastleMain, Exits.CastleMuseumToMain, ExitCategories.CastleExterior),
    Exits.CastleMuseumToMain: ShufflableExit(Regions.Museum, Exits.CastleMainToMuseum),
    Exits.CastleMainToLower: ShufflableExit(Regions.CreepyCastleMain, Exits.CastleLowerToMain, ExitCategories.CastleExterior),
    Exits.CastleLowerToMain: ShufflableExit(Regions.LowerCave, Exits.CastleMainToLower, ExitCategories.CastleLower),
    Exits.CastleMainToUpper: ShufflableExit(Regions.CreepyCastleMain, Exits.CastleUpperToMain, ExitCategories.CastleExterior),
    Exits.CastleUpperToMain: ShufflableExit(Regions.UpperCave, Exits.CastleMainToUpper, ExitCategories.CastleUpper),
    Exits.CastleWaterfallToUpper: ShufflableExit(Regions.CastleWaterfall, Exits.CastleUpperToWaterfall, ExitCategories.CastleExterior),
    Exits.CastleUpperToWaterfall: ShufflableExit(Regions.UpperCave, Exits.CastleWaterfallToUpper, ExitCategories.CastleUpper),
    Exits.CastleBallroomToRace: ShufflableExit(Regions.Ballroom, Exits.CastleRaceToBallroom, ExitCategories.CastleBallroom),
    Exits.CastleRaceToBallroom: ShufflableExit(Regions.CastleTinyRace, Exits.CastleBallroomToRace),
    Exits.CastleLowerToCrypt: ShufflableExit(Regions.LowerCave, Exits.CastleCryptToLower, ExitCategories.CastleLower),
    Exits.CastleCryptToLower: ShufflableExit(Regions.Crypt, Exits.CastleLowerToCrypt, ExitCategories.CastleCrypt),
    Exits.CastleLowerToMauseoleum: ShufflableExit(Regions.LowerCave, Exits.CastleMausoleumToLower, ExitCategories.CastleLower),
    Exits.CastleMausoleumToLower: ShufflableExit(Regions.Mausoleum, Exits.CastleLowerToMauseoleum),
    Exits.CastleCryptToCarts: ShufflableExit(Regions.Crypt, Exits.CastleCartsToCrypt, ExitCategories.CastleCrypt),
    Exits.CastleCartsToCrypt: ShufflableExit(Regions.CastleMinecarts, Exits.CastleCryptToCarts),
    Exits.CastleUpperToDungeon: ShufflableExit(Regions.UpperCave, Exits.CastleDungeonToUpper, ExitCategories.CastleUpper),
    Exits.CastleDungeonToUpper: ShufflableExit(Regions.Dungeon, Exits.CastleUpperToDungeon),
}

LevelExitPool = [
    Exits.IslesToJapes,
    Exits.JapesToIsles,
    Exits.IslesToAztec,
    Exits.AztecToIsles,
    Exits.IslesToFactory,
    Exits.FactoryToIsles,
    Exits.IslesToGalleon,
    Exits.GalleonToIsles,
    Exits.IslesToForest,
    Exits.ForestToIsles,
    Exits.IslesToCaves,
    Exits.CavesToIsles,
    Exits.IslesToCastle,
    Exits.CastleToIsles,
    Exits.IslesToHelm,
    Exits.HelmToIsles,
]

def Reset():
    for exit in ShufflableExits.values():
        exit.dest = None
        exit.shuffled = False

def ShuffleExitsInPool(exitpool):
    while len(exitpool) > 0:
        random.shuffle(exitpool)
        targetId = exitpool.pop()
        target = ShufflableExits[targetId]
        destinations = exitpool.copy()
        # If our target exit to shuffle has a category, unsure it's not shuffled to entrances with the same category
        if target.category is not None:
            destinations = [x for x in destinations if ShufflableExits[x].category is None or ShufflableExits[x].category != target.category]
        random.shuffle(destinations)
        # Select the destination
        destId = destinations.pop()
        target.dest = destId
        target.shuffled = True
        # if not decoupled
        dest = ShufflableExits[destId]
        dest.dest = targetId
        dest.shuffled = True
        exitpool.remove(destId)


def ShuffleExits(settings):
    if settings.ShuffleLevels:
        ShuffleExitsInPool(LevelExitPool)

def ExitShuffle(settings):
    retries = 0
    while True:
        try:
            # Shuffle entrances based on settings
            ShuffleExits(settings)
            # Verify world by assuring all locations are still reachable
            accessible = Fill.GetAccessibleLocations(AllItems(settings))
            if len(accessible) < len(LocationList):
                raise Ex.EntrancePlacementException
            return
        except Ex.EntrancePlacementException:
            if retries == 14:
                raise Ex.EntranceAttemptCountExceeded
            else:
                retries += 1
                print("Entrance placement failed. Retrying. Tries: " + str(retries))
                Reset()


