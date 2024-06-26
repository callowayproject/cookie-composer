# Composition files

Composition files are YAML documents with layer configurations. They are used for generating new projects and recording how a current project was generated. The composition files used for generating new projects are usually minimal, compared to the `.composition.yaml` file `cookie-composer` writes in the project as a record of state.

For example, a basic composition file for generating new projects might look like:

```python title="Example composition" 
--8<-- "example-composition.yaml"
```

When this is used to create a project:

```console title="An interactive console example"
--8<-- "interactive-create.txt"
```

The composition file saved in the new project (named `my-test-project` in this example) as `.composition.yaml` would look like:

```console title="A rendered composition"
--8<-- "rendered-composition.yaml"
```

If you look closely you'll see that `.composition.yaml` contains the contents of `package-composition.yaml`. Internally the `.composition.yaml` file is termed a "rendered composition" because it contains all the parameters used to render this specific project. This rendered composition is used when applying updates of the templates. 

## Template layers

Composition files are technically [YAML streams](https://yaml.org/spec/1.2.2/#22-structures) consisting of one or more documents describing a layer configuration.
