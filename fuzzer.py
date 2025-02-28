import os
import random
import subprocess

def mutate(jpg):
    # Randomly choose a byte to mutate
    index = random.randint(0, len(jpg) - 1)
    # Randomly choose a new byte value
    new_byte = random.randint(0, 255)
    # Replace the byte at index with new_byte
    new_jpg = jpg[:index] + bytes([new_byte]) + jpg[index+1:]
    return new_jpg

def run_jpeg2bmp(temp_jpg, output_bmp):
    """
    Runs the target program (jpeg2bmp) using the mutated image file.
    Returns the stderr output from the program.
    """
    try:
        command = f"./jpeg2bmp {temp_jpg} /output/{output_bmp}"
        ret = os.system(command)
        ret_code = os.WEXITSTATUS(ret)
    except subprocess.TimeoutExpired:
        print("Execution timed out.")
        return ""
    return ret, ret_code


def main():
    with open("cross.jpg", 'rb') as file:
        crossjpg = file.read()
    
    for a in range(0,100):
        for b in range(random.randint(0,500)):
            new_jpg = mutate(crossjpg)
        with open("temp.jpg", 'wb') as file:
            file.write(new_jpg)
        stderr = run_jpeg2bmp(crossjpg, f"output{a}.bmp")
        if "Error" in stderr:
            print("Crashed with input: {}".format(new_jpg))
            break
    
    
    
    
    # for i in range(fuzz_num):
    #     # Compose values for firstInt, charArray, secondInt
    #     first_int = random.randint(0, 49999)
    #     second_int = random.randint(0, 1)
    #     array_size = random.randint(0, 19)
        
    #     char_array = 'A' * array_size
        
    #     command = "./jpeg2bmp {} \"{}\" {}\n".format(first_int, char_array, second_int)
        
    #     ret = os.system(command)
    #     ret_code = os.WEXITSTATUS(ret)
        
    #     print("retCode={}  ## Input:  firstInt = {},  arraySize = {}, secondInt = {}".format(ret_code, first_int, array_size, second_int))

if __name__ == "__main__":
    main()