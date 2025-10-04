import subprocess
import os

# credits: https://www.tutorialspoint.com/How-to-find-difference-between-2-files-in-Python with modification :D
def compare_file(file1, file2, p, q): # file1 ground truth; file2 answer
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        f1_lines = f1.readlines()
        f2_lines = f2.readlines()

        if((len(f1_lines) != len(f2_lines))): # but need to consider windows OS extra endline at the end
            print(f"Task {p}: Testcase {q}, line number amount wrong")
            return False

        for i in range(len(f1_lines)):
            if(f1_lines[i]!=f2_lines[i]):
                print(f"Task {p}: Testcase {q} is wrong!")
                print(f"Difference at line {i + 1}:\n")
                print(f"Solution: {f1_lines[i]}")
                print(f"Your Answer: {f2_lines[i]}")
                return False
    print(f"Task {p}: Testcase {q} pass!")
    return True

def compare_imagedump(file1, file2, p, q):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        f1_lines = f1.readlines()
        f2_lines = f2.readlines()

        try:
            if( int(f1_lines[0])!=int(f2_lines[0]) or int(f1_lines[1])!=int(f2_lines[1]) ):
                print(f"Task {p}: Testcase {q} is wrong, image dimension is incorrect")
                return 0
            err = 0.0
            for i in range(int(f1_lines[0])*int(f1_lines[1])):
                rgb_sol = f1_lines[2+i].split()
                rgb_ans = f2_lines[2+i].split()
                for j in range(3):
                    err += abs(int(rgb_sol[j]) - int(rgb_ans[j]))
            err /= int(f1_lines[0])*int(f1_lines[1])*3
            if(err <= 2.55):
                print(f"Task {p}: Testcase {q} pass!")
                return 1
            elif(err <= 12.75):
                print(f"Task {p}: Testcase {q} gets 75% partial credit; Average per pixel channel error: {err}")
                return 0.75
            else:
                print(f"Task {p}: Testcase {q} is wrong, image is significantly different")
                return 0
        except Exception as e:
            print(f"Task {p}: Testcase {q} is wrong, output is malformed")
            print(e)
            return 0


# compiles program
os.system("gcc -Wuninitialized -std=c99 main.c image_processing.c game.c lib/cbmp.c -o pa.exe -lm")

pts = 0
include_private_testcases = False

# Task 1 grading
# Public testcases
tpts = 0.0
print("Task 1")
for i in range(2):
    try:
        subprocess.check_output(f"ulimit -s 64000 && cat testcases/testcase1_{i+1}.txt | ./pa.exe > out.txt", shell=True, timeout=10)
        if compare_file(f"testcases/output/output1_{i+1}.txt", "out.txt", 1, i+1):
            pts += 1
            tpts += 1
    except subprocess.TimeoutExpired:
        print(f"Task 1: Testcase {i+1} timed out!")
    except subprocess.CalledProcessError:
        print(f"Task 1: Testcase {i+1} gives out an error!")
print(f"{tpts}/2.0\n")

# Private testcases
tpts = 0.0
if include_private_testcases:
    print("Task 1 (Private Testcases)")
    for i in range(2):
        try:
            subprocess.check_output(f"ulimit -s 64000 && cat testcases/_testcase1_{i+1}.txt | ./pa.exe > out.txt", shell=True, timeout=10)
            if compare_file(f"testcases/output/_output1_{i+1}.txt", "out.txt", 1, i+1):
                pts += 1.5
                tpts += 1.5
        except subprocess.TimeoutExpired:
            print(f"Task 1: Testcase {i+1} timed out!")
        except subprocess.CalledProcessError:
            print(f"Task 1: Testcase {i+1} gives out an error!")

    print(f"{tpts}/3.0\n")


# Task 2 grading
# Public testcases
tpts = 0.0
print("Task 2")
for i in range(2):
    try:
        subprocess.check_output(f"ulimit -s 64000 && cat testcases/testcase2_{i+1}.txt | ./pa.exe > out.txt", shell=True, timeout=10)
        mult = compare_imagedump(f"testcases/output/dump2_{i+1}.txt", "dump.txt", 2, i+1)
        pts += 1.5 * mult
        tpts += 1.5 * mult
    except subprocess.TimeoutExpired:
        print(f"Task 2: Testcase {i+1} timed out!")
    except subprocess.CalledProcessError:
        print(f"Task 2: Testcase {i+1} gives out an error!")
print(f"{tpts}/3.0\n")

# Private testcases
tpts = 0.0
if include_private_testcases:
    print("Task 2 (Private Testcases)")
    for i in range(3):
        try:
            subprocess.check_output(f"ulimit -s 64000 && cat testcases/_testcase2_{i+1}.txt | ./pa.exe > out.txt", shell=True, timeout=10)
            mult = compare_imagedump(f"testcases/output/_dump2_{i+1}.txt", "dump.txt", 2, i+1)
            pts += 4.0 * mult
            tpts += 4.0  * mult
        except subprocess.TimeoutExpired:
            print(f"Task 2: Testcase {i+1} timed out!")
        except subprocess.CalledProcessError:
            print(f"Task 2: Testcase {i+1} gives out an error!")

    print(f"{tpts}/12.0\n")


# Task 3 grading
# Public testcases
tpts = 0.0
print("Task 3 [ConvFilter Generation]")
for i in range(3):
    try:
        subprocess.check_output(f"ulimit -s 64000 && cat testcases/testcase3_{i+1}.txt | ./pa.exe > out.txt", shell=True, timeout=10)
        if compare_file(f"testcases/output/output3_{i+1}.txt", "out.txt", 3, i+1):
            pts += 1
            tpts += 1
    except subprocess.TimeoutExpired:
        print(f"Task 3: Testcase {i+1} timed out!") 
    except subprocess.CalledProcessError:
        print(f"Task 3: Testcase {i+1} gives out an error!")
print(f"{tpts}/3.0\n")

# Private testcases
tpts = 0.0
if include_private_testcases:
    print("Task 3 [ConvFilter Generation] (Private Testcases)")
    for i, j in zip(range(4), [1, 2, 2, 2]):
        try:
            subprocess.check_output(f"ulimit -s 64000 && cat testcases/_testcase3_{i+1}.txt | ./pa.exe > out.txt", shell=True, timeout=10)
            if compare_file(f"testcases/output/_output3_{i+1}.txt", "out.txt", 3, i+1):
                pts += j
                tpts += j
        except subprocess.TimeoutExpired:
            print(f"Task 3: Testcase {i+1} timed out!")
        except subprocess.CalledProcessError:
            print(f"Task 3: Testcase {i+1} gives out an error!")

    print(f"{tpts}/7.0\n")

# Task 3
# Public testcases
tpts = 0.0
print("Task 3 [Average Blurring and Gaussian Blurring]")
for i in range(3, 5):
    try:
        subprocess.check_output(f"ulimit -s 64000 && cat testcases/testcase3_{i+1}.txt | ./pa.exe > out.txt", shell=True, timeout=10)
        mult = compare_imagedump(f"testcases/output/dump3_{i+1}.txt", "dump.txt", 3, i+1)
        pts += 1 * mult
        tpts += 1 * mult
    except subprocess.TimeoutExpired:
        print(f"Task 3: Testcase {i+1} timed out!")
    except subprocess.CalledProcessError:
        print(f"Task 3: Testcase {i+1} gives out an error!")
print(f"{tpts}/2.0\n")

# Private testcases
tpts = 0.0
if include_private_testcases:
    print("Task 3 [Average Blurring and Gaussian Blurring] (Private Testcases)")
    for i, j in zip(range(4, 9), [2, 2, 3, 3, 3]):
        try:
            subprocess.check_output(f"ulimit -s 64000 && cat testcases/_testcase3_{i+1}.txt | ./pa.exe > out.txt", shell=True, timeout=10)
            mult = compare_imagedump(f"testcases/output/_dump3_{i+1}.txt", "dump.txt", 3, i+1)
            pts += j * mult
            tpts += j * mult
        except subprocess.TimeoutExpired:
            print(f"Task 3: Testcase {i+1} timed out!")
        except subprocess.CalledProcessError:
            print(f"Task 3: Testcase {i+1} gives out an error!")

    print(f"{tpts}/13.0\n")

# Task 4
# Public testcases
tpts = 0.0
print("Task 4")
for i in range(3):
    try:
        subprocess.check_output(f"ulimit -s 64000 && cat testcases/testcase4_{i+1}.txt | ./pa.exe > out.txt", shell=True, timeout=10)
        mult = compare_imagedump(f"testcases/output/dump4_{i+1}.txt", "dump.txt", 4, i+1)
        pts += 1 * mult
        tpts += 1 * mult
    except subprocess.TimeoutExpired:
        print(f"Task 4: Testcase {i+1} timed out!")
    except subprocess.CalledProcessError:
        print(f"Task 4: Testcase {i+1} gives out an error!")
print(f"{tpts}/3.0\n")

# Private testcases
tpts = 0.0
if include_private_testcases:
    print("Task 4 (Private Testcases)")
    for i in range(3):
        try:
            subprocess.check_output(f"ulimit -s 64000 && cat testcases/_testcase4_{i+1}.txt | ./pa.exe > out.txt", shell=True, timeout=10)
            mult = compare_imagedump(f"testcases/output/_dump4_{i+1}.txt", "dump.txt", 4, i+1)
            pts += 4 * mult
            tpts += 4 * mult
        except subprocess.TimeoutExpired:
            print(f"Task 4: Testcase {i+1} timed out!")
        except subprocess.CalledProcessError:
            print(f"Task 4: Testcase {i+1} gives out an error!")

    print(f"{tpts}/12.0\n")

# Task 5 grading
# Public testcases
tpts = 0.0
print("Task 5")
for i in range(2):
    try:
        subprocess.check_output(f"ulimit -s 64000 && cat testcases/testcase5_{i+1}.txt | ./pa.exe > out.txt", shell=True, timeout=10)
        if compare_file(f"testcases/output/output5_{i+1}.txt", "out.txt", 5, i+1):
            pts += 1
            tpts += 1
    except subprocess.TimeoutExpired:
        print(f"Task 5: Testcase {i+1} timed out!")
    except subprocess.CalledProcessError:
        print(f"Task 5: Testcase {i+1} gives out an error!")
print(f"{tpts}/2.0\n")

# Private testcases
tpts = 0.0
if include_private_testcases:
    print("Task 5 (Private Testcases)")
    for i in range(2):
        try:
            subprocess.check_output(f"ulimit -s 64000 && cat testcases/_testcase5_{i+1}.txt | ./pa.exe > out.txt", shell=True, timeout=10)
            if compare_file(f"testcases/output/_output5_{i+1}.txt", "out.txt", 5, i+1):
                pts += 4
                tpts += 4
        except subprocess.TimeoutExpired:
            print(f"Task 5: Testcase {i+1} timed out!")
        except subprocess.CalledProcessError:
            print(f"Task 5: Testcase {i+1} gives out an error!")

    print(f"{tpts}/8.0\n")

# Task 6 grading
# Public testcases
tpts = 0.0
print("Task 6")
for i in range(2):
    try:
        subprocess.check_output(f"ulimit -s 64000 && cat testcases/testcase6_{i+1}.txt | ./pa.exe > out.txt", shell=True, timeout=10)
        if compare_file(f"testcases/output/output6_{i+1}.txt", "out.txt", 6, i+1):
            pts += 1
            tpts += 1
    except subprocess.TimeoutExpired:
        print(f"Task 6: Testcase {i+1} timed out!")
    except subprocess.CalledProcessError:
        print(f"Task 6: Testcase {i+1} gives out an error!")
print(f"{tpts}/2.0\n")

# Private testcases
tpts = 0.0
if include_private_testcases:
    print("Task 6 (Private Testcases)")
    for i in range(4):
        try:
            subprocess.check_output(f"ulimit -s 64000 && cat testcases/_testcase6_{i+1}.txt | ./pa.exe > out.txt", shell=True, timeout=10)
            if compare_file(f"testcases/output/_output6_{i+1}.txt", "out.txt", 6, i+1):
                pts += 2
                tpts += 2
        except subprocess.TimeoutExpired:
            print(f"Task 6: Testcase {i+1} timed out!")
        except subprocess.CalledProcessError:
            print(f"Task 6: Testcase {i+1} gives out an error!")

    print(f"{tpts}/8.0\n")

# Task 7 grading
# Public testcases
tpts = 0.0
print("Task 7")
for i in range(4):
    try:
        subprocess.check_output(f"ulimit -s 64000 && cat testcases/testcase7_{i+1}.txt | ./pa.exe > out.txt", shell=True, timeout=10)
        if compare_file(f"testcases/output/output7_{i+1}.txt", "out.txt", 7, i+1):
            pts += 1
            tpts += 1
    except subprocess.TimeoutExpired:
        print(f"Task 7: Testcase {i+1} timed out!")
    except subprocess.CalledProcessError:
        print(f"Task 7: Testcase {i+1} gives out an error!")
print(f"{tpts}/4.0\n")

# Private testcases
tpts = 0.0
if include_private_testcases:
    print("Task 7 (Private Testcases)")
    for i in range(4):
        try:
            subprocess.check_output(f"ulimit -s 64000 && cat testcases/_testcase7_{i+1}.txt | ./pa.exe > out.txt", shell=True, timeout=10)
            if compare_file(f"testcases/output/_output7_{i+1}.txt", "out.txt", 7, i+1):
                pts += 4
                tpts += 4
        except subprocess.TimeoutExpired:
            print(f"Task 7: Testcase {i+1} timed out!")
        except subprocess.CalledProcessError:
            print(f"Task 7: Testcase {i+1} gives out an error!")

    print(f"{tpts}/16.0\n")


if include_private_testcases:
    print(f"Final grade: {pts}/100.0 | {pts}%")
else:
    print(f"Final grade: {pts}/21.0 | {pts/21 * 100}%")