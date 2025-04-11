In Video Quiz XBlock
====================

This XBlock allows for Open edX components to be displayed to users inside of videos at specific time points.

Overview
--------

This XBlock expects to have a **Video component** and a **Problem component**
added to the same Unit as itself.

The XBlock is then configured (see below) to map timestamps (in seconds)
to Component IDs (the Problems), along with the Video Component ID.

Whenever video playback reaches a configured timestamp, the video is
paused and the corresponding Problem Component is overlayed on top of
the Video.

The user can answer problem, though it is not required.

When the user clicks "Continue", the problem is closed and the video
resumes where it left off.

Multiple timestamps can be configured per video.

Installation
------------

Tutor
*****

To add the In Video Quiz XBlock package to Tutor, follow these steps:

1. Add the package to the ``OPENEDX_EXTRA_PIP_REQUIREMENTS`` using the following command:

.. code:: bash

    tutor config save --append OPENEDX_EXTRA_PIP_REQUIREMENTS="git+https://github.com/openedx/xblock-in-video-quiz@LATEST_RELEASE"


5. Rebuild the Open edX image to include the new package:

   .. code:: bash

       tutor images build openedx

6. Start or restart the Open edX platform:

   .. code:: bash

       tutor local start -d

The In Video Quiz XBlock should now be installed and available for use in your Open edX instance.

Other
*****

Install the requirements into the python virtual environment of your
``edx-platform`` installation by running the following command from the
root folder:

.. code:: bash

    make requirements

Enabling in Studio
------------------

You can enable the In Video Quiz XBlock in Studio through the
advanced settings.

1. From the main page of a specific course, navigate to
   ``Settings -> Advanced Settings`` from the top menu.
2. Add the ``"invideoquiz"`` to your ``Advanced module list``.
3. Click the "**Save changes**" button.

.. image:: ./images/advanced-settings.png
  :alt: Advanced Settings
  :width: 500px
  :align: center


Configuration in Studio
-----------------------

``Video Location``: The ID of the Video Component, eg:
    ``cf5557d7eee9408786116f9fead8b2ba``
``Problem Timemap``: A JSON dictionary with:
    - timestamps (in seconds, as a string) as keys
    - a problem component ID as the value, eg:
    ``{"5": "10fd296e593e404ba999d78c6a76db84"}``

This would display the Problem ``10fd29...`` 5 seconds into Video ``cf5557...``.

TODO: This should be further fleshed out to explain how to get these
values, etc.

Testing in LMS
--------------

To see the full behavior, you must use the masquerade feature to
impersonate a normal learner.

When viewing the Unit as a Staff/Instructor, you will instead see a
debug note that displays at which point the video will be paused for the
problem.

Implementation Notes
--------------------

This approach is both clever and brittle.

With a small amount of code, we're able to leverage the functionality of
existing problems and the video player into a fairly elegant solution.

But as it depends upon expected behavior and display in the LMS,
it requires a specific configuration
and the behavior is vulnerable to breaking as the LMS experience changes
(eg, the conversion to the Learning MFE from the Legacy Courseware).

Future Work/Ideas
-----------------

Ideally, this XBlock would be a Parent Component,
that contains the Video+Problem components as children.

This would make the feature more resilient to LMS changes, as it would
"know" which components to use and how to find and use them,
without brittle lookups.

Setup and configuration would also be simplified, easing adoption.

A more customized Studio View could be added (along with, or in spite
of the Parent Component change), which would also simplify
configuration.

License
-------

This software was forked from https://github.com/Stanford-Online/xblock-in-video-quiz

All contribution made to those repositories, the last of which is tagged
`final-bsd-3c-contribution`_, are licensed by the original contributors under
the terms of the `BSD 3-Clause License`_.

This software is now maintained for the purpose of the Open edX Project, which
licenses any further contributions to this repository under `the AGPLv3 license`_.

.. _final-bsd-3c-contribution: https://github.com/openedx/xblock-in-video-quiz/releases/tag/final-bsd-3c-contribution
.. _BSD 3-Clause License: ./LICENSE-BSD-3c
.. _the AGPLv3 license: ./LICENSE
