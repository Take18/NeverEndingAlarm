import sys
import csv
import random
from os import path
from os import system
from time import sleep
from playsound import playsound
from concurrent.futures import ThreadPoolExecutor as tpe


def makeQuestion() :
	number = random.randint(2, 7)
	question = 1
	answer = []
	for i in range(number) :
		elem = random.choice([2, 3, 5, 7, 11, 13])
		question *= elem
		answer.append(str(elem))
	ret = {"question":question, "answer":answer}
	return ret

def playMusic() :
	global filename
	while running :
		playsound(filename)
		sleep(1)

def showQuestions() :
	global running
	if questions == False :
		correct = 0
		while correct < 10 :
			failure = False
			this_q = makeQuestion()
			answer = this_q['answer']
			q_number = this_q['question']
			while len(answer)>0 :
				system('cls')
				print()
				print(q_number)
				print()
				usr_input = input()
				if usr_input in answer :
					answer.remove(usr_input)
					q_number = int(q_number / int(usr_input))
				else :
					print()
					print("You are wrong...")
					failure = True
					break
			if failure :
				continue
			print()
			print("That's right!!")
			correct += 1
	else :
		q_copy = questions
		for q in q_copy :
			system('cls')
			failure = False
			answer = q["answer"]
			print()
			print(q["question"])
			while len(answer)>0 :
				usr_input = input()
				if usr_input in answer :
					answer.remove(usr_input)
				else :
					print()
					print("You are wrong...")
					q_copy.append(q)
					failure = True
					break
			if failure :
				continue
			print()
			print("That's right!!")
	running = False

def main() :
	global filename, questions
	if len(sys.argv)>1 and path.isfile(sys.argv[1]) :
		filename = sys.argv[1]
	elif path.isfile("sample.mp3") :
		filename = "sample.mp3"
	elif path.isfile("sample.wav") :
		filename = "sample.wav"
	else :
		return False

	if len(sys.argv)>2 and path.isfile(sys.argv[2]+'.csv') :
		rows = csv.reader(open(sys.argv[2]+'.csv', 'r'))
		questions = []
		for row in rows :
			tmp_ans = row[1:]
			answers = []
			for a in tmp_ans :
				answers.append(a.strip())
			questions.append({"question":row[0], "answer":answers})
	with tpe(max_workers=2) as e :
		e.submit(playMusic)
		e.submit(showQuestions)

running = True
filename = ""
questions = False
main()
