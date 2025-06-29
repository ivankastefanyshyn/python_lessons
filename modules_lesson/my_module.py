def greeting(name):
    print(f"Hello, {name}")


person = {"name": "Vira", "age": 57, "country": "Ukraine"}
print(person)

numbers = [1, 2, 3, 4, 5]
print(numbers)

sentence = "I try to learn Python"
print(sentence)


# __name__
def say_hello():
    print("Hello")
    if __name__ == "__main__":
        print("mymodule is executed directly")
    else:
        print("mymodule is imported as module")


say_hello()
