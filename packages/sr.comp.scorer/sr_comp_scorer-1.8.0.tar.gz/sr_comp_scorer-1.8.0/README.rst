SRComp Scorer
=============

|Build Status|

A web UI to edit scores from SRComp score files.

Deployment
----------

For using the scorer at an event:

.. code:: shell

    script/install.sh

The install script prints instructions regarding the setup of the corresponding
compstate as well as how to run the resulting instance. Currently this is aimed
at install on a user's own machine rather than being hosted externally.

Publishing Scores
~~~~~~~~~~~~~~~~~

Scores are expected to be published using the SRComp CLI ``deploy`` command.

Typically this is arranged by having SSHD running on the machine at the
score-entry desk, allowing the person who deploys the scores to *pull* them onto
their own machine before both deploying them to the various compboxes and
pushing them to archival storage (typically GitHub).

From the perspective of the person deploying the scores these steps might look like:

.. code:: shell

    git pull $SCORER_MACHINE master
    git push
    srcomp deploy .
    ssh $SCORER_MACHINE 'cd compstate && git pull --ff-only'

This setup enables the person deploying the scores to optionally act as a
reviewer, perhaps by running the scorer on their own machine in order to view
the scores without relying on physical proximity to the score-entry desk.

Development
-----------

**Install**:

.. code:: shell

    pip install -e .

**Run**:
``python -m sr.comp.scorer`` (see the ``--help``) for details.

Developers may wish to use the `SRComp Dev`_ repo to setup a dev instance.


.. |Build Status| image:: https://circleci.com/gh/PeterJCLaw/srcomp-scorer.png?branch=main
   :target: https://circleci.com/gh/PeterJCLaw/srcomp-scorer

.. _`SRComp Dev`: https://github.com/PeterJCLaw/srcomp-dev
