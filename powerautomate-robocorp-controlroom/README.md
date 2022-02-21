# Power Automate triggering a Process in Robocorp Control Room

This example will use Microsoft Power Automate flow to monitor new items
on Sharepoint list and on each new item will trigger a Robocorp Control Room
process with email.

## About Sharepoint list item details

This example will read Sharepoint list `Item` contents from the email body of
the received trigger email. This is not the most secure way, because data is
included in the email.

Alternative approach would be to send link to Sharepoint `Item` and Robot
would access that via MSGraph API.

## Steps

Assumption: You have some Sharepoint list which benefits from this Robot.

1. Create a Robocorp Robot task which will execute on email trigger
2. Configure a process in Robocorp Control Room
3. Configure a flow in the Microsoft Power Automate

### Step 1. Create a Robocorp Robot task which will execute on email trigger

The Power Automate sends email body as HTML and it can't be configured to plain text.
Due to this restriction we will be sending item from Power Automate within placeholder texts to identify `Item` in the email body.
The `Item` will be placed between **ITEMBODYSTART** and **ITEMBODYEND** texts (this will happen at step 3.)

Robot is using custom library (``SharepointLibrary.py``) to get the `Item` from the email and
``RPA.Robocorp.WorkItems`` library to read work item variable `parsedEmail` which is a variable
automatically provided by the library when Work Item has been triggered with email.
The `parsedEmail` contains all email fields, but in this example we will using only `Body`
field.

Robot will then output all the key-value pairs of the Sharepoint Item.

### Step 2. Configure a process in Robocorp Control Room

Upload Robot to your Robocorp Control Room Workspace. Create new process into Control Room and from `Configure Process` add a step
executing ``Power Automating`` task of this Robot. Still in the `Configure process` switch to `Schedules & Triggers` and add
`Trigger the process with email` - this will generate unique email address which can be used to trigger this Process with an email.
Make a copy of the email address as it is needed when we will in the next step configure Power Automate.

![Configure step](images/configure_process_1.png)
![Configure email trigger](images/configure_process_2.png)

Link. [https://cloud.robocorp.com](https://cloud.robocorp.com)

### Step 3. Configure a flow in the Microsoft Power Automate

Create a flow into Microsoft Power Automate. You can start with the blank flow. The flow consists of three steps.

**Step 3.1.** Sharepoint. "When an item is created". This step requires that we will configure Sharepoint site address and the name of the list.

**Step 3.2.** Sharepoint. "Get item". This step requires that we will configure Sharepoint site address, the name of the list and the Id of the Item
(for the Id we will be using the ID from step 1). The Body returned by "Get Item" is a dictionary containing all fields in the Item.

**Step 3.3.** Email. "Send an email notification (V3)". This step requires that we will configure `To` address (put here the Robocorp Process trigger email
address from Step 2), `Subject` can be anything because our Robot is not using that information and in the `Body` place the `Body` from step 3.2 "Get Item"
between placeholder texts.

![Flow steps](images/power_automate_flow.png)

Link. [https://flow.microsoft.com](https:/flow.microsoft.com)

## Result

![Result in the log.html](images/log_of_the_result.png)

