class World(object):

    def __init__(self):
        self.objs = set()
        self.types = set()
        self.rels = set()
        self.obj_2_types = dict()
        self.type_2_objs = dict()
        self.obj_rel_2_objs = dict()
        self.rel_2_objs = dict()

    def _assert_not_taken(self, x):
        assert x not in self.objs
        assert x not in self.types
        assert x not in self.rels

    def _is_num(self, x):
        try:
            int(x)
            return True
        except Exception:
            return False

    def run(self, *args):
        arg0 = args[0]
        if arg0 == 'obj':
            assert len(args) == 2
            objname = args[1]
            self._assert_not_taken(objname)
            self.objs.add(objname)
        elif arg0 == 'type':
            assert len(args) == 2
            typename = args[1]
            self._assert_not_taken(typename)
            self.types.add(typename)
        elif arg0 == 'rel':
            assert len(args) == 2
            relname = args[1]
            self._assert_not_taken(relname)
            self.rels.add(relname)
            self.rel_2_objs[relname] = set()
        elif arg0 == 'del':
            assert len(args) == 2
            todel = args[1]
            if todel in self.objs:
                self.objs.remove(todel)
                del self.obj_2_types[todel]
            elif todel in self.types:
                self.types.remove(todel)
                del self.type_2_objs[todel]
            elif todel in self.rels:
                self.rels.remove(todel)
                for obj in self.rel_2_objs[todel]:
                    k = (obj, todel)
                    del self.obj_rel_2_objs[k]
                del self.rel_2_objs[todel]
            else:
                raise Exception("{} not found".format(todel))
        elif arg0 in self.types:
            assert len(args) == 2
            objname = args[1]
            self.objs.add(objname)
            if arg0 not in self.type_2_objs:
                self.type_2_objs[arg0] = set([objname])
                self.obj_2_types[objname] = set([arg0])
            else:
                self.type_2_objs[arg0].add(objname)
                self.obj_2_types[objname].add(arg0)
        elif arg0 in self.objs:
            assert len(args) == 3
            rel = args[1]
            if rel[-1] == '+':
                rel = rel[:-1]
                inc = True
            else:
                inc = False
            assert rel in self.rels
            obj2 = args[2]
            assert obj2 in self.objs
            k = (arg0, rel)
            self.rel_2_objs[rel].add(arg0)
            if inc:
                if k in self.obj_rel_2_objs:
                    self.obj_rel_2_objs[k].add(obj2)
                else:
                    self.obj_rel_2_objs[k] = set([obj2])
            else:
                self.obj_rel_2_objs[k] = set([obj2])
        else:
            raise Exception(str(args))
