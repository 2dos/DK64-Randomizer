using System.Security.Cryptography.X509Certificates;

namespace DK64BuildRoutine {
    internal class Songs {
        public class SongMemory {
            public static ushort value;
            public SongMemory(
                int channel = 0, 
                int bank = 0,
                int v = 0, 
                bool loop = false,
                bool p = false,
                bool d = false,
                bool a = false,
                bool is_sfx = false,
                bool is_music = false
            ) {
                /*
                    0VV0 MXPL ACCC CBBD
                    C = Channel
                    P = ?
                    L = Loop
                    B = Bank
                    D = ?
                    V = SFX Volume related. Each bit is some property that seems mutually exclusive
                    A = ?
                    X = Is sound effect, use SFX Volume
                    M = Is sound effect and music (?) - Use the volume of whatever is higher between the two
                */
                int p_v = p ? (1 << 9) : 0;
                int loop_v = loop ? (1 << 8) : 0;
                int a_v = a ? (1 << 7) : 0;
                int d_v = d ? 1 : 0;
                int mx_v = 0;
                if (is_sfx) {
                    if (is_music) {
                        mx_v = 1 << 11;
                    } else {
                        mx_v = 1 << 10;
                    }
                }
                value = (ushort)((v << 13) | p_v | loop_v | a_v | (channel << 3) | (bank << 1) | d_v | mx_v);
            }

            public ushort getValue() {
                return value;
            }
        }

        static SongMemory[] song_data = {
            new SongMemory(channel: 0, bank: 0),
            new SongMemory(channel: 0, bank: 0, loop: true, d: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 1, bank: 0, loop: true, a: true),
            new SongMemory(channel: 1, bank: 0, loop: true, d: true, a: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 8, bank: 0, is_sfx: true),
            new SongMemory(channel: 1, bank: 0, loop: true, d: true, a: true),
            new SongMemory(channel: 8, bank: 1, a: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 8, bank: 1, a: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 8, bank: 1, a: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 8, bank: 1, a: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 8, bank: 1, a: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 6, bank: 2, p: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 3, bank: 1, loop: true, a: true),
            new SongMemory(channel: 3, bank: 1, loop: true, a: true),
            new SongMemory(channel: 8, bank: 2, a: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 1, bank: 0, loop: true, d: true),
            new SongMemory(channel: 7, bank: 2, p: true, d: true, a: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 0, bank: 0, loop: true, d: true),
            new SongMemory(channel: 6, bank: 3, p: true, d: true, is_sfx: true),
            new SongMemory(channel: 6, bank: 3, p: true, d: true, is_sfx: true),
            new SongMemory(channel: 8, bank: 3, p: true, d: true, is_sfx: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 1, bank: 0, loop: true, a: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 1, bank: 1, loop: true, a: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 7, bank: 3, p: true, d: true, is_sfx: true),
            new SongMemory(channel: 7, bank: 3, p: true, d: true, is_sfx: true),
            new SongMemory(channel: 10, bank: 2, loop: true, a: true),
            new SongMemory(channel: 7, bank: 3, p: true, d: true, is_sfx: true),
            new SongMemory(channel: 3, bank: 0, loop: true, a: true),
            new SongMemory(channel: 2, bank: 1, loop: true, a: true),
            new SongMemory(channel: 2, bank: 2, loop: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 9, bank: 2, d: true, a: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 11, bank: 3, is_sfx: true, is_music: true),
            new SongMemory(channel: 3, bank: 2, d: true, a: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 10, bank: 2, is_sfx: true, is_music: true),
            new SongMemory(channel: 10, bank: 2, is_sfx: true, is_music: true),
            new SongMemory(channel: 8, bank: 2, is_sfx: true),
            new SongMemory(channel: 8, bank: 2, d: true, a: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 6, bank: 2, p: true, d: true, is_sfx: true),
            new SongMemory(channel: 1, bank: 0, loop: true, a: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 1, bank: 1, loop: true, a: true),
            new SongMemory(channel: 1, bank: 1, loop: true, a: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 3, bank: 1, a: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true, d: true),
            new SongMemory(channel: 3, bank: 0, a: true),
            new SongMemory(channel: 2, bank: 0, loop: true, a: true),
            new SongMemory(channel: 6, bank: 2, loop: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 1, bank: 0, loop: true),
            new SongMemory(channel: 1, bank: 0, loop: true, a: true),
            new SongMemory(channel: 1, bank: 1, loop: true, d: true, a: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 8, bank: 2, d: true, is_sfx: true),
            new SongMemory(channel: 4, bank: 2, loop: true, d: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 8, bank: 3, d: true, is_sfx: true),
            new SongMemory(channel: 0, bank: 0, loop: true, d: true),
            new SongMemory(channel: 8, bank: 2, d: true, a: true, is_sfx: true),
            new SongMemory(channel: 1, bank: 0, loop: true, a: true),
            new SongMemory(channel: 3, bank: 1, loop: true, a: true),
            new SongMemory(channel: 2, bank: 1, loop: true, a: true),
            new SongMemory(channel: 2, bank: 0, loop: true, a: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 7, bank: 2, p: true, d: true, is_sfx: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 1, bank: 0, loop: true, a: true),
            new SongMemory(channel: 1, bank: 0, loop: true, a: true),
            new SongMemory(channel: 0, bank: 0, loop: true, d: true),
            new SongMemory(channel: 2, bank: 1, loop: true, d: true, a: true),
            new SongMemory(channel: 0, bank: 1, loop: true),
            new SongMemory(channel: 3, bank: 0, loop: true),
            new SongMemory(channel: 3, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 1, bank: 0, loop: true, a: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true, d: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 2, bank: 1, loop: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 9, bank: 1, loop: true, a: true),
            new SongMemory(channel: 1, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 5, bank: 1, loop: true, a: true),
            new SongMemory(channel: 0, bank: 0, loop: true, d: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 3, bank: 1, loop: true, a: true),
            new SongMemory(channel: 2, bank: 0, loop: true, a: true),
            new SongMemory(channel: 0, bank: 0, loop: true, d: true),
            new SongMemory(channel: 1, bank: 0, loop: true, d: true),
            new SongMemory(channel: 0, bank: 0, loop: true, d: true),
            new SongMemory(channel: 0, bank: 0, loop: true, d: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 2, bank: 1, a: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 2, bank: 1, a: true, is_sfx: true, is_music: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 1, bank: 0, loop: true, a: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true, d: true),
            new SongMemory(channel: 3, bank: 0, loop: true, a: true),
            new SongMemory(channel: 2, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 7, bank: 2, a: true, is_sfx: true),
            new SongMemory(channel: 7, bank: 3, is_sfx: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true, d: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true, d: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 8, bank: 2, d: true, is_sfx: true),
            new SongMemory(channel: 8, bank: 3, p: true, d: true, is_sfx: true),
            new SongMemory(channel: 8, bank: 3, p: true, d: true, is_sfx: true),
            new SongMemory(channel: 8, bank: 2, p: true, d: true, is_sfx: true),
            new SongMemory(channel: 8, bank: 2, p: true, d: true, is_sfx: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 8, bank: 2, p: true, d: true, is_sfx: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true, d: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 0, bank: 0, loop: true),
            new SongMemory(channel: 1, bank: 0, loop: true, a: true),
            new SongMemory(channel: 11, bank: 0, loop: true, a: true),
            new SongMemory(channel: 1, bank: 1, loop: true, a: true),
            new SongMemory(channel: 8, bank: 2, p: true, d: true, is_sfx: true),
            new SongMemory(channel: 3, bank: 0),
            new SongMemory(channel: 1, bank: 0, loop: true),
        };

        public static void writeVanillaSongData(string file) {
            int song_count = song_data.Length;
            try {
                int[] memoryArr = new int[song_count];
                for (int i = 0; i < song_count; i++) {
                    memoryArr[i] = song_data[i].getValue();
                }
                using (var fs = new FileStream(file, FileMode.Append, FileAccess.Write)) {
                    fs.Write(Lib.ArrayToByteArray(memoryArr, 2), 0x1FFF000, song_count * 2);
                }
            } catch (Exception ex) {
                Console.WriteLine("Exception caught in process: {0}", ex);
            }
        }
    }
}