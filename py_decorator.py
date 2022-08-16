# Decorator Basic Practice
'''
First Class Function

Advantages:
1. High flexibility
2. High legibility
3. Help with packaging
4. Low code repetition rate / high simplicity
'''
import time

def separate():
    print('--------------------------------------------------')

# Decorator_func1
def print_func_name(func):
    def warp():
        print("Now use function '{}'".format(func.__name__))
        func()
    return warp

# Decorator_func2
def print_time(func):
    def warp2():
        print("Now the Unix time is {}".format(int(time.time())))
        func()
    return warp2

# Decorator with parameter
def print_func_time(time):
    def decorator(func):
        def warp():
            print("Now use function '{}'".format(func.__name__))
            print("Now the Unix time is {}".format(int(time)))
            func()
        return warp
    return decorator

# Decorator with Class
class Item:
    def __init__(self, func):
        self.name = func.__name__
        self.item_func = func

    def show_item(self):
        print(f'Item name = {self.name}')

# Decorator_1
@print_func_name
def dog_bark():
    print("Bark !!!")

# Decorator_2
@print_func_name
def cat_miaow():
    print("Miaow ~~~")

# Decorator_3
@print_func_name
@print_time
def human_oh():
    print('Ohhhh BBQ !')

# Decorator_4
@print_func_time(time=time.time())
def bee_bee():
    print("Bee ~~~")

# Decorator_5
@Item
def Create_item():
    print('Create a new item')

if __name__ == "__main__":
    separate()

    dog_bark()
    # > Now use function 'dog_bark'
    # > Bark !!!

    separate()

    cat_miaow()
    # > Now use function 'cat_miaow'
    # > Miaow ~~~

    separate()

    human_oh()
    # > Now use function 'warp2'
    # > Now the Unix time is ....
    # > Ohhhh BBQ !

    separate()

    bee_bee()
    # > Now use function 'bee_bee'
    # > Now use Unix time is ....
    # > Bee ~~~

    separate()

    item_1 = Create_item
    item_1.show_item()
    # > Item name = Template
    item_1.item_func()
    # > Create a new item

    separate()