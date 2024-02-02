using System.Net;
using System.IO;
using System;
using DK64BuildRoutine;

namespace DK64BuildRoutine {
    internal class Program {
        static void Main(string[] args) {
            // Delete New ROM File
            Globals.DeleteFile(Globals.newROMName);
            // Copy old ROM File to New ROM File
            Globals.CopyFile(Globals.ROMName, Globals.newROMName);
            // Create Bin Folder
            try {
                if (!Directory.Exists(Path.Combine(Globals.ROOT_FOLDER, Globals.BIN_FOLDER))) {
                    Directory.CreateDirectory(Path.Combine(Globals.ROOT_FOLDER, Globals.BIN_FOLDER));
                }
            } catch (Exception e) {
                Console.WriteLine("The process failed: {0}", e.ToString());
            }

            Models.loadNewModels();
        }
    }
}
