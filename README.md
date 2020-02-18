# mkdocs-codeinclude-plugin

A plugin for mkdocs that allows some advanced 'includes' functionality to be used for embedded code blocks.
This is effectively an extended Markdown format, but is intended to degrade gracefully when rendered with a different renderer. 

## Usage

A codeinclude block resembles a regular markdown link surrounded by a pair of XML comments, e.g.:

<!-- 
To prevent this from being rendered as a codeinclude when rendering this page, we use HTML tags.
See this in its rendered form to understand its actual appearance, or look at other pages in the
docs.
-->

<pre><code>&lt;!--codeinclude--&gt;
[Human readable title for snippet](./relative_path_to_example_code.java) targeting_expression
&lt;!--/codeinclude--&gt;
</code></pre>

Where `targeting_expression` could be:

* `block:someString` or
* `inside_block:someString`

If these are provided, the macro will seek out any line containing the token `someString` and grab the next curly brace
delimited block that it finds. `block` will grab the starting line and closing brace, whereas `inside_block` will omit 
these.

e.g., given:
```java

public class FooService {

    public void doFoo() {
        foo.doSomething();
    }

}
```

If we use `block:doFoo` as our targeting expression, we will have the following content included into our page:

```java
public void doFoo() {
    foo.doSomething();
}
```

Whereas using `inside_block:doFoo` we would just have the inner content of the method included:

```java
foo.doSomething();
```

Note that:

* Any code included will be have its indentation reduced
* Every line in the source file will be searched for an instance of the token (e.g. `doFoo`). If more than one line
  includes that token, then potentially more than one block could be targeted for inclusion. It is advisable to use a
  specific, unique token to avoid unexpected behaviour.
  
When we wish to include a section of code that does not naturally appear within braces, we can simply insert our token,
with matching braces, in a comment. 
While a little ugly, this has the benefit of working in any context, even in languages that do not use
curly braces, and is easy to understand. 
For example:

```java
public class FooService {

    public void boringMethod() {
        doSomethingBoring();
        
        // doFoo {
        doTheThingThatWeActuallyWantToShow();
        // }
    }

}
```

will be rendered as:

```java
doTheThingThatWeActuallyWantToShow();
```

## Building the Project

Install the dependencies:

```shell
pip install -r requirements.txt
pip install nose # Optionally, install nose to run the tests
```

Run the tests:
```shell
nosetests
```
