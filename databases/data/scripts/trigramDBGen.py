# Written by Niraj Mahajan, Department of Computer Science, IIT Bombay.

# Loads a pickle with elements as trigrams seperated by $ along with their frequencies
# Adds this into the sql database
import os
import argparse
import sqlite3
import pickle

# parser = argparse.ArgumentParser()
# parser.add_argument('--path', required=True)

# args = vars(parser.parse_args())

# if(not os.path.exists(args['path'])):
# 	print("Invalid Path")
# 	os._exit(1)

# if(not os.path.isfile(args['path'])):
# 	print("Path does not have a file")
# 	os._exit(2)

with open('trig.pickle', 'rb') as handle:
    TRIG = pickle.load(handle)
print('Loaded the dictionary', flush = True)

conn = sqlite3.connect('../dumps/Trigram-Bigram-Dictionary.db')
c = conn.cursor()

c.execute('''DROP TABLE IF EXISTS Trigrams1''')

c.execute('''CREATE TABLE Trigrams1
             (id INTEGER PRIMARY KEY,first text, second text, third text, freq INTEGER)''')
          
print('Created the table', flush=True)
count = 0
sql_str = "INSERT into Trigrams1(first, second, third, freq) values(?,?,?,?)"
data = []
# outf = open('outTrigWithFreq.txt', 'w')
# outf.write('first,second,third,freq\n')
# with open(args['path'], 'r') as infile:
for elem, freq in sorted(TRIG.items(), key = lambda x: x[1],reverse = True):
	count = count + 1;
	if(count % 100000 == 0):
		print(count, end = ", ", flush=True)
		c.executemany(sql_str, data)
		conn.commit()
		data = []
	word_list = elem.split('$')
	w1 = word_list[0]
	w2 = word_list[1]
	w3 = word_list[2]
	# c.execute('''SELECT id, freq FROM Trigrams1 WHERE first = ? AND second = ? AND third = ?''', (w1, w2, w3))
	# data1 = c.fetchall()

	# if(len(data1) == 0):
	# 	c.execute('''INSERT into Trigrams1(first, second, third, freq) values(?,?,?,?)''', (w1, w2, w3, 1))
	# else:
	# 	c.execute('''UPDATE Trigrams1 SET freq = ? WHERE id = ?''', (data1[0][1]+1, data1[0][0]))
	data.append((w1, w2, w3, freq,))

print('\nData generated', flush = True)
c.executemany(sql_str, data)
# outf.close()
conn.commit()
c.close()
conn.close()			