# Research

## Bytecode Loops

if then
---
if label1
label1


if then else
---
if label1
jump label2
label1
label2


if else if
---
if label1
jump label2
label1
if label2
label2 (accessed x2)


ternary
---
if label1
jump label2 (with items on stack)
label1
label2


while
---
label1
if label2
jump label1
label2


do while
---
label1
if label1


switch
---
store register 0
if label1
if label2
jump label3
label1
jump label4
label2
jump label4
label3 (default)
label4
