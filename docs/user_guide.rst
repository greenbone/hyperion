.. _user_guide:

User Guide
##########

.. contents::
    :local:
    :class: toc
    :backlinks: none


Introduction
============
**hyperion** provides a GraphQL API for **gvmd**. To learn about GraphQL, please
read `Introduction to GraphQL <https://graphql.org/learn/>`_ or any of the
excellent guides found online.

Making Requests
===============

**hyperion** provides a variety of queries and mutations one can send to
**gvmd**, but most of them are locked behind the `login` mutation for security
reasons. Therefore before running any other query, please run (substituting
admin/admin for your gvmd credentials):

.. code-block::

    mutation {
        login (username: "admin", password: "admin") {
            ok
        }
    }

Upon success, you should see the response:

.. code-block::

    {
        "data": {
            "login": {
                "ok": true
            }
        }
    }

As examples, we will document all the available GraphQL queries and mutations
for tasks here. To see the full documentation for this entity, including the
optional arguments, please see :ref:`api/task <task>`.

Queries
-------

Example Query: Getting a single task
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**hyperion** supports both querying for a single task and a list of tasks. To
query a single task, run the following:

.. code-block::

    query {
        task (taskId: "4d55e723-32d4-4746-b59b-d763b3cfc856") {
            name
            owner
            creationTime
        }
    }

This should return:

.. code-block::

    {
        "data": {
            "task": {
                "name": "newtask",
                "owner": "admin",
                "creationTime": "2020-02-26T10:12:28+00:00"
            }
        }
    }

The `task` query runs `get_task()` from **python_gvm** and `taskId` is the only
argument. `name, owner` and `creationTime` are all fields available to query.
To get a complete list of fields please refer to the
:ref:`API documentation <task_queries>`.

Example Query: Getting a list of tasks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To get a list of tasks, run

.. code-block::

    query {
        tasks {
            nodes {
                uuid
                name
                owner
                comment
            }
        }
    }

This query returns:

.. code-block::

 {
    "data": {
        "tasks": {
            "nodes": [
                {
                    "uuid": "4d55e723-32d4-4746-b59b-d763b3cfc856",
                    "name": "newtask",
                    "owner": "admin",
                    "comment": null
                },
                {
                    "uuid": "1fb47870-47ce-4b9f-a8f9-8b4b19624c59",
                    "name": "TLS",
                    "owner": "admin",
                    "comment": null
                },
                ...
            ]
        }
    }
 }

Unlike getting a single task, the `nodes` field is required because **hyperion**
uses relay for pagination. This applies for all queries for a list of entities.

This query takes an optional argument `filterString`. If you've used **gsa**
before, they have the same format as the filter strings used there.

.. insert link to api docs here

For example:

.. code-block::

    query {
        tasks (filterString: "name~TLS rows=4") {
            nodes {
                uuid
                name
            }
        }
    }

Which returns something like:

.. code-block::

    {
        "data": {
            "tasks": {
                "nodes": [
                    {
                        "uuid": "1fb47870-47ce-4b9f-a8f9-8b4b19624c59",
                        "name": "TLS"
                    },
                    {
                        "uuid": "5d07b6eb-27f9-424a-a206-34babbba7b4d",
                        "name": "TLS Clone 1"
                    },
                    {
                        "uuid": "3e2dab9d-8abe-4eb6-a3c7-5171738ac520",
                        "name": "TLS Clone 2"
                    },
                    {
                        "uuid": "49415287-32e7-4451-9424-df4e44bffc6c",
                        "name": "TLS Clone 3"
                    }
                ]
            }
        }
    }

Mutations
---------

Example Mutation: Cloning a task
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To clone a task, run the following mutation:

.. code-block::

    mutation {
        cloneTask (taskId: "4d55e723-32d4-4746-b59b-d763b3cfc856") {
            taskId
        }
    }

`cloneTask` takes *one* required argument `taskId`, and returns the `taskId` of
the cloned task. The response looks like this:

.. code-block::

    {
        "data": {
            "cloneTask": {
                "taskId": "93e8bf46-155a-4b23-be15-605c918e9c01"
            }
        }
    }

To delete a task with a given `taskId`, simply substitute `deleteTask` in the
above mutation, and replace the returned `taskId` with `ok`.

Example Mutation: Creating a task
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create a task, run the following mutation:

.. code-block::

    mutation {
        createTask (
            name: "created",
            configId: "daba56c8-73ec-11df-a475-002264764cea",
            scannerId: "08b69003-5fc2-4037-a479-93b440211c73",
            targetId: "30c12207-a957-4a52-91cf-0d6ac695f12e",
            comment: "hello world!"
        ) {
            taskId
        }
    }

Response:

.. code-block::

    {
        "data": {
            "createTask": {
                "taskId": "f5c40267-71ab-4cd7-b14b-3599a84522e8"
            }
        }
    }

The fields `name, configId, scannerId` and `targetId` are required. The rest are
optional. This mutation returns the id of the task you just created.

Example Mutation: Modifying a task
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To modify the task we just created, run:

.. code-block::

    mutation {
        modifyTask (
            taskId: "f5c40267-71ab-4cd7-b14b-3599a84522e8",
            name: "modified",
            comment: "To be or not to be"
        ) {
            taskId
        }
    }

For this mutation, all arguments *except* `taskId` are optional. If an argument
is not given, such as `scannerId`, it will remain unchanged.

Troubleshooting
===============

When using or developing for **hyperion**, you may run into some common errors
with some common solutions.

Error: /var/run/gvmd.sock not found
-----------------------------------

Solution: Your `gvmd.sock` is not in the default location. Change Django
settings to use your custom location instead.

Error: Connection refused
-------------------------

Solution: **gvmd** may be down or not started. Make sure it is running by

.. code-block:: bash

    ps ax | grep gvmd

Error: Not Authorized
---------------------

Solution: Your `login` mutation credentials were incorrect, or it was not run.
