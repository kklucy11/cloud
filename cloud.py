#from multiprocessing import process
import subprocess
import threading
#import concurrent.futures


english_list = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine'] + [str(i) for i in range(1, 10)]


def generate_intNumber(question_str):
    if question_str.isdigit():
        return int(question_str)
    else:
        return english_list.index(question_str) + 1

def find_question(question):
    _question = question.split()
    if _question[0] in english_list:
        return(question)
    else:
        first_word = ''
        for eng in english_list:
            for qu in _question:
                index = qu.find(eng)
                if index > 0:
                    first_word = eng
                    index = question.find(first_word)
                    return question[index:]
                    
def communication(a):
    # 建立與app_mining的通訊
    #proc = subprocess.Popen(["python3" , "question.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    proc = subprocess.Popen(["./app_mining" , "b0829009"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # 重複讀取問題與回答
    question_list = []
    word = ""
    while a==True:
        # 讀取問題
        out = proc.stdout.read(1).decode()
        if out != "\n":
            word += out
            if "=" in word:
                print(word)
                word = find_question(word)
                question_list = word.split()
                        
                num1 = generate_intNumber(question_list[0]) 
                num2 = generate_intNumber(question_list[2])
                answer = num1 * num2
                print(f"{num1} * {num2} = ", answer)

                # 將答案傳給執行檔
                proc.stdin.write(f"{answer}\n".encode())
                proc.stdin.flush()
                word = ""
        else:
            print(word)
            word = ""
    proc.communicate()

num = []
t_list = []

for n in range(1000):
    name = ("name", n)
    num.append(name)
for number in num:
    number = threading.Thread(target = communication, args=(True,))
    t_list.append(number)

 
# 開始工作
for t in t_list:
    t.start()
 
# 調整多程順序
for t in t_list:
    t.join()

#with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
#    executor.map(communication(True))