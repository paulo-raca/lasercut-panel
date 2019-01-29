# Generate SVG file with profile for a retangular frame with tabs on the top edge

## Example usage


### Single tab
```
$ ./create_outline.py 15x10 --units=cm --hole-size=.5 --hole-padding=.75 > demo1.svg
```
![Single tab](demo1.svg)


### Two tabs
```
$ ./create_outline.py 15x10 --units=cm --hole-size=.5 --hole-padding=.75 > demo2.svg
```
![Two tabs](demo2.svg)

### Two tabs, aligned to corners

```
$ ./create_outline.py 15x10 --units=cm --hole-size=.5 --hole-padding=.75 --tabs=2 --from-border > demo3.svg
```
![Two tabs, aligned to corners](demo3.svg)

### Many tabs

```
$ ./create_outline.py 15x10 --units=cm --hole-size=.5 --hole-padding=.75 --tabs=5 > demo4.svg
```
![Many tabs](demo4.svg)

### Many tabs, aligned to corners

```
$ ./create_outline.py 15x10 --units=cm --hole-size=.5 --hole-padding=.75 --tabs=5 --from-border > demo5.svg
```
![Many tabs, aligned to corners](demo3.svg)

