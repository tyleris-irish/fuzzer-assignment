import os
import random
import subprocess
import re

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
    Returns the combined output (stdout and stderr), the extracted bug number (if any),
    and the return code.
    """
    command = f"./jpeg2bmp {temp_jpg} /output/{output_bmp}"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        # Combine stdout and stderr
        output = result.stdout + result.stderr
        
        # Use regex to extract the bug number from the output.
        match = re.search(r'Bug#(\d+)', output)
        bug_number = match.group(1) if match else None
        
    except subprocess.TimeoutExpired:
        print("Execution timed out.")
        return "", None, None
        
    return output, bug_number, result.returncode


def main():
    with open("cross.jpg", 'rb') as file:
        crossjpg = file.read()
    os.makedirs("output", exist_ok=True)
    os.makedirs("input", exist_ok=True)

    bugs = {
        1:0,
        2:0,
        3:0,
        4:0,
        5:0,
        6:0,
        7:0,
        8:0,
        9:0,
        10:0,
        "total":0
    }

    for a in range(1,1000):
        for b in range(random.randint(0,500)):
            new_jpg = mutate(crossjpg)
        with open(f"./input/temp{a}.jpg", 'wb') as file:
            file.write(new_jpg)
        output, bug_number, return_code = run_jpeg2bmp(f"./input/temp{a}.jpg", f"output{a}.bmp")
        
        if bug_number:
            bugs[int(bug_number)] += 1
            bugs["total"] += 1
            print(f"Found bug #{bug_number} with input: temp{a}.jpg")
            with open(f"./output/bug{bug_number}.jpg", 'wb') as file:
                file.write(new_jpg)

        if "Error" in output:
            print("Crashed with input: {}".format(new_jpg))
            break
    
    print("Bugs found:")
    for bug, count in bugs.items():
        if count > 0:
            print(f"Bug #{bug}: {count} occurrences")

if __name__ == "__main__":
    main()