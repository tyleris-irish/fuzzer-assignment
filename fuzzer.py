import os
import random
import subprocess
import re

def mutate(jpg):
    """
    Mutates a jpeg file by randomly changing a single byte.
    """
    index = random.randint(0, len(jpg) - 1)
    new_byte = random.randint(0, 255)
    new_jpg = jpg[:index] + bytes([new_byte]) + jpg[index+1:]
    return new_jpg

def run_jpeg2bmp(temp_jpg, output_bmp):
    """
    Runs the target program (jpeg2bmp) using the mutated image file.
    Returns the combined output (stdout and stderr), the extracted bug number (if any),
    and the return code.
    """
    command = f"./jpeg2bmp {temp_jpg} ./output/{output_bmp}"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        output = result.stdout + result.stderr

        # Print the output if a bug was found
        if "Found bug" in str(result):
            print(result)
        
        # Use regex to extract the bug number from the output.
        match = re.search(r'Bug#(\d+)', output)
        bug_number = match.group(1) if match else None
        
    except subprocess.TimeoutExpired:
        print("Execution timed out.")
        return "", None, None
        
    return output, bug_number


def main():
    # Initialize directories and variables
    os.makedirs("bugged_input", exist_ok=True)
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    with open("cross.jpg", 'rb') as file:
        crossjpg = file.read()
    
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
    
    # Attempt 1000 fuzzing iterations
    for a in range(1,1000):
        # Mutate the input file a random number of times
        for _ in range(random.randint(0,500)):
            new_jpg = mutate(crossjpg)
        with open(f"./input/temp{a}.jpg", 'wb') as file:
            file.write(new_jpg)

        # Run the target program with the mutated input
        output, bug_number = run_jpeg2bmp(f"./input/temp{a}.jpg", f"output{a}.bmp")
        
        # If a bug was found, save the mutated input file and record bug
        if bug_number:
            bugs[int(bug_number)] += 1
            bugs["total"] += 1
            print(f"Found bug #{bug_number} with input: temp{a}.jpg")
            with open(f"./bugged_input/bug{bug_number}.jpg", 'wb') as file:
                file.write(new_jpg)

        if "Error" in output:
            print("Crashed with input: {}".format(new_jpg))
            break
    
    # Print summary of bugs found
    print("Bugs found:")
    for bug, count in bugs.items():
        if count > 0:
            print(f"Bug #{bug}: {count} occurrences")

if __name__ == "__main__":
    main()