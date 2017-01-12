# Peow CMS
Static web-site generator

## Template engine sintax (with equvalent code in python)

+ {%FOO%}
	`print(foo)`

+ {%FOO|BAR%}
	`print(foo['bar'])`

+ {%[FOO+1]%}
	`print(foo+1)`

+ {?%FOO%>%BAR%?}...{?ELSE?}...{?END?}
	`if(foo>bar):`
    `...`
    `else:`
    `...`

+ {@FOO:BAR@}...{%BAR%}...{@END@}
    `for bar in foo:`
    `...`
    `   print(bar)`
    `...`

+ {@FOO:BAR@}...{%BAR%}...{@@FOO2:BAR2@}...{%BAR2%}...{@END@@}...{@END@}
	`for bar in foo:`
    `...`
    `   print(bar)`
    `...`
    `   for bar2 in foo2:`
    `...`
    `       print(bar2)`
    `...`

+ {!FOO!}
    `print(open('foo.html').read())`