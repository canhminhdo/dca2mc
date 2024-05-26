# A Tableau-based Approach to Model Checking Linear Temporal Properties
This repository presents a support tool called `DCA2MC` for the tableau-based approach to model checking linear temporal properties.

The core idea is to split the original model checking problem into smaller model checking problems and tackle each smaller one. We creatively use the tableau-based method to perform the division. For each intermediate layer, we need to collect states and formulas that should be satisfied by the states located at the beginning of the next layer.
For the final layer, we conduct model checking experiments for each state and its formulas.

## 1. How to use `DCA2MC`
`DCA2MC` provides an interactive mode for users with the following commands, where `_` denotes the arguments for the commands.

- `initialize[_,_,_]` initialize the application with a system module ID, an initial state, and an LTL formula as a desired property for model checking as inputs.

- `layerCheck _` generates states and formulas with a layer configuration `_`, that is a list of nonzero natural numbers (e.g., 2 2).

- `lastCheck` conducts model checking experiments for the final layer.

- `check _` sequentially performs the `layerCheck _` and `lastCheck` commands.

- `analyze` shows the current state with some information from the application for debugging.

- `help` shows the command instructions.

- `exit` quits the application

## 2. A case study with `DCA2MC`

Let us show how to conduct a model checking expeirment for TAS protocol with `DCA2MC`.

**Step 1:** Start the application with the following commands:

```
load specs/tas.maude
maude dca2mc.maude
```
We first load the formal specification of the TAS protocol in Maude and then load our support tool via the `dca2mc.maude` file.

**Step 2:** Initialize the application to model check that Qlock enjoys a desired property.

```
initialize['QLOCK-CHECK, init, lofree]
```

where `'QLOCK-CHECK` is the system module ID, `init` is the initial state, and `lofree` is the desired property.

**Step 3:** Conduct model checking experiments for intermediate layers.

```
layerCheck 2 2
```

where `2 2` is the layer configuration denoting the first and second layer depths are 2 and 2, respectively.

**Step 4:** Conduct model checking experiments for the final layer.

```
lastCheck
```
This command will return `true` if Qlock enjoys the desired property; otherwise, `false` is returned.

**Step 5:** Quit the application.

```
q
```

## 3. Publications
TBA