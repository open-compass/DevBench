To add a new school

```
./UMM add scholl -name Maths
```

Add a student named John and a teacher named Bob to School of Maths

```
./UMM add person -name John -age 20 -type 1 -school 1
./UMM add person -name Bob -age 40 -type 2 -school 1
```

Change the age of John

```
./UMM update person -id 1 -age 21
```

List all school

```
./UMM list school
```

List all students aged 20

```
./UMM list person -type 1 -age 20
```

Set Bob as the mentor of John

```
./UMM mentor assgin -student 1 -mentor 2
```