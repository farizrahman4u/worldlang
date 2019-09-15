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
        if not args:
            continue
        arg0 = args[0].lower()
        if not arg0:
            continue
        if arg0[0] == '#':
            continue
        if arg0 == 'exit':
            break
        elif arg0 == 'reset':
            world = World()
        elif arg0 == 'save':
            path = input('Enter file name:')
            ext = '.world'
            if path[-len(ext):].lower() != ext:
                path += ext
            try:
                world.save(path)
            except Exception as e:
                print(e)
                continue
            print('World saved to ' + path)
        elif arg0 == 'load':
            path = input('Enter file name:')
            ext = '.world'
            if path[-len(ext):].lower() != ext:
                path += ext
            if not os.path.isfile(path):
                print('File not found: ' + path)
                continue
            try:
                world = World.load(path)
            except Exception as e:
                print(str(e))
                continue
            print('World loaded from ' + path)
        elif arg0 == 'graph':
            if len(args) > 1:
                arg1 = args[1].lower()
                assert arg1 in ['objects', 'types']
            else:
                arg1 = 'objects'
            if arg1 == 'objects':
                from dot import object_graph
                dot = object_graph(world)
            else:
                from dot import type_graph
                dot = type_graph(world)
            dot.format = 'png'
            tmp = 'temp.png'
            if os.path.isfile(tmp):
                os.remove(tmp)
            dot.render(tmp, view=True)
        elif arg0 == 'code':
            print(world.get_code() + '\n')
        else:    
            try:
                world.run(*args)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    repl()
