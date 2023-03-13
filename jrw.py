import json
import sys

def stuff():
    global metadata
    global instruction
    if instruction == 0:
        with open('/home/david/Desktop/Backend/jsontest.txt') as f:
            #json_metadata = f.readline()
            json_metadata = json.load(f)
            metadata = json.loads(json_metadata)
            print(metadata)

            #json_metadata = json.load(f)
            sensor_id = metadata['sensor_id']
            location = metadata['location']
            file_type = metadata['file_type']
            print(sensor_id, location, file_type)
            print("[+] Returning from reading from jrw.py")
            print("[++++++++++++++++++++++++++++]")
    else:
        with open('/home/david/Desktop/Backend/jsontest.txt', 'r+') as f:
            #json.dump(metadata, f)
            f.truncate()
            f.seek(0)
            json.dump(metadata, f)
            print("[+] Returning from writing to jrw.py")
    

#do a whole if statement that determines if we are reading or writing therefore just 1 code
#param1 = sys.argv[1]
file_type = sys.argv[1]
instruction = int(sys.argv[2])
metadata = sys.argv[3]
print(f"[+]this is the meta data {metadata}")
print("[+] running JRW.py...")
#print(file_type, instruction, metadata)
stuff()
