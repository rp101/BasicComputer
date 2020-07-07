import assembler

#while True:
#text = input(">> ")
f = open("src.abc", "r")

result, error = assembler.run(f.read())

if error: print(error)
else: print(result)
