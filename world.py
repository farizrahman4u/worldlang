class World(object):

    def __init__(self):

        # ---Object graph---

        # Set of all objects: set<str>
        self.objs = set()
        # Set of all types: set<str>
        self.types = set()
        # Set of all relations: set<str>
        self.rels = set()
        # Map from object to types: str->set<str>
        self.obj_2_types = dict()
        # Map from type to objects: str->set<str>
        self.type_2_objs = dict()
        # Map from relation to objects: str->set<str>
        self.rel_2_objs = dict()
        # Map from object+relation to objects: (str,str)->set<str>
        self.obj_rel_2_objs = dict()

        # ---Type graph---

        # str->set<str>
        self.sub_types = {}
        self.super_types = {}

    def copy(self):
        world = self.__class__()
        attrs = ['objs',
                 'types',
                 'rels',
                 'obj_2_types',
                 'type_2_objs',
                 'rel_2_objs',
                 'obj_rel_2_objs']
        for attr in attrs:
            setattr(world, getattr(self, attr).copy())
        return world

    def add_object(self, obj):
        if obj in self.objs:
            err = 'Unable to create object {}.'.format(obj)
            err += ' Antother object with the same name already exists.'
            raise ValueError(err)
        elif obj in self.types:
            err = 'Unable to create object {}.'.format(obj)
            err += ' A type with the same name already exists.'
            raise ValueError(err)
        elif obj in self.rels:
            err = 'Unable to create object {}.'.format(obj)
            err += ' A relation with the same name already exists.'
            raise ValueError(err)
        self.objs.add(obj)
        self.obj_2_types[obj] = set()
        if obj[0] == '$':
            self.type_object(obj, obj[1:])


    def delete_object(self, obj):
        if obj not in self.objs:
            err = 'Unable to delete object {}.'.format(obj)
            err += 'Object not found.'
            raise ValueError(err)
        self.objs.remove(obj)
        del self.obj_2_types[obj]
        for typ, objs in self.type_2_objs.items():
            if obj in objs:
                objs.remove(obj)
        for rel, objs in self.rel_2_objs.items():
            if obj in objs:
                objs.remove(obj)
        keys = list(self.obj_rel_2_objs.keys())
        for k in keys:
            if k[0] == obj:
                del self.obj_rel_2_objs[k]

    def add_type(self, typ):
        if typ in self.types:
            err = 'Unable to create type {}.'.format(typ)
            err += ' Antother type with the same name already exists.'
            raise ValueError(err)        
        elif typ in self.objs:
            err = 'Unable to create type {}.'.format(typ)
            err += ' An object with the same name already exists.'
            raise ValueError(err) 
        elif typ in self.rels:
            err = 'Unable to create type {}.'.format(typ)
            err += ' A relation with the same name already exists.'
            raise ValueError(err)
        self.types.add(typ)
        self.type_2_objs[typ] = set()
        self.sub_types[typ] = set()
        self.super_types[typ] = set()

    def type_type(self, sub_type, super_type, inc=False):
        if super_type not in self.types:
            raise ValueError('Unknown type {}.'.format(super_type))
        if sub_type not in self.types:
            raise ValueError('Unknown type {}.'.format(sub_type))
        self.sub_types[super_type].add(sub_type)
        if inc:
            self.super_types[sub_type].add(super_type)
        else:
            self.super_types[sub_type] = set([super_type])

    def type_object(self, obj, typ, inc=False):
        if typ not in self.types:
            raise ValueError('Unknown type {}.'.format(typ))
        if obj not in self.objs:
            self.add_object(obj)
        if inc:
            self.obj_2_types[obj].add(typ)
            self.type_2_objs[typ].add(obj)
        else:
            curr_types = self.obj_2_types[obj]
            for c_type in curr_types:
                self.type_2_objs[c_type].remove(obj)
            self.obj_2_types[obj] = set([typ])
            self.type_2_objs[typ] = set([obj])

    def untype_type(self, sub_type, super_type=None):
        if sub_type not in self.types:
            raise ValueError('Unknown type {}.'.format(sub_type))
        if super_type is None:
            curr_sup_types = self.super_types[sub_type]
            self.super_types[sub_type] = set()
            for c_type in curr_sup_types:
                self.sub_types[c_type].remove(sub_type)
        else:
            if super_type not in self.types:
                raise ValueError('Unknown type {}.'.format(super_type))
            if super_type not in self.super_types[sub_type]:
                err = '{} is not a super type of {}.'.format(super_type, sub_type)
                raise ValueError(err)
            self.super_types[sub_type].remove(super_type)
            self.sub_types[super_type].remove(sub_type)

    def untype_object(self, obj, typ=None):
        if typ is None:
            curr_types = self.obj_2_types[obj]
            self.obj_2_types[obj] = set()
            for c_type in curr_types:
                self.type_2_objs[c_type].remove(obj)
        else:
            if typ not in self.types:
                raise ValueError('Unknown type {}.'.format(typ))
            if typ not in self.obj_2_types[obj]:
                err = 'Object {} is does not belong to type {}.'.format(obj, typ)
                raise ValueError(err)
            self.obj_2_types[obj].remove(typ)
            self.type_2_objs[typ].remove(obj)

    def delete_type(self, typ):
        if typ not in self.types:
            err = 'Unable to delete type {}.'.format(typ)
            err += 'Type not found.'
            raise ValueError(err)
        self.types.remove(typ)
        objs = self.type_2_objs.pop(typ)
        for obj in objs:
            self.obj_2_types[obj].remove(typ)
        del self.sub_types[typ]
        del self.super_types[typ]

    def add_relation(self, rel):
        if rel in self.rels:
            err = 'Unable to create relation {}.'.format(rel)
            err += ' Antother relation with the same name already exists.'
            raise ValueError(err)
        elif rel in self.objs:
            err = 'Unable to create relation {}.'.format(rel)
            err += ' An object with the same name already exists.'
            raise ValueError(err)
        elif rel in self.types:
            err = 'Unable to create relation {}.'.format(rel)
            err += ' A type with the same name already exists.'
            raise ValueError(err)
        self.rels.add(rel)
        self.rel_2_objs[rel] = set()

    def relate_objects(self, rel, obj1, obj2, inc=False):
        if rel not in self.rels:
            raise ValueError('Unknown relation: {}.'.format(rel))
        if obj1 not in self.objs:
            if obj1 in self.types:
                obj1 = '$' + obj1
                self.add_object(obj1)
            else:
                raise ValueError('Unknown object: {}.'.format(obj1))
        if obj2 not in self.objs:
            if obj2 in self.types:
                obj2 = '$' + obj2
                self.add_object(obj2)
            else:
                raise ValueError('Unknown object: {}.'.format(obj2))
        self.rel_2_objs[rel].add(obj1)
        k = (obj1, rel)
        if inc:
            if k in self.obj_rel_2_objs:
                self.obj_rel_2_objs[k].add(obj2)
            else:
                self.obj_rel_2_objs[k] = set([obj2])
        else:
            self.obj_rel_2_objs[k] = set([obj2])

    def unrelate_objects(self, rel, obj1, obj2=None):
        if rel not in self.rels:
            raise ValueError('Unknown relation: {}.'.format(rel))
        if obj1 not in self.objs:
            if obj1 in self.types:
                obj1 = '$' + obj1
            else:
                raise ValueError('Unknown object: {}.'.format(obj1))
        if obj2 is None:
            self.rel_2_objs[rel].remove(obj1)
            del self.obj_rel_2_objs[(obj1, rel)]
        else:
            if obj2 not in self.objs:
                if obj2 in self.types:
                    obj2 = '$' + obj2
                else:
                    raise ValueError('Unknown object: {}.'.format(obj2))
            k = (obj1, rel)
            if k not in self.obj_rel_2_objs:
                err = '{} and {} are not related by relation {}.'.format(
                    obj1, obj2, rel
                )
                raise ValueError(err)
            self.obj_rel_2_objs[k].remove(obj2)
            if not self.obj_rel_2_objs[k]:
                self.rel_2_objs[rel].remove(obj1)

    def delete_relation(self, rel):
        if rel not in self.rels:
            err = 'Unable to delete relation {}.'.format(rel)
            err += 'Relation not found.'
            raise ValueError(err)
        self.rels.remove(rel)
        del self.rel_2_objs[rel]
        keys = list(self.obj_rel_2_objs.keys())
        for k in keys:
            if k[1] == rel:
                del self.obj_rel_2_objs[k]

    def get_code(self):
        code = []
        code.append('# Objects')
        for obj in self.objs:
            if obj[0] != '$':
                code.append('obj ' + obj)
        code.append('\n# Types')
        for typ in self.types:
            code.append('type ' + typ)
        code.append('\n# Relations')
        for rel in self.rels:
            code.append('rel ' + rel)
        code.append('\n# Object types')
        for obj, types in self.obj_2_types.items():
            if len(types) > 1:
                suff = '+'
            else:
                suff = ''
            for typ in types:
                code.append(' '.join([typ + suff, obj]))
        code.append('\n# Object graph')
        for (obj1, rel), objs in self.obj_rel_2_objs.items():
            if len(objs) > 1:
                rel = rel + '+'
            for obj2 in objs:
                code.append(' '.join([rel, obj1, obj2]))
        code.append('\n# Type graph')
        for sup, subs in self.sub_types.items():
            for sub in subs:
                code.append(' '.join([sup, sub]))
        return '\n'.join(code)


    def serialize(self):
        config = {}
        config['objects'] = list(self.objs)
        config['types'] = list(self.types)
        config['relations'] = list(self.rels)
        object_types = {k: list(v) for (k, v) in self.obj_2_types.items()}
        config['object_types'] = object_types
        object_graph = []
        for (obj1, rel), objs in self.obj_rel_2_objs.items():
            object_graph.append((rel, obj1, list(objs)))
        config['object_graph'] = object_graph
        type_graph = {k: list(v) for (k, v) in self.sub_types.items()}
        config['type_graph'] =  type_graph
        return config

    @classmethod
    def deserialize(cls, config):
        world = cls()
        for obj in config['objects']:
            world.add_object(obj)
        for typ in config['types']:
            world.add_type(typ)
        for rel in config['relations']:
            world.add_relation(rel)
        for obj, types in config['object_types'].items():
            for typ in types:
                world.type_object(obj, typ)
        for rel, obj1, objs in config['object_graph']:
            for obj2 in objs:
                world.relate_objects(rel, obj1, obj2)
        for sup, sub in config['type_graph'].copy():
            world.type_type(sub, sup)
        return world

    def run(self, *args):
        arg0 = args[0]
        if arg0 == 'obj':
            assert len(args) == 2
            self.add_object(args[1])
        elif arg0 == 'type':
            assert len(args) == 2
            self.add_type(args[1])
        elif arg0 == 'rel':
            assert len(args) == 2
            self.add_relation(args[1])
        elif arg0 == 'del':
            assert len(args) ==  2
            arg1 = args[1]
            if arg1 in self.objs:
                self.delete_object(arg1)
            elif arg1 in self.types:
                self.delete_type(arg1)
            elif arg1 in self.rels:
                self.delete_relation(arg1)
            else:
                raise ValueError('Undefined token: {}.'.format(arg1))
        elif arg0 in self.types:
            if len(args) == 2:
                arg1 = args[1]
                if arg1 in self.types:
                    self.type_type(arg1, arg0)
                elif arg1 in self.rels or (arg1[-1] == '+' and arg1[:-1] in self.rels):
                    err = 'Only 1 arg provided for relation {}.'.format(arg1)
                    raise ValueError(err)
                else:
                    self.type_object(arg1, arg0)
            elif len(args) == 3:
                arg1 = args[1]
                arg2 = args[2]
                if arg1 not in self.rels:
                    raise ValueError('Unknown relation: {}'.format(arg1))
                self.relate_objects(arg1, arg0, arg2)
            else:
                raise ValueError('Too many arguments.')
        elif arg0[-1] == '!' and arg0[:-1] in self.types:
            assert len(args) == 2
            arg1 = args[1]
            if arg1 in self.types:
                self.untype_type(arg1, arg0[:-1])
            elif arg1 in self.objs:
                self.untype_object(arg1, arg0[:-1])
            else:
                raise ValueError('Undefined token: {}.'.format(arg1))
        elif arg0[-1] == '+' and arg0[:-1] in self.types:
            assert len(args) == 2
            arg1 = args[1]
            if arg1 in self.types:
                self.type_type(arg1, arg0[:-1], True)
            elif arg1 in self.objs:
                self.type_object(arg1, arg0[:-1],True)
        elif arg0 in self.rels:
            assert len(args) == 3
            self.relate_objects(arg0, args[1], args[2])
        elif arg0[-1] == '+' and arg0[:-1] in self.rels:
            assert len(args) == 3
            self.relate_objects(arg0[:-1], args[1], args[2], inc=True)
        elif arg0[-1] == '!' and arg0[:-1] in self.rels:
            if len(args) == 2:
                self.unrelate_objects(arg0[:-1], args[1])
            elif len(args) == 3:
                self.unrelate_objects(arg0[:-1], args[1], args[2])
            else:
                raise ValueError('Too many arguments.')
        elif arg0 in self.objs:
            assert len(args) == 3
            arg1 = args[1]
            if arg1 not in self.rels:
                raise ValueError('Unknown relation: {}.'.format(arg1))
            self.relate_objects(arg1, arg0, args[2])
        else:
            raise ValueError('Invalid syntax: ' + ' '.join(args))

    def save(self, path):
        with open(path, 'w') as f:
            f.write(str(self.get_code()))

    @classmethod
    def load(cls, path):
        world = cls()
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                while '  ' in line:
                    line = line.replace('  ', ' ')
                args = line.split(' ')
                if args and args[0] and args[0][0] != '#':
                    world.run(*args)
        return world

def reset(self):
    self.__init__()
