# mkdocs-codeinclude-plugin

A plugin for mkdocs that allows some advanced 'includes' functionality to be used for embedded code blocks.
This is effectively an extended Markdown format, but is intended to degrade gracefully when rendered with a different renderer. 

## Getting Started

Use in Markdown
```
<!--codeinclude--> 
[foo](Foo.java) inside_block:main
<!--/codeinclude-->
```

Use in Code
```java
public class Foo {

    // main {
    public void bar() {
        System.out.print("Foo Bar")
    }
    // }}
}
```

Will generate:
```java
public void bar() {
    System.out.print("Foo Bar")
}
```

## Development

_**TODO**_ Add documentation

Explain how to run the automated tests for this system

### Running the tests

_**TODO**_ Add documentation

## Deployment

_**TODO**_ Add documentation

## Built With

* [MkDocs](https://www.mkdocs.org/) - The framework used


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [mkdocs-codeinclude-plugin](https://github.com/rnorth/mkdocs-codeinclude-plugin). 

## Authors

* **Richard North** - *Initial work* - [Richard North](https://github.com/rnorth)

See also the list of [contributors](https://github.com/rnorth/mkdocs-codeinclude-plugin/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
