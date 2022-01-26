
from Katna.video import Video
from Katna.writer import KeyFrameDiskWriter
import os

import resnet as resnet
import glob


def extract_frames(ip_file, op_folder, frame_count):
    vd= Video()
    diskwriter= KeyFrameDiskWriter(location=op_folder)
    video_path= os.path.join(ip_file)
    vd.extract_video_keyframes(
        no_of_frames= frame_count,
        file_path=video_path,
        writer=diskwriter,
    )

def delete_existing_files(folder):
    files= glob.glob(folder+"/*")
    for f in files:
        os.remove(f)


def get_vectors_for_video(ip_file, op_folder, frame_count):

    delete_existing_files(op_folder)

    extract_frames(ip_file, op_folder, frame_count)

    images= list(glob.glob(op_folder+"/*"))

    vector= resnet.apply_resnet50(images)
    
    return vector


    






if __name__== "__main__":
    ip_file= "../liv_data/Video/0hu12MP7b1U.mp4"
    op_folder= "../liv_data/tmp_files"
    # extract_frames(ip_file, op_folder, 6)
    res= get_vectors_for_video(ip_file, op_folder, 6)
    print(res.shape)