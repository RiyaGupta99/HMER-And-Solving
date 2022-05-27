# inputs : dict {1:"",2:"x",...}
import os
import subprocess

root = os.getcwd()
SEGMENTED_FILES_DIRECTORY = os.path.join(root, "segmented")
FILE = "1_1_"
COUNT_THRESHOLD = 20


def feedback(feedback_dict):
    files = sorted(list(os.walk(SEGMENTED_FILES_DIRECTORY))[0][2])
    # assert here that lenght of segmented files is equal to length of dict
    count_file_read = open("count.txt","r")
    count = count_file_read.read()
    count_new_imgs = int(count.split(".")[0])
    count_file_read.close()
    for key, value in feedback_dict:
        if value == "Correct":
            pass
        else:
            image_file = FILE + str(key) + ".jpg"
            #copy image_file to dataset with folder name as the value
            count_new_imgs += 1
    if count_new_imgs >= COUNT_THRESHOLD:
        #retrain model
        train_parallel = subprocess.Popen(['python','train.py'])
        count_new_imgs = 0
        pass
    
    count_file_write = open("count.txt","w")
    count_file_write.write(count_new_imgs)
    count_file_write.close()