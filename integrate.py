
from scipy import integrate

def square_result(x):
	return x*x
	
result, err = integrate.quad(square_result, -1, 1)
print result