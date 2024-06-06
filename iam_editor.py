from PIL import Image as im
import numpy as np

map_elements = 128 * 128


def read_iam(iam_path):
    with open(iam_path, "rb+") as iam_file:
        iam_content = iam_file.read()
    return iam_content


def write_modified_iam(iam_path, iam_content):
    modified_iam_content = bytearray(iam_content)
    modified_texture_id = 3400
    overwrite_all_textures(modified_iam_content, modified_texture_id)
    with open(iam_path, "wb+") as iam_file:
        iam_file.write(modified_iam_content)
    return


def overwrite_all_textures(modified_iam_content, texture_id):
    cursor = 8
    bytes_to_insert = texture_id.to_bytes(2, byteorder='little')
    zeros = b'\x00\x00'
    for i in range(map_elements):
        # print(modified_iam_content[cursor:cursor+2])
        if modified_iam_content[cursor:cursor+2] == zeros:
            pass
            # print('zeros!')
        else:
            modified_iam_content[cursor:cursor+2] = bytes_to_insert
        cursor += 6


def group_raw_iam_data(iam_content):
    save_type = int.from_bytes(iam_content[0:4], "little")
    ob_size = int.from_bytes(iam_content[4:8], "little")
    cursor = 8
    concat_string_result = ''
    for i in range(map_elements):
        texture = int.from_bytes(iam_content[cursor:cursor+2], "little")
        texture_with_mask = texture & 0x3ff
        cursor += 6
        concat_string_result += str(texture_with_mask) + ' '
        if i % 128 == 127:
            concat_string_result += "\n"

    # print(concat_string_result)


def app():
    iam_filename = 'oval1.iam'
    iam_path = f'res/iam/final_release/{iam_filename}'
    output_path = f'out/iam/{iam_filename}'
    iam_content = read_iam(iam_path)
    group_raw_iam_data(iam_content)
    write_modified_iam(output_path, iam_content)


def pil_test():
    array = np.arange(0, 737280, 1, np.uint8) # check type of array
    print(type(array))

    # our array will be of width
    # 737280 pixels That means it
    # will be a long dark line
    print(array.shape)

    # Reshape the array into a
    # familiar resoluition
    array = np.reshape(array, (1024, 720))

    # show the shape of the array
    print(array.shape)

    # show the array
    print(array)

    # creating image object of
    # above array
    data = im.fromarray(array)

    # saving the final output
    # as a PNG file
    data.save('gfg_dummy_pic.png')


if __name__ == '__main__':
    app()
