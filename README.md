# Castle Builders

> SWF decompilation tool, written for Castle Crashers

## Goals

- [x] Lexer
  - [x] Main.swf opcodes
  - [x] All opcodes
    - [ ] Not and Unknown
- [x] Parser
  - [x] To P-Code
  - [x] To Actionscript
    - [x] Expressions
    - [x] If Else
    - [ ] If Else If
    - [ ] Ternary If Else
    - [x] Switch case
    - [x] While loop
    - [ ] Do While
    - [ ] For loop
    - [ ] Arithmic precedence
    - [ ] String handling
    - [ ] While in If
  - [ ] To Bytes
- [ ] Reading SWF
  - [x] Code
  - [ ] Assets
  - [ ] Other
- [ ] Writing SWF
  - [ ] Code
  - [ ] Assets
  - [ ] Other
- [x] Runtime
  - [x] One file
  - [ ] Multiple files
- [ ] Fix Sly issues
  - [ ] WARNING: shift/reduce conflicts
  - [ ] spaces / newlines
  - [ ] DRY code

## Usage

Doesn't actually accept SWF's just yet

```
$ python runtime.py {filename.swf}
```

P-Code

```
$ python runtime.py {filename.swf} --pcode
```

## Tests

```
$ python -m unittest discover
```

## Decompilation Example

Bytes in SWF

```
88 06 00 01 00 66 69 62 00 8e 0e 00 66 69 62 00 01 00 02 2a 00 01 6e 00 58 00 96 02 00 04 01 96 05 00 07 02 00 00 00 48 12 9d 02 00 0a 00 96 02 00 04 01 99 02 00 39 00 96 02 00 04 01 96 05 00 07 01 00 00 00 0b 96 05 00 07 01 00 00 00 96 02 00 08 00 3d 96 02 00 04 01 96 05 00 07 02 00 00 00 0b 96 05 00 07 01 00 00 00 96 02 00 08 00 3d 47 3e 00
```

Decompiled ActionScript

```
function fib(n)
{
  return n < 2 ? n : fib(n - 1) + fib(n - 2);
}
```

# Links

- http://www.doc.ic.ac.uk/lab/labman/swwf/SWFalexref.html
