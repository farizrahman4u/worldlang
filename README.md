# worldlang

A language for building and querying world models.

------

The language has 2 parts: Build and Query.

### Build spec:

##### Creating an object

```
obj <obj_name>
```

##### Creating a type

```
type <type_name>
```
##### Creating a relation

```
rel <relation_name>
```

##### Typing an object

```
<type_name> <object_name>
```

Example:

```
obj x
type A
A x
```
An object can have multiple types. In which case use the following syntax:

```
<type1>+ <object>
<type2>+ <object>
<type3>+ <object>
```

Example:

```
obj x
type A
type B
type C
A+ x
B+ x
C+ x
```


Note: object will be create if it doesn't exist.

##### Untyping object

```
<type>! <object>
````

Example:

```
obj x
type A
A x
A! x
```

##### Relating objects

```
<object1> <relation> <object2>
````

Alternatively:

```
<relation> <object1> <object2>
```

Example:

```
obj x
obj y
rel like
x like y
# or: like x y
```


An object can be realted to multiple objects through the same relation. For such cases use the following syntax:

```
<object1> <relation>+ <object2>
<object1> <relation>+ <object3>
<object1> <relation>+ <object4>
```

Alternatively:

```
<relation>+ <object1> <object2>
<relation>+ <object1> <object3>
<relation>+ <object1> <object4>
```

Example:

```
obj x
obj a
obj b
obj c
rel has
x has+ a
x has+ b
x has+ c
```

##### Unrelating objects

```
<relation>! <object1> <object2>
```

Alternatively:
```
<object1> <relation>! <object2>
```

Example:

```
obj x
obj y
rel like
x like y
# or: like x y
x like! y
# or: like! x y
```
