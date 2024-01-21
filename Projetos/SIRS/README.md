# C54 GrooveGalaxy Project Read Me

## Team

| Number | Name                 | User                                            | E-mail                                           |
| -------|----------------------|-------------------------------------------------| -------------------------------------------------|
| 99079  | Guilherme Pascoal    | <https://github.com/Dredegui>                   | <mailto:guilherme.pascoal@tecnico.ulisboa.pt>    |
| 99083  | Guilherme Batalheiro | <https://github.com/guilherme-batalheiro>       | <mailto:guilherme.batalheiro@tecnico.ulisboa.pt> |
| 99097  | José Cutileiro       | <https://github.com/JoseCutileiro>              | <mailto:jose.cutileiro@tecnico.ulisboa.pt>       |

![Alice](img/alice.jpg) ![Bob](img/bob.png) ![José Cutileiro](img/charlie.png)

*(add face photos with 150px height; faces should have similar size and framing)*

## Contents

This repository contains documentation and source code for the *Network and Computer Security (SIRS)* project.

The [REPORT](REPORT.md) document provides a detailed overview of the key technical decisions and various components of the implemented project.
It offers insights into the rationale behind these choices, the project's architecture, and the impact of these decisions on the overall functionality and performance of the system.

This document presents installation and demonstration instructions.

## Installation TODO

To see the project in action, it is necessary to setup a virtual environment, with N networks and M machines.  

The following diagram shows the networks and machines:

*(include a text-based or an image-based diagram)*

### Prerequisites TODO

All the virtual machines are based on: Linux 64-bit, Kali 2023.3  

[Download](https://...link_to_download_installation_media) and [install](https://...link_to_installation_instructions) a virtual machine of Kali Linux 2023.3.  
Clone the base machine to create the other machines.

*(above, replace witch actual links)*

### Machine configurations TODO

For each machine, there is an initialization script with the machine name, with prefix `init-` and suffix `.sh`, that installs all the necessary packages and makes all required configurations in the a clean machine.

Inside each machine, use Git to obtain a copy of all the scripts and code.

```sh
$ git clone https://github.com/tecnico-sec/cxx...
```

*(above, replace with link to actual repository)*

Next we have custom instructions for each machine.

#### Machine 1 TODO

This machine runs ...

*(describe what kind of software runs on this machine, e.g. a database server (PostgreSQL 16.1))*

To verify:

```sh
$ setup command
```

*(replace with actual commands)*

To test:

```sh
$ test command
```

*(replace with actual commands)*

The expected results are ...

*(explain what is supposed to happen if all goes well)*

If you receive the following message ... then ...

*(explain how to fix some known problem)*

#### Machine ...

*(similar content structure as Machine 1)*

## Demonstration

Now that all the networks and machines are up and running, ...

*(give a tour of the best features of the application; add screenshots when relevant)*

```sh
$ demo command
```

*(replace with actual commands)*

*(IMPORTANT: show evidence of the security mechanisms in action; show message payloads, print relevant messages, perform simulated attacks to show the defenses in action, etc.)*

This concludes the demonstration.

## Additional Information

### Links to Used Tools and Libraries

- [Python 3.9.0](https://www.python.org/downloads/release/python-390/)
- [cryptography 41.0.7](https://pypi.org/project/cryptography/)
- [Flask 3.0.0](https://flask.palletsprojects.com/en/3.0.x/)
- [Postgresql](https://www.postgresql.org/)
- [pgAdmin](https://www.pgadmin.org/)

### License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) for details.

*(switch to another license, or no license, as you see fit)*

----
END OF README
