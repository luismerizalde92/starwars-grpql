""" funcion para evaluar si un numero es par o multiplo de cinco
        
    :author: Luis Merizalde - luis.merizalde@outlook.com

    :return: nada
    :rtype: None      
"""

import time

# inicio tiempo de ejecución
start = time.time()
for x in range(101):
	str_print = f'{x}'
	# validar si el número es par
	if x % 2 == 0:
		str_print += ' buzz'
	# validar si el número es multiplo de cinco
	if x % 5 == 0:
		str_print += ' bazz'

	print(str_print)

# fin tiempo de ejecución
end = time.time()
print("Execution time of the program is - ", end-start)