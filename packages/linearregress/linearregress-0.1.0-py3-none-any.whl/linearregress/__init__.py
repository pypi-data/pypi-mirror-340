def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
height <- c(102,117,105,141,135,115,138,114,137,100,131,119,115,121,113)
weight <- c(61,46,62,54,60,69,51,50,46,64,48,56,64,48,59)
student <- lm(weight ~ height)
student
predict(student, data.frame (height = 199), interval="confidence")
plot(student)

    '''
    print(code)