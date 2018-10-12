from world import World
import sys
import os

if sys.version_info[0] == 2:
    input = raw_input

print("""                     _     _ _                   
                    | |   | | |                  
 __      _____  _ __| | __| | | __ _ _ __   __ _ 
 \ \ /\ / / _ \| '__| |/ _` | |/ _` | '_ \ / _` |
  \ V  V / (_) | |  | | (_| | | (_| | | | | (_| |
   \_/\_/ \___/|_|  |_|\__,_|_|\__,_|_| |_|\__, |
                                            __/ |
                                           |___/ 

\n\n\n""")

world = World()

def repl():
    global world
    while(True):
        code = input('>>> ')
        code = code.strip()
        while '  ' in code:
            code = code.replace('  ', ' ')
        args = code.split(' ')
        arg0 = args[0].lower()
        if arg0 == 'exit':
            break
        elif arg0 == 'reset':
            world = World()
        elif arg0 == 'save':
            path = input('Enter file name:')
            ext = '.world'
            if path[-len(ext):].lower() != ext:
                path += ext
            world.save(path)
            print('World saved to ' + path)
        elif arg0 == 'load':
            path = input('Enter file name:')
            ext = '.world'
            if path[-len(ext):].lower() != ext:
                path += ext
            if not os.path.isfile(path):
                print('File not found: ' + path)
            try:
                world = World.load(path)
            except Exception as ex:
                print(ex)
            print('World loaded from ' + path)
        else:    
            try:
                world.run(*args)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    repl()
