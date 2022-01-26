
import helpers

audio_file= helpers.path_of("../audio/vgg19.txt")

with open(audio_file) as file:
    for line_no, line in enumerate(file):
        if line.split(",")[0]=="nan":
            print(line)
            continue
        if line.split(",")[0]=="inf":
            print(line)
            continue
        print(line)
        line= eval("["+line+"]")
        if line[0] is None:
            print(line)
        # print(line)
        # exit()