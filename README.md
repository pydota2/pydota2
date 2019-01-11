# pydota2
PyDota2 Framework Integrated with DotaService, DotaWorld and DotaClient

# Building / Installing
The following command should pull down the pydota2 repo with all submodules
also recursively pulled down (up to 8 simulatenously)

`git clone --recurse-submodules -j8 git https://github.com/pydota2/pydota2.git`

Once the clone completes you should have a `build.sh` at the top-level 
pydota2 directory. So...

`cd pydota2`

`./build.sh`

This should build all the appropriate modules needed to run the system.
`dotaservice`, `dotaworld`, `pydota2`

Note, `dotaclient` is not built as a module b/c we launch code from within
it direclty on the command shell (it depends on how you want to run the AI - 
distributed over K8s, locally, seeded with a pretrained model, etc.).

# Execution
First, launch the dotaservice module

`python3.7 -m dotaservice`

Next, launch the dotaclient optimizer

`python dotaclient/optimizer.py`

Finally, launch the dotaclient agent (with options you want)

`python dotaclient/agent.py [--local True] [--pretrained-model <PATH>]`

As the agent runs it will put updated models of what it learned in the 
`runs/` directory (subdirectories named by date/time of execution)

# Acknowledgments
Much of this code is co-developed with Tim Zaman
[Tim Zaman](https://github.com/TimZaman)
