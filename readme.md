# Elliptic Curve Jacobian Point Operations

## Note

* This readme is written with the assumption that mathjax is enabled(LaTeX renderer for markdown).
* `<0>` denotes the point at infinity
* There are 2 scriptfiles with output of examples of usage, use `cat scriptfile` and `cat scriptfile-pypy`
* For large curves use pypy3, a JIT compiler for Python, it dramatically reduces the time to
run for example:

```
➜  proj3-jacobian git:(master) ✗ time (pypy3 ./driver.py -a 13 -b 17 -m 1000003 -o /dev/null)
( pypy3 ./driver.py -a 13 -b 17 -m 1000003 -o /dev/null; )  9.32s user 0.16s system 99% cpu 9.532 total
```

## Usage

Curve:

$$y^2 \cong x^3 + ax^2z^4 + bz^6 \bmod m$$

Example Curve:

$$y^2 \cong x^3 + x^2z^4 + z^6 \bmod 31$$

Help:

`./driver.py -h`

Output to file (stdout by default)

`./driver.py [...] -o outputfile`

## Input File

To use a file as an input, `-a A -b B -m M` can be omitted.

`./driver.py -i inputfile`

Where `inputfile` is a space denominated file with `A B M`.

Example:
```
a b m
```

## Prime Order Curve

`./driver.py -a A -b B -m M`

Example

`./driver.py -a 1 -b 1 -m 31`

## Brute Force

Brute force method

`./driver.py -a A - b B -m M --brute`

Example

`./driver.py -a 1 -b 1 -m 31 --brute`

## Verbose Brute Force

Brute force and all orders of points

`./driver.py -a A - b B -m M --brute -bv`

Example

`./driver.py -a 1 -b 1 -m 31 --bv`

## Point Group

Generate the order of the point verbosely
There is also a flag(`--affine` to print out in affine space)

`./driver.py -a A -b B -m M -px X`

or

`./driver.py -a A -b B -m M -px X -py Y`

or

`./driver.py -a A -b B -m M -px X -py Y -pz Z`

Example

`./driver.py -a 1 -b 1 -m 31 -px 0 --affine`

Example Output:

```
0p = <O>
1p = <0, 1, 1>
2p = <8, 26, 1>
3p = <10, 22, 1>
4p = <22, 21, 1>
5p = <17, 23, 1>
6p = <19, 20, 1>
7p = <13, 17, 1>
8p = <23, 16, 1>
9p = <12, 6, 1>
10p = <28, 8, 1>
11p = <5, 21, 1>
12p = <11, 17, 1>
13p = <7, 17, 1>
14p = <21, 13, 1>
15p = <4, 10, 1>
16p = <3, 0, 1>
17p = <4, 21, 1>
18p = <21, 18, 1>
19p = <7, 14, 1>
20p = <11, 14, 1>
21p = <5, 10, 1>
22p = <28, 23, 1>
23p = <12, 25, 1>
24p = <23, 15, 1>
25p = <13, 14, 1>
26p = <19, 11, 1>
27p = <17, 8, 1>
28p = <22, 10, 1>
29p = <10, 9, 1>
30p = <8, 5, 1>
31p = <0, 30, 1>
32p = <O>
```
