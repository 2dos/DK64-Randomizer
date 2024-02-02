using System.Net;
using System.IO;
using System;

namespace DK64BuildRoutine {
    internal class Models {
        internal class BoneVertex {
            public static int start;
            public static int count;

            public BoneVertex(int start_value, int count_value) {
                start = start_value;
                count = count_value;
            }
        }

        internal class Port {
            static void ModelTwo (string vertex_file, string dl_file, string overlay_dl_file, string model_name, string base_file) {

            }

            static void Actor (string vertex_file, string dl_file, string model_name, string base_file) {

            }

            static void ActorToM2 (int actor_index, string input_file, string output_file, int base_file_index, bool vertex_bottom_is_zero, float scale) {

            }

            static void SpriteToM2 (int new_image, float scaling, string output_file) {

            }

            static void RipCollision (int collision_source_model, int output_model, string output_file) {

            }
        }

        internal class Shrink {

        }

        internal class Fix {
            
        }

        public static void loadNewModels() {

        }
    }
}