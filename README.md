# A Divide & Conquer Approach to Model Checking Linear Temporal Properties
This repository presents a support tool called `DCA2MC` for the divide & conquer approach to model checking linear temporal properties.

The core idea is to split the original model checking problem into smaller model checking problems using the tableau-based method and tackle each smaller one. As a result, the original reachable state space is split into multiple layers. For each intermediate layer, we need to collect all states located at the bottom of the layer and their associated formulas that should be considered for the states, and use them as the inputs for the next layer. For the final layer, we conduct model checking experiments for each state and its associated formulas independently.

## 1. How to use `DCA2MC`
`DCA2MC` provides an interactive mode for users with the following commands, where `_` denotes the arguments for the commands.

- `initialize[_,_,_]` initialize the application with a system module ID, an initial state, and an LTL formula as a desired property for model checking as inputs.

- `layer-check _` generates states and formulas with a layer configuration `_`, that is a list of nonzero natural numbers (e.g., 2 2).

- `last-check` conducts model checking experiments for the final layer.

- `set-cores _` sets the number of workers for parallelization, handling state and formula generation at each intermediate layer and conducting model checking experiments in the final layer.

- `set-checker _` specifies an external model checker (e.g., Spin) for interaction. Currently, only Spin is supported.

- `set-checker-cores _` defines the number of external model checker clients used for parallelization.

- `set-seed _` to set the random seed for state selection.

- `select-states _` randomly selects a specified number of states.

<!-- 
- `check _` sequentially performs the `layerCheck _` and `lastCheck` commands. 
-->

- `analyze` shows the current state with some information from the application for debugging.

- `help` shows the command instructions.

- `quit` exits the application.

## 2. `DCA2MC` with an example

Let us show you how to conduct a model checking experiment for Qlock protocol with `DCA2MC`.

**Step 1:** Start the application with the following commands:

```
load specs/qlock.maude
maude dca2mc.maude
```
We first load the formal specification of Qlock protocol in Maude and then load our support tool via the `dca2mc.maude` file.

**Step 2:** Initialize the application to model check that Qlock enjoys a desired property.

```
initialize[QLOCK-CHECK, init, lofree]
```

where `QLOCK-CHECK` is the system module ID, `init` is the initial state, and `lofree` is the desired property under verification (i.e., the lockout freedom property).

**Step 3:** Use parallelization with 8 workers for `DCA2MC`.

```
set-cores 8
```

**Step 4:** Conduct model checking experiments for intermediate layers.

```
layer-check 2 2
```

where `2 2` is the layer configuration denoting the first and second layer depths 2 and 2, respectively.

**Step 4:** Conduct model checking experiments in the final layer.

```
last-check
```
This command will return `true` if Qlock enjoys the desired property; otherwise, `false` is returned. Because the command returned `true` in this case, we conclude that Qlock satisfies the desired property with the initial state using `DCA2MC`.

**Step 5:** Exit the application.

```
quit
```

## 3. Publications

- Canh Minh Do, Tsubasa Takagi, Kazuhiro Ogata: A Tableau-based Approach to Model Checking Linear Temporal Properties, The 25th International Conference on Formal Engineering Methods (ICFEM), LNCS 15394, pp. 353-374, Springer, 2024. (DOI: [10.1007/978-981-96-0617-7_20](https://doi.org/10.1007/978-981-96-0617-7_20))