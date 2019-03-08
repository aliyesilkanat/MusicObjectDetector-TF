import os
import muscima.io
import glob
from collections import Counter
import argparse

from omrdatasettools.image_generators.MuscimaPlusPlusImageGenerator import MuscimaPlusPlusImageGenerator
from tqdm import tqdm

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_dir", default="data/muscima_pp_raw/v1.0/data/cropobjects_withstaff/")
    parser.add_argument("--mapping_output_path", default="mapping_all_classes.txt")
    parser.add_argument("--remove_line_shaped_or_construct", type=bool, default=False)
    args = parser.parse_args()

    names = glob.glob(os.path.join(args.dataset_dir, "*.xml"))
    data = {}
    image_generator = MuscimaPlusPlusImageGenerator()

    for name in tqdm(names, desc="Reading all objects from MUSCIMA++ annotations"):
        data[name] = image_generator.load_crop_objects_from_xml_file(name)
    datas = []

    for value in data.values():
        for val in value:
            datas.append(val)

    c = Counter([x.clsname for x in datas])

    ignored_classes = []  # ["double_sharp", "numeral_2", "numeral_5", "numeral_6", "numeral_7", "numeral_8"]
    line_shaped_or_construct = ["stem",
                                "beam",
                                "thin_barline",
                                "measure_separator",
                                "slur",
                                "tie",
                                "key_signature",
                                "dynamics_text",
                                "hairpin-decr.",
                                "other_text",
                                "tuple",
                                "hairpin-cresc.",
                                "time_signature",
                                "staff_grouping",
                                "trill",
                                "tenuto",
                                "tempo_text",
                                "multi-staff_brace",
                                "multiple-note_tremolo",
                                "repeat",
                                "multi-staff_bracket",
                                "tuple_bracket/line"]
    filtered_class_id = []
    for key, value in c.items():
        if key in ignored_classes:
            continue
        if args.remove_line_shaped_or_construct:
            if key not in line_shaped_or_construct:
                filtered_class_id.append(key)
        else:
            filtered_class_id.append(key)
    filtered_class_id.sort()
    with open(args.mapping_output_path, "w") as f:
        for i, classname in enumerate(filtered_class_id):
            f.write("""item{{
    id: {0}
    name: '{1}'
}}
""".format(i + 1, classname))
