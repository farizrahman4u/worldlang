def object_graph(world):
    import graphviz
    dot = graphviz.Digraph(comment='World Object Graph')
    for obj in world.objs:
        dot.node(obj, obj)
    for (obj1, rel), objs in world.obj_rel_2_objs.items():
        for obj2 in objs:
            dot.edge(obj1, obj2, label=' ' * 3 + rel)
    return dot

def type_graph(world):
    import graphviz
    dot = graphviz.Digraph(comment="World Type Graph")
    for typ in world.types:
        dot.node(typ)
    for sup, subs in world.sub_types.items():
        for sub in subs:
            dot.edge(sup, sub)
    for typ, objs in world.type_2_objs.items():
        for obj in objs:
            dot.edge(typ, obj)
    return dot