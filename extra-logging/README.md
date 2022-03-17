# Template for producer-consumer model robots using work items

This template contains a working robot implementation that has the basic structure where one part produces work items from input and another part that consumes those work items. 

> The [producer-consumer](https://en.wikipedia.org/wiki/Producer%E2%80%93consumer_problem) model is not limited to two steps, it can continue so that the consumer generates further work items for the next step and so on.

The template tries to keep the amount of functional code at a minimum so you have less to clear out and replace with your own implementation, but some functional logic is needed to have the template working and guiding the key parts.

> We recommended checking out the article "[Using work items](https://robocorp.com/docs/development-guide/control-room/work-items)" before diving in.


> Also a fully functional example robot can be found at: [Web Store Order Processor Using Work Items](https://robocorp.com/portal/robot/robocorp/example-web-store-work-items)


## Tasks

The robot is split into two tasks, meant to run as separate steps in Control Room. The first task generates (produces) data, and the second one reads (consumes) and processes that data.

### The first task (the producer)

- Load the example Excel file from work item
- Splits the Excel file into work items for the consumer

### The second task (the consumer)

> We recommended checking out the article "[Work item exception handling](https://robocorp.com/docs/development-guide/control-room/work-items#work-item-exception-handling)" before diving in.

- A simulated "Login" step.
  - This simulates random failures to highlight the use of `APPLICATION` -exception type.
- Loop that handles the work items and just creates a logs row for each
  - This simulates random failures to highlight the use of `BUSINESS` -exception type.

### Local testing

For best experience to test the work items in this example we recommend using [our VS Code extensions](https://robocorp.com/docs/developer-tools/visual-studio-code). With the Robocorp Code extension you can simply run and [select the input work items](https://robocorp.com/docs/developer-tools/visual-studio-code/extension-features#using-work-items) to use, create inputs to simulate error cases and so on.