# Peow CMS
Static web-site generator

## How to install

Run ```bash
	bash first-run.sh
	```
For Ubuntu-users: ```bash
	bash first-run.sh --ubuntu
	```
## How to generate site

Run ```bash
	bash build.sh
	```
## Template structure

comming soon...

## Template engine sintax (with equvalent code in python)

+ `{%FOO%}`

	```python
	print(foo)
	```

+ `{%FOO|BAR%}`

    ```python
    print(foo['bar'])
    ```
+ `{%[FOO+1]%}`

	```python
	print(foo+1)
	```

+ `{?%FOO%>%BAR%?}...{?ELSE?}...{?END?}`

	```python
	if(foo>bar):
	    ...
    else:`
        ...
    ```
+ `{@FOO:BAR@}...{%BAR%}...{@END@}`

    ```python
    for bar in foo:
        ...
        print(bar)
        ...
    ```

+ `{@FOO:BAR@}...{%BAR%}...{@@FOO2:BAR2@}...{%BAR2%}...{@END@@}...{@END@}`

	```python
	for bar in foo:
	    ...
	    print(bar)
	    ...
	        for bar2 in foo2:
	            ...
	            print(bar2)
	            ...
	```

+ `{!FOO!}`

    ```python
    print(open('foo.html').read())
    ```

+ `{#Lorem Ipsum#}`

    ```python
    #Lorem Ipsum
    ```
