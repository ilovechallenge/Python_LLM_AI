.. note::

    **This is only a preview/placeholder for LMQL's documentation. The full documentation will be available on official launch.**

Welcome to LMQL!
===================================

**LMQL** (Language Model Query Language) is a programming language for large language model interaction. 
It facilitates LLM interaction by combining the benefits of natural language prompting with the expressiveness 
of Python. With only a few lines of LMQL code, users can express advanced, multi-part and tool-augmented LM queries, 
which then are optimized by the LMQL runtime to run efficiently as part of the LM decoding loop.

LMQL is a research project by the `Secure,  Reliable, and Intelligent Systems Lab <https://www.sri.inf.ethz.ch/>`_ at ETH Zürich.

Quick Start
-----------

To get started locally, check out the :doc:`quickstart` section. 
For smaller experiments, you can also use the web-based `LMQL Playground <lmql.ai/playground/>`_:

.. raw:: html

    <div class="getting-started-options">
      <div class="columns is-getting-started">
        <div class="column getting-started">
          <h2>Explore LMQL</h2>
          <a class="primary" href="https://lmql.ai/playground">
            Playground IDE
          </a>
          <a href="https://github.com/eth-sri/lmql">
            GitHub Repo 
          </a>
        </div>

        <div class="column getting-started">
          <h2>Run Locally</h2>
          <div class="cmd"> 
              pip install lmql
          </div> 
          To run LMQL locally, read the <span><a href="quickstart.html">Getting Started</a></span> section of the documentation.
        </div>
      </div>
    </div>

Contents
--------

.. toctree::
    :maxdepth: 2

    quickstart
    language/index.md
    python/index.rst
    dev-setup
