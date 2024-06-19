from obj_to_dataframe import *


def app():
    obj_input_path = "res/objs/darci1/0/pelvis00.obj"
    obj_df = extract_obj_to_df(obj_input_path)
    print(obj_df)


if __name__ == '__main__':
    app()

