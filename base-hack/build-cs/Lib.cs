using System.Net;
using System.IO;
using System;

namespace DK64BuildRoutine {
    internal class Lib {
        public static void FileSizeFix (string file) {
            FileInfo fi = new FileInfo(file);
            int length = (int)fi.Length;
            int to_add = length & 0xF;
            if (to_add != 0) {
                try {
                    byte[] byteArray = new byte[to_add];
                    for (int i = 0; i < to_add; i++) {
                        byteArray[i] = 0;
                    }
                    using (var fs = new FileStream(file, FileMode.Append, FileAccess.Write)) {
                        fs.Write(byteArray, length, to_add);
                    }
                } catch (Exception ex) {
                    Console.WriteLine("Exception caught in process: {0}", ex);
                }
            }
        }

        public static float IntToFloat(int intf) {
            // TODO: This
            // int* val = &intf;
            // return *(float*)val;
            return 0.0f;
        }

        public static int FloatToInt(float floati) {
            // TODO: This
            // float* val = &floati;
            // return *(int*)val;
            return 0;
        }

        public static byte[] ArrayToByteArray(int[] array, int item_size) {
            byte[] output = new byte[array.Length * item_size];
            for (int i = 0; i < array.Length; i++) {
                int local_value = array[i] & ((1 << (8 * item_size)) - 1);
                for (int j = 0; j < item_size; j++) {
                    byte value = (byte)(local_value & 0xFF);
                    local_value >>= 8;
                    output[(i * item_size) + j] = value;
                }
            }
            return output;
        }
    }
}