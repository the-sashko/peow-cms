# Peow CMS
Static web-site generator

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
